import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {hash} from './index-files.mjs';
import {discoverTargets} from './discovery.mjs';
import sourceTools from './kv-source.cjs';
export function parseArgs(args){
 const options={};
 for(let i=0;i<args.length;i++){
  const key=args[i];
  if(['--all','--retain','--ensure','--help'].includes(key))options[key.slice(2)]=true;
  else if(['--section','--version','--site-dir','--publish-dir'].includes(key)){
   const value=args[++i];if(!value||value.startsWith('--'))throw Error(`Missing value for ${key}`);options[key.slice(2)]=value;
  }else throw Error(`Unknown option: ${key}`);
 }
 if(options.help)return options;
 if(Boolean(options.all)===Boolean(options.section))throw Error('Choose --all or --section');
 if(options.version&&!options.section)throw Error('--version requires --section');
 return options;
}
export function selectTargets(registry,options){
 const selected=registry.filter(t=>options.all||(t.section===options.section&&(!options.version||t.version===options.version)));
 if(!selected.length)throw Error('No configured semantic index matches this section/version');
 return selected;
}
export function inspect(directory){
 const file=path.join(directory,'manifest.json');
 if(!fs.existsSync(file))return {missing:true};
 const manifest=JSON.parse(fs.readFileSync(file));
 if(!manifest.index||!manifest.vectors||!manifest.assets?.[manifest.index]||!manifest.assets?.[manifest.vectors])throw Error('Invalid index manifest');
 for(const name of [...(manifest.indexParts||[manifest.index]),...(manifest.vectorParts||[manifest.vectors])])if(!manifest.assets[name])throw Error('Missing index shard checksum');
 for(const name of Object.keys(manifest.assets)){
  if(path.basename(name)!==name)throw Error('Invalid index asset path');
  if(!fs.existsSync(path.join(directory,name)))return {missing:true,manifest};
 }
 return {missing:false,manifest};
}
export function validateIndex(root,target,model,sourcePath){
 const dir=path.join(root,target.directory),{missing,manifest:m}=inspect(dir);
 if(missing)throw Error(`Missing index: ${target.section}`);
 for(const [file,digest] of Object.entries(m.assets))if(hash(fs.readFileSync(path.join(dir,file)))!==digest)throw Error(`Corrupt index asset: ${file}`);
 for(const key of ['modelDirectory','dimensions','dtype','runtime'])if(m[key]!==model[key])throw Error(`Index/runtime mismatch: ${key}`);
 const passages=(m.indexParts||[m.index]).flatMap(file=>JSON.parse(fs.readFileSync(path.join(dir,file))));
 if(passages.length!==m.passages||passages.some(p=>!p.url.startsWith(target.scope)))throw Error('Index scope/count mismatch');
 if((m.vectorParts||[m.vectors]).reduce((bytes,file)=>bytes+fs.statSync(path.join(dir,file)).size,0)!==m.passages*m.dimensions*4)throw Error('Vector dimensions mismatch');
 if(target.kind==='markdown'){
  const dir=path.join(root,target.source),names=fs.readdirSync(dir).filter(n=>n.endsWith('.md')).sort();
  if(JSON.stringify(names)!==JSON.stringify(Object.keys(m.sources||{}).sort())||names.some(n=>hash(fs.readFileSync(path.join(dir,n)))!==m.sources[n]))throw Error(`Stale index: ${target.section}; run a targeted rebuild`);
 }else if(sourcePath){
  const source=JSON.parse(fs.readFileSync(sourcePath));
  const digest=m.sourceNormalization===1?sourceTools.sourceDigestV1(source,target.scope):sourceTools.sourceDigest(source,target.scope);
  if(digest!==m.sourceDigest&&(m.sourceNormalization||sourceTools.legacySourceDigest(source,target.scope)!==m.sourceDigest))throw Error(`Stale index: ${target.section} ${target.version}; run a targeted rebuild`);
 }
 return m;
}
function dependencies(root){
 // Do not probe Node's module resolver before installation: Node caches missing
 // package metadata, which would make the first post-install import fail.
 if(['@huggingface/transformers','yaml','linkedom'].every(p=>fs.existsSync(new URL(`./node_modules/${p}/package.json`,import.meta.url))))return;
 const args=['ci','--prefix',path.join(root,'tools/semantic-search'),'--omit=dev','--no-audit','--no-fund'];
 // Invoke npm's JavaScript entry point on Windows rather than passing a path
 // through cmd.exe; this also handles workspace names containing spaces.
 const npmCLI=path.join(path.dirname(process.execPath),'node_modules/npm/bin/npm-cli.js');
 const result=process.platform==='win32'
  ?spawnSync(process.execPath,[npmCLI,...args],{stdio:'inherit'})
  :spawnSync('npm',args,{stdio:'inherit'});
 if(result.status!==0)throw Error('Could not install pinned semantic-index build dependencies');
}
async function runtime(root){
 const dir=path.join(root,'content/static/semantic-search'),file=path.join(dir,'runtime.json');
 let model=fs.existsSync(file)?JSON.parse(fs.readFileSync(file)):null;
 let missing=!model;
 for(const [name,digest] of Object.entries(model?.assets||{})){
  const file=path.join(dir,name);
  if(!fs.existsSync(file)){missing=true;continue;}
  if(hash(fs.readFileSync(file))!==digest)throw Error(`Corrupt shared runtime asset: ${name}`);
 }
 if(missing){dependencies(root);model=await (await import('./engine.mjs')).prepareRuntime(root);}
 return model;
}
function renderSource(root,project="core"){
 // Reuse the existing build's metadata/mount preparation, bypassing semantic
 // checks only for this intermediate export to avoid recursive generation.
 const relative=`tools/generated/semantic-render/${project}`,directory=path.join(root,relative);fs.mkdirSync(directory,{recursive:true});
 const local=spawnSync('hugo',['version'],{encoding:'utf8'}).status===0;
 let result;
 if(local&&process.platform!=='win32'){
  result=spawnSync('sh',[path.join(root,'tools/scripts/build-project.sh'),project,path.join(directory,'public')],{stdio:'inherit',env:{...process.env,OPENRIAK_SEMANTIC_EXPORT_ONLY:'1',OPENRIAK_DOCS_BUILD_PROFILE:process.env.OPENRIAK_DOCS_BUILD_PROFILE||'release',HUGO_GENERATED_CONFIG:path.join(directory,'hugo.yaml'),OPENRIAK_DOCS_DEVELOPMENT_DATA_ROOT:path.join(directory,'data'),GOMAXPROCS:'4',GOMEMLIMIT:'6GiB'}});
 }else{
  const version=fs.readFileSync(path.join(root,'.hugo-version'),'utf8').trim();
  result=spawnSync('docker',['run','--rm','--user',`${process.getuid?.()??1000}:${process.getgid?.()??1000}`,'-e','OPENRIAK_SEMANTIC_EXPORT_ONLY=1','-e',`OPENRIAK_DOCS_BUILD_PROFILE=${process.env.OPENRIAK_DOCS_BUILD_PROFILE||'release'}`,'-e',`HUGO_GENERATED_CONFIG=/project/${relative}/hugo.yaml`,'-e',`OPENRIAK_DOCS_DEVELOPMENT_DATA_ROOT=/project/${relative}/data`,'-e','GOMAXPROCS=4','-e','GOMEMLIMIT=6GiB','-v',`${root}:/project`,'--entrypoint','sh',`ghcr.io/gohugoio/hugo:v${version}`,'/project/tools/scripts/build-project.sh',project,`/project/${relative}/public`],{stdio:'inherit'});
 }
 if(result.status!==0)throw Error('Hugo semantic-source export failed');
 return path.join(directory,'public');
}
export function syncAssets(root,target,manifest,destination,{retain=false}={}){
 const source=path.join(root,target.directory),out=path.join(destination,target.publicPath);
 fs.mkdirSync(out,{recursive:true});
 const isGeneration=file=>/^(passages-[a-f0-9]{16}\.json|vectors-[a-f0-9]{16}\.bin)$/.test(file);
 const files=new Set(fs.readdirSync(source).filter(isGeneration));
 for(const file of files)fs.copyFileSync(path.join(source,file),path.join(out,file));
 fs.copyFileSync(path.join(source,'manifest.json'),path.join(out,'manifest.json.tmp'));
 fs.renameSync(path.join(out,'manifest.json.tmp'),path.join(out,'manifest.json'));
 // Publish source-retained generations too. Remove only generations that have
 // actually been cleaned from the source, unless retention is requested here.
 if(!retain)for(const file of fs.readdirSync(out))if(isGeneration(file)&&!files.has(file))fs.unlinkSync(path.join(out,file));
}

