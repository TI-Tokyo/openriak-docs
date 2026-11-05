import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {parseArgs,selectTargets,run,inspect,validateIndex,syncAssets} from './manager.mjs';
import {hash,publishIndex} from './index-files.mjs';
const model={modelDirectory:'model-test',dimensions:2,dtype:'q8',runtime:'test'};
const targets=[{section:'archived-technical-blog',kind:'markdown',source:'content/blog',directory:'indexes/blog',publicPath:'blog-index',scope:'archived-technical-blog/'},{section:'openriak-kv',version:'3.4.0',kind:'hugo',directory:'indexes/kv1',publicPath:'kv1',scope:'openriak-kv/3.4.0/',exportPath:'openriak-kv/3.4.0/semantic-source.json'},{section:'openriak-kv',version:'3.4.1',kind:'hugo',directory:'indexes/kv2',publicPath:'kv2',scope:'openriak-kv/3.4.1/',exportPath:'openriak-kv/3.4.1/semantic-source.json'}];
function fixture(){
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'semantic-manager-'));fs.mkdirSync(path.join(root,'tools/semantic-search'),{recursive:true});fs.mkdirSync(path.join(root,'content/blog'),{recursive:true});fs.mkdirSync(path.join(root,'content/static/semantic-search'),{recursive:true});
 fs.writeFileSync(path.join(root,'tools/semantic-search/indexes.json'),JSON.stringify(targets));fs.writeFileSync(path.join(root,'content/blog/a.md'),'Article');
 return root;
}
const passage=(scope,text='First')=>({title:'Title',heading:'Heading',text,url:scope+'page/'});
const vectors=()=>[Buffer.from(new Float32Array([1,0]).buffer)];
function build(root,target,options={},text='First'){
 return publishIndex(path.join(root,target.directory),{...model,scope:target.scope,...(target.kind==='markdown'?{sources:{'a.md':hash(fs.readFileSync(path.join(root,target.source,'a.md')))}}:{})},[passage(target.scope,text)],vectors(),options);
}
test('CLI selectors require explicit versions or all and restrict section names',()=>{
 assert.equal(selectTargets(targets,parseArgs(['--all'])).length,3);
 assert.equal(selectTargets(targets,parseArgs(['--section','openriak-kv','--all'])).length,2);
 assert.equal(selectTargets(targets,parseArgs(['--section','archived-technical-blog','--all'])).length,1);
 const multiple=parseArgs(['--section','openriak-kv','--version','3.4.0','--version','3.4.1','--version','3.4.0']);
 assert.deepEqual(multiple.versions,['3.4.0','3.4.1']);
 assert.equal(selectTargets(targets,multiple).length,2);
 assert.equal(selectTargets(targets,parseArgs(['--section','openriak-kv','--version','3.4.1']))[0].version,'3.4.1');
 for(const section of ['openriak-kv','openriak-cs','openriak-ts','community','settings','archived-technical-blog','archived-mailing-list'])assert.equal(parseArgs(['--section',section,'--all']).section,section);
 for(const args of [[],['--section','openriak-kv'],['--section','homepage','--all'],['--section','unknown','--all'],['--version','3.4.0'],['--all','--version','3.4.0'],['--section'],['--all','--unknown'],['--section','settings','--version','3.4.0'],['--section','openriak-kv','--version','latest'],['--section','openriak-kv','--all','--version','3.4.0'],['--section','settings','--section','community','--all']])assert.throws(()=>parseArgs(args),args.join(' '));
 assert.throws(()=>selectTargets(targets,parseArgs(['--section','openriak-kv','--version','3.4.0','--version','9.9.9'])),/9.9.9/);
});
test('retain keeps old generations; normal publication removes only old index files',()=>{
 const root=fixture(),dir=path.join(root,targets[0].directory);const first=build(root,targets[0]);fs.writeFileSync(path.join(dir,'notes.txt'),'keep');
 const second=build(root,targets[0],{retain:true},'Second');assert.ok(fs.existsSync(path.join(dir,first.index)));
 const third=build(root,targets[0],{},'Third');assert.ok(!fs.existsSync(path.join(dir,first.index)));assert.ok(!fs.existsSync(path.join(dir,second.index)));assert.ok(fs.existsSync(path.join(dir,third.index)));assert.ok(fs.existsSync(path.join(dir,'notes.txt')));
});
test('failed generation preserves the previous manifest and assets',()=>{
 const root=fixture(),dir=path.join(root,targets[0].directory);const first=build(root,targets[0]);
 assert.throws(()=>publishIndex(dir,{...model,scope:'archived-technical-blog/'},[passage('blog/')],[Buffer.alloc(1)]));
 assert.equal(inspect(dir).manifest.index,first.index);assert.ok(fs.existsSync(path.join(dir,first.index)));
});
test('default builds missing indexes, skips valid files, repairs missing/corrupt assets, malformed manifests and stale content',async()=>{
 const root=fixture();let calls=0;
 const hooks={runtime:async()=>model,rebuild:async target=>{calls++;build(root,target);}};
 await run(root,{all:true,section:'archived-technical-blog'},hooks);assert.equal(calls,1);
 await run(root,{all:true,section:'archived-technical-blog'},hooks);assert.equal(calls,1);
 const dir=path.join(root,targets[0].directory);fs.unlinkSync(path.join(dir,inspect(dir).manifest.vectors));
 await run(root,{all:true,section:'archived-technical-blog'},hooks);assert.equal(calls,2);
 fs.appendFileSync(path.join(dir,inspect(dir).manifest.index),' ');
 await run(root,{all:true,section:'archived-technical-blog'},hooks);assert.equal(calls,3);
 fs.writeFileSync(path.join(dir,'manifest.json'),'{broken');
 await run(root,{all:true,section:'archived-technical-blog'},hooks);assert.equal(calls,4);
 fs.writeFileSync(path.join(root,'content/blog/a.md'),'Changed');
 await run(root,{all:true,section:'archived-technical-blog'},hooks);assert.equal(calls,5);
 const before=snapshot(root);
 await run(root,{all:true,section:'archived-technical-blog'},hooks);assert.equal(calls,5);
 assert.deepEqual(snapshot(root),before,'valid files keep their contents and timestamps');
});
test('all rebuilds every registered target and renders source only once',async()=>{
 const root=fixture();let renders=0;const built=[];
 // A fixture export digest is omitted here so validate with a known export.
 const source={baseURL:'https://example.test/',pages:[]};const site=path.join(root,'rendered');
 const {default:sourceTools}=await import('./kv-source.cjs');
 for(const t of targets.filter(t=>t.exportPath)){fs.mkdirSync(path.dirname(path.join(site,t.exportPath)),{recursive:true});fs.writeFileSync(path.join(site,t.exportPath),JSON.stringify(source));}
 await run(root,{all:true,retain:true},{runtime:async()=>model,render:async()=>{renders++;return site;},rebuild:async(t,sourcePath,o)=>{
  built.push(t.section+(t.version||''));assert.equal(o.retain,true);build(root,t,{retain:o.retain});
  if(sourcePath){const file=path.join(root,t.directory,'manifest.json'),m=JSON.parse(fs.readFileSync(file));m.sourceDigest=sourceTools.sourceDigest(source,t.scope);m.sourceNormalization=3;fs.writeFileSync(file,JSON.stringify(m));}
 }});
 assert.deepEqual(built,['archived-technical-blog','openriak-kv3.4.0','openriak-kv3.4.1']);assert.equal(renders,1);
 const before=snapshot(root);
 const repeated=await run(root,{all:true},{runtime:async()=>model,render:async()=>site,rebuild:()=>assert.fail('An unchanged second run must not rebuild')});
 assert.equal(repeated.needed,0);
 assert.deepEqual(snapshot(root),before);
});
test('source changes fail validation; publication includes a newly generated index',()=>{
 const root=fixture(),target=targets[0],m=build(root,target),out=path.join(root,'public');
 validateIndex(root,target,model);syncAssets(root,target,m,out);assert.ok(fs.existsSync(path.join(out,target.publicPath,m.vectors)));
 fs.writeFileSync(path.join(root,'content/blog/a.md'),'Changed');assert.throws(()=>validateIndex(root,target,model),/Stale/);
});

