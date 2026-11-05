import fs from 'node:fs';
import path from 'node:path';
// The export exists only for pages published by this Hugo build/profile.
export function discoverTargets(site, overrides=[]){
 const targets=[];
 function walk(dir){
  for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
   if(entry.isDirectory())walk(path.join(dir,entry.name));
   else if(entry.name==='semantic-source.json'){
    const file=path.join(dir,entry.name),source=JSON.parse(fs.readFileSync(file));
    if(!source.section)continue;
    if(!/^[a-z0-9-]+$/.test(source.section)||source.version&&!/^[a-zA-Z0-9._-]+$/.test(source.version))throw Error(`Invalid semantic scope: ${file}`);
    const expected=source.section==='homepage'?'':`${source.section}/${source.version?source.version+'/':''}`;
    if(['.','..'].includes(source.version)||source.scope!==expected)throw Error(`Invalid semantic scope: ${file}`);
    const override=overrides.find(t=>t.section===source.section&&(t.version||'')===(source.version||''));
    const publicPath=`semantic-indexes/${source.section}${source.version?'/'+source.version:''}`;
    targets.push({section:source.section,...(source.version?{version:source.version}:{}),kind:'hugo',directory:`content/static/${publicPath}`,publicPath,scope:source.scope,deduplicate:true,...override,exportPath:path.relative(site,file)});
   }
  }
 }
 walk(site);
 // A front-matter outputs override must not silently disable a version index.
 for(const product of ['openriak-kv','openriak-cs','openriak-ts','riak-kv','riak-cs','riak-ts']){
  const directory=path.join(site,product);if(!fs.existsSync(directory))continue;
  for(const entry of fs.readdirSync(directory,{withFileTypes:true})){
   if(!entry.isDirectory()||!/^\d+\.\d+\.\d+/.test(entry.name))continue;
   const html=path.join(directory,entry.name,'index.html');
   if(fs.existsSync(html)&&/data-product=/.test(fs.readFileSync(html,'utf8'))&&!targets.some(t=>t.scope===`${product}/${entry.name}/`))throw Error(`Missing semantic export for published version ${product}/${entry.name}`);
  }
 }
 if(!targets.length)throw Error(`No semantic source exports in ${site}; rebuild Hugo with the current templates`);
 return targets.sort((a,b)=>a.scope.localeCompare(b.scope));
}