export async function run(root,options,hooks={}){
 const registry=JSON.parse(fs.readFileSync(path.join(root,'tools/semantic-search/indexes.json')));
 let site=options['site-dir']?path.resolve(options['site-dir']):null;
 let discovered;
 if(!site&&!hooks.runtime){
  const archive=options.section?.startsWith('archived-');
  site=renderSource(root,archive?'archives':'core');
  discovered=discoverTargets(site,registry).map(t=>({...t,exportPath:path.resolve(site,t.exportPath)}));
  if(options.all&&(process.env.OPENRIAK_DOCS_BUILD_PROFILE||'release')==='release'){
   const archiveSite=renderSource(root,'archives');
   discovered.push(...discoverTargets(archiveSite,registry).map(t=>({...t,exportPath:path.resolve(archiveSite,t.exportPath)})));
  }
 }
 const selected=selectTargets(discovered||(site&&!hooks.runtime?discoverTargets(site,registry):registry),options);
 const model=hooks.runtime?await hooks.runtime():await runtime(root);
 for(const target of selected){
  const missing=inspect(path.join(root,target.directory)).missing;
  let source=site&&target.exportPath?path.resolve(site,target.exportPath):null;
  if((!options.ensure||missing)&&target.kind==='hugo'&&!source){site=hooks.render?await hooks.render():renderSource(root);source=path.resolve(site,target.exportPath);}
  if(!options.ensure||missing){
   if(hooks.rebuild)await hooks.rebuild(target,source,options);
   else{dependencies(root);await (await import('./engine.mjs')).rebuild(root,target,source,{retain:options.retain});}
  }
  const m=validateIndex(root,target,model,source);
  console.log(`Validated ${target.section}${target.version?' '+target.version:''}: ${m.passages} passages.`);
  if(options['publish-dir'])syncAssets(root,target,m,path.resolve(options['publish-dir']),{retain:options.retain});
 }
 if(options['publish-dir'])fs.cpSync(path.join(root,'content/static/semantic-search'),path.join(path.resolve(options['publish-dir']),'semantic-search'),{recursive:true,dereference:true});
}