test('publishing an existing index preserves generations retained in the source',()=>{
 const root=fixture(),target=targets[0],out=path.join(root,'public');
 const first=build(root,target);syncAssets(root,target,first,out);
 const next=build(root,target,{retain:true},'Retained');syncAssets(root,target,next,out);
 assert.ok(fs.existsSync(path.join(out,target.publicPath,first.index)));
 const last=build(root,target,{},'Cleaned');syncAssets(root,target,last,out);
 assert.ok(!fs.existsSync(path.join(out,target.publicPath,first.index)));
 assert.ok(fs.existsSync(path.join(out,target.publicPath,last.index)));
});

test('whatif accepts force/retain, rejects publishing and explains retired flags',()=>{
 assert.equal(parseArgs(['--all','--whatif']).whatif,true);
 assert.equal(parseArgs(['--all','--whatif','--force','--retain']).force,true);
 assert.throws(()=>parseArgs(['--all','--whatif','--publish-dir','public']),/cannot be combined/);
 assert.throws(()=>parseArgs(['--all','--check']),/replaced by --whatif/);
 assert.throws(()=>parseArgs(['--all','--ensure']),/no longer needed/);
});
function snapshot(root){
 const files={};
 function walk(dir){for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
  const file=path.join(dir,entry.name);
  if(entry.isDirectory())walk(file);
  else files[path.relative(root,file)]={digest:hash(fs.readFileSync(file)),mtime:fs.statSync(file).mtimeMs};
 }}
 walk(root);return files;
}
async function checkFixture(){
 const root=fixture(),site=path.join(root,'rendered');
 const {default:sourceTools}=await import('./kv-source.cjs');
 const runtimeDir=path.join(root,'content/static/semantic-search');
 fs.writeFileSync(path.join(runtimeDir,'runtime.json'),JSON.stringify({...model,assets:{'model.bin':hash('model')}}));
 fs.writeFileSync(path.join(runtimeDir,'model.bin'),'model');
 for(const target of targets){
  build(root,target);
  const exportPath=target.exportPath||'blog/semantic-source.json';
  const source={baseURL:'https://example.test/',section:target.section,scope:target.scope,version:target.version||'',pages:[]};
  fs.mkdirSync(path.dirname(path.join(site,exportPath)),{recursive:true});
  fs.writeFileSync(path.join(site,exportPath),JSON.stringify(source));
  const file=path.join(root,target.directory,'manifest.json'),manifest=JSON.parse(fs.readFileSync(file));
  manifest.sourceDigest=sourceTools.sourceDigest(source,target.scope);manifest.sourceNormalization=3;fs.writeFileSync(file,JSON.stringify(manifest));
 }
 return {root,site};
}
test('whatif reports stale, corrupt and missing indexes, continues to valid ones, and writes nothing',async()=>{
 const {root,site}=await checkFixture();
 const extra={...targets[0],section:'other',scope:'other/',directory:'indexes/other'};
 fs.writeFileSync(path.join(root,'tools/semantic-search/indexes.json'),JSON.stringify([...targets,extra]));
 build(root,extra);
 // Change only blog source; use another source for the healthy fourth index.
 fs.mkdirSync(path.join(root,'content/other'));fs.writeFileSync(path.join(root,'content/other/a.md'),'Article');
 extra.source='content/other';
 fs.writeFileSync(path.join(root,'tools/semantic-search/indexes.json'),JSON.stringify([...targets,extra]));
 fs.writeFileSync(path.join(root,'content/blog/a.md'),'Changed');
 const dir=path.join(root,targets[1].directory);
 fs.appendFileSync(path.join(dir,inspect(dir).manifest.index),' ');
 fs.unlinkSync(path.join(root,targets[2].directory,'manifest.json'));
 const before=snapshot(root);
 const report=await run(root,{all:true,whatif:true,'site-dir':site},{runtime:async()=>model,rebuild:()=>assert.fail('check must not rebuild')});
 assert.equal(report.needed,3);assert.equal(report.results.length,4);
 assert.match(report.results[0].reason,/Stale/);assert.match(report.results[1].reason,/Corrupt/);assert.match(report.results[2].reason,/Missing/);assert.equal(report.results[3].ok,true);
 assert.deepEqual(snapshot(root),before);
});
test('whatif uses exported Hugo content and never repairs a missing runtime',async()=>{
 const {root,site}=await checkFixture();
 let report=await run(root,{all:true,whatif:true,'site-dir':site});
 assert.equal(report.needed,0);assert.equal(report.runtimeIssue,null);
 const file=path.join(site,targets[1].exportPath),source=JSON.parse(fs.readFileSync(file));
 source.pages=[{url:'/openriak-kv/3.4.0/page/',title:'Changed',html:'<p>New content.</p>'}];fs.writeFileSync(file,JSON.stringify(source));
 fs.unlinkSync(path.join(root,'content/static/semantic-search/model.bin'));
 const before=snapshot(root);
 report=await run(root,{all:true,whatif:true,'site-dir':site});
 assert.equal(report.needed,1);assert.match(report.runtimeIssue,/Missing shared/);
 assert.match(report.results.find(r=>r.target.version==='3.4.0').reason,/Stale/);
 assert.deepEqual(snapshot(root),before);
});

