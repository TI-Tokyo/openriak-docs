import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {parseArgs,selectTargets,run,inspect,validateIndex,syncAssets} from './manager.mjs';
import {hash,publishIndex} from './index-files.mjs';
const model={modelDirectory:'model-test',dimensions:2,dtype:'q8',runtime:'test'};
const targets=[{section:'blog',kind:'markdown',source:'content/blog',directory:'indexes/blog',publicPath:'blog-index',scope:'blog/'},{section:'kv',version:'1',kind:'hugo',directory:'indexes/kv1',publicPath:'kv1',scope:'kv/1/',exportPath:'kv/1/semantic-source.json'},{section:'kv',version:'2',kind:'hugo',directory:'indexes/kv2',publicPath:'kv2',scope:'kv/2/',exportPath:'kv/2/semantic-source.json'}];
function fixture(){
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'semantic-manager-'));fs.mkdirSync(path.join(root,'tools/semantic-search'),{recursive:true});fs.mkdirSync(path.join(root,'content/blog'),{recursive:true});fs.mkdirSync(path.join(root,'content/static/semantic-search'),{recursive:true});
 fs.writeFileSync(path.join(root,'tools/semantic-search/indexes.json'),JSON.stringify(targets));fs.writeFileSync(path.join(root,'content/blog/a.md'),'Article');
 return root;
}
const passage=(scope,text='First')=>({title:'Title',heading:'Heading',text,url:scope+'page/'});
const vectors=()=>[Buffer.from(new Float32Array([1,0]).buffer)];
function build(root,target,options={},text='First'){
 return publishIndex(path.join(root,target.directory),{...model,scope:target.scope,...(target.kind==='markdown'?{sources:{'a.md':hash('Article')}}:{})},[passage(target.scope,text)],vectors(),options);
}
test('CLI selection supports section, optional version and all; rejects ambiguous input',()=>{
 assert.equal(selectTargets(targets,parseArgs(['--all'])).length,3);
 assert.equal(selectTargets(targets,parseArgs(['--section','kv'])).length,2);
 assert.equal(selectTargets(targets,parseArgs(['--section','kv','--version','2']))[0].version,'2');
 for(const args of [[],['--all','--section','blog'],['--version','1'],['--section'],['--all','--unknown']])assert.throws(()=>parseArgs(args));
 assert.throws(()=>selectTargets(targets,{section:'unknown'}));
});
test('retain keeps old generations; normal publication removes only old index files',()=>{
 const root=fixture(),dir=path.join(root,targets[0].directory);const first=build(root,targets[0]);fs.writeFileSync(path.join(dir,'notes.txt'),'keep');
 const second=build(root,targets[0],{retain:true},'Second');assert.ok(fs.existsSync(path.join(dir,first.index)));
 const third=build(root,targets[0],{},'Third');assert.ok(!fs.existsSync(path.join(dir,first.index)));assert.ok(!fs.existsSync(path.join(dir,second.index)));assert.ok(fs.existsSync(path.join(dir,third.index)));assert.ok(fs.existsSync(path.join(dir,'notes.txt')));
});
test('failed generation preserves the previous manifest and assets',()=>{
 const root=fixture(),dir=path.join(root,targets[0].directory);const first=build(root,targets[0]);
 assert.throws(()=>publishIndex(dir,{...model,scope:'blog/'},[passage('blog/')],[Buffer.alloc(1)]));
 assert.equal(inspect(dir).manifest.index,first.index);assert.ok(fs.existsSync(path.join(dir,first.index)));
});
test('ensure builds missing indexes, reuses existing ones, and repairs a missing vector file',async()=>{
 const root=fixture();let calls=0;
 const hooks={runtime:async()=>model,rebuild:async target=>{calls++;build(root,target);}};
 await run(root,{ensure:true,section:'blog'},hooks);assert.equal(calls,1);
 await run(root,{ensure:true,section:'blog'},hooks);assert.equal(calls,1);
 const dir=path.join(root,targets[0].directory);fs.unlinkSync(path.join(dir,inspect(dir).manifest.vectors));
 await run(root,{ensure:true,section:'blog'},hooks);assert.equal(calls,2);
 fs.appendFileSync(path.join(dir,inspect(dir).manifest.index),' ');
 await assert.rejects(()=>run(root,{ensure:true,section:'blog'},hooks),/Corrupt/);assert.equal(calls,2);
});
test('all rebuilds every registered target and renders source only once',async()=>{
 const root=fixture();let renders=0;const built=[];
 // A fixture export digest is omitted here so validate with a known export.
 const source={baseURL:'https://example.test/',pages:[]};const site=path.join(root,'rendered');
 const {default:sourceTools}=await import('./kv-source.cjs');
 for(const t of targets.filter(t=>t.exportPath)){fs.mkdirSync(path.dirname(path.join(site,t.exportPath)),{recursive:true});fs.writeFileSync(path.join(site,t.exportPath),JSON.stringify(source));}
 await run(root,{all:true,retain:true},{runtime:async()=>model,render:async()=>{renders++;return site;},rebuild:async(t,sourcePath,o)=>{
  built.push(t.section+(t.version||''));assert.equal(o.retain,true);build(root,t,{retain:o.retain});
  if(sourcePath){const file=path.join(root,t.directory,'manifest.json'),m=JSON.parse(fs.readFileSync(file));m.sourceDigest=sourceTools.sourceDigest(source,t.scope);fs.writeFileSync(file,JSON.stringify(m));}
 }});
 assert.deepEqual(built,['blog','kv1','kv2']);assert.equal(renders,1);
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