async function rebuildFixture(root,target,sourcePath,options={}){
 build(root,target,options);
 if(sourcePath){
  const {default:sourceTools}=await import('./kv-source.cjs');
  const file=path.join(root,target.directory,'manifest.json'),manifest=JSON.parse(fs.readFileSync(file));
  manifest.sourceDigest=sourceTools.sourceDigest(JSON.parse(fs.readFileSync(sourcePath)),target.scope);
  manifest.sourceNormalization=3;fs.writeFileSync(file,JSON.stringify(manifest));
 }
}
test('whatif force lists every selected valid index without changing files',async()=>{
 const {root,site}=await checkFixture(),before=snapshot(root);
 const options=parseArgs(['--all','--whatif','--force','--site-dir',site]);
 const report=await run(root,options,{runtime:async()=>model,rebuild:()=>assert.fail('whatif must not rebuild')});
 assert.equal(report.needed,3);assert.ok(report.results.every(result=>result.reason==='Forced by --force'));
 assert.deepEqual(snapshot(root),before);
});
test('force rebuilds only the requested versions even when valid',async()=>{
 const {root,site}=await checkFixture(),before=snapshot(root),rebuilt=[];
 const options=parseArgs(['--section','openriak-kv','--version','3.4.1','--force','--site-dir',site]);
 const report=await run(root,options,{runtime:async()=>model,rebuild:async(target,source,o)=>{
  rebuilt.push(target.version);await rebuildFixture(root,target,source,o);
 }});
 assert.deepEqual(rebuilt,['3.4.1']);assert.equal(report.needed,1);
 const after=snapshot(root);
 for(const [file,value] of Object.entries(before))if(!file.startsWith('indexes/kv2/'))assert.deepEqual(after[file],value,file);
});
test('multiple version selection updates stale content but leaves other valid indexes untouched',async()=>{
 const {root,site}=await checkFixture();
 const file=path.join(site,targets[1].exportPath),source=JSON.parse(fs.readFileSync(file));
 source.pages=[{title:'New',url:'/openriak-kv/3.4.0/new/',html:'<p>New content</p>'}];fs.writeFileSync(file,JSON.stringify(source));
 const before=snapshot(root),rebuilt=[];
 const options=parseArgs(['--section','openriak-kv','--version','3.4.0','--version','3.4.1','--site-dir',site]);
 const report=await run(root,options,{runtime:async()=>model,rebuild:async(target,source,o)=>{
  rebuilt.push(target.version);await rebuildFixture(root,target,source,o);
 }});
 assert.deepEqual(rebuilt,['3.4.0']);assert.equal(report.results.length,2);assert.equal(report.needed,1);
 const after=snapshot(root);
 for(const [file,value] of Object.entries(before))if(!file.startsWith('indexes/kv1/'))assert.deepEqual(after[file],value,file);
});
