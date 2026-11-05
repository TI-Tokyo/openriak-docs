import fs from 'node:fs';
import path from 'node:path';
import {pipeline,env} from '@huggingface/transformers';
import {parse as yaml} from 'yaml';
import {articleSections,makeSectionPassages} from './passages.mjs';
import {hash,publishIndex} from './index-files.mjs';
import sourceTools from './kv-source.cjs';

export async function prepareRuntime(root){
 const model=JSON.parse(fs.readFileSync(path.join(root,'tools/semantic-search/model.json')));
 const out=path.join(root,'content/static/semantic-search');fs.mkdirSync(out,{recursive:true});
 const modelFiles=['config.json','tokenizer.json','tokenizer_config.json','special_tokens_map.json','onnx/model_quantized.onnx'];
 for(const name of modelFiles){
  const dest=path.join(out,model.modelDirectory,name);fs.mkdirSync(path.dirname(dest),{recursive:true});
  if(!fs.existsSync(dest)){
   const response=await fetch(`https://huggingface.co/${model.model}/resolve/${model.revision}/${name}`);
   if(!response.ok)throw Error(`Model download failed: ${response.status} ${name}`);
   fs.writeFileSync(dest+'.tmp',Buffer.from(await response.arrayBuffer()));fs.renameSync(dest+'.tmp',dest);
  }
 }
 const dependencies=path.join(root,'tools/semantic-search/node_modules');
 const vendorFiles=['transformers.min.js','ort-wasm-simd-threaded.jsep.mjs','ort-wasm-simd-threaded.jsep.wasm'];
 for(const file of vendorFiles)fs.copyFileSync(path.join(dependencies,'@huggingface/transformers/dist',file),path.join(out,file));
 fs.copyFileSync(path.join(dependencies,'@huggingface/transformers/LICENSE'),path.join(out,'TRANSFORMERS-LICENSE'));
 fs.copyFileSync(path.join(out,'TRANSFORMERS-LICENSE'),path.join(out,'MODEL-LICENSE'));
 if(!fs.existsSync(path.join(out,'ONNX-RUNTIME-LICENSE'))){
  const commit=fs.readFileSync(path.join(dependencies,'onnxruntime-web/__commit.txt'),'utf8').trim();
  const response=await fetch(`https://raw.githubusercontent.com/microsoft/onnxruntime/${commit}/LICENSE`);
  if(!response.ok)throw Error('Could not retrieve ONNX Runtime licence');
  fs.writeFileSync(path.join(out,'ONNX-RUNTIME-LICENSE'),await response.text());
 }
 const assets=Object.fromEntries([...modelFiles.map(f=>model.modelDirectory+'/'+f),...vendorFiles].map(file=>[file,hash(fs.readFileSync(path.join(out,file)))]));
 const manifest={...model,assets};fs.writeFileSync(path.join(out,'runtime.json'),JSON.stringify(manifest,null,2)+'\n');
 return manifest;
}

let extractor;
export async function rebuild(root,target,sourcePath,{retain=false}={}){
 const runtime=path.join(root,'content/static/semantic-search');
 const model=JSON.parse(fs.readFileSync(path.join(runtime,'runtime.json')));
 env.allowRemoteModels=false;env.localModelPath=runtime+'/';
 extractor ||= await pipeline('feature-extraction',model.modelDirectory,{dtype:model.dtype,device:'cpu',session_options:{intraOpNumThreads:2,interOpNumThreads:1}});
 const pages=[],extra={};
 if(target.kind==='markdown'){
  extra.sources={};
  const directory=path.join(root,target.source);
  for(const name of fs.readdirSync(directory).filter(n=>n.endsWith('.md')).sort()){
   const raw=fs.readFileSync(path.join(directory,name),'utf8');extra.sources[name]=hash(raw);
   const match=raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);if(!match)throw Error(`Missing front matter: ${name}`);
   const metadata=yaml(match[1]);if(metadata.draft)continue;
   pages.push({title:metadata.title,date:String(metadata.date).slice(0,10),url:target.scope+'posts/'+name.slice(0,-3)+'/',body:raw.slice(match[0].length)});
  }
  extra.articles=pages.length;
 }else{
  const source=JSON.parse(fs.readFileSync(sourcePath));
  pages.push(...sourceTools.canonicalPages(source,target.scope).map(p=>({...p,body:p.html})));
  extra.sourceDigest=sourceTools.sourceDigest(source,target.scope);extra.sourceNormalization=3;extra.sourceBaseURL=source.baseURL;extra.pages=pages.length;
  extra.sourcePageDigests=sourceTools.sourcePageDigests(source,target.scope);
 }
 const passages=[];
 const preparation=path.join(root,'tools/generated/semantic-cache',model.revision,'passages');fs.mkdirSync(preparation,{recursive:true});
 const algorithm=hash(fs.readFileSync(new URL('./passages.mjs',import.meta.url)));
 for(const [i,page] of pages.entries()){
  if(i%50===0)console.log(`${target.section}: preparing page ${i+1}/${pages.length}`);
  const sections=articleSections(page.body,target.kind==='hugo');
  const prepared=path.join(preparation,hash(JSON.stringify([algorithm,page.title,sections,256]))+'.json');
  let chunks;
  if(fs.existsSync(prepared))chunks=JSON.parse(fs.readFileSync(prepared));
  else{
   chunks=makeSectionPassages(page.title,sections,text=>extractor.tokenizer.encode(text).length,256);
   for(const passage of chunks)if(extractor.tokenizer.encode(passage.input).length>256)throw Error(`Passage exceeds token limit: ${page.url}`);
   fs.writeFileSync(prepared,JSON.stringify(chunks));
  }
  for(const passage of chunks){
   passages.push({...Object.fromEntries(Object.entries(page).filter(([key])=>['title','date','url'].includes(key))),...passage});
  }
 }
 const cacheDir=path.join(root,'tools/generated/semantic-cache',model.revision);fs.mkdirSync(cacheDir,{recursive:true});
 const vectors=[];let computed=0;const began=performance.now();
 for(let i=0;i<passages.length;i++){
  const p=passages[i],cache=path.join(cacheDir,hash('q8-mean-normalized-v1\n'+p.input)+'.bin');let data;
  if(fs.existsSync(cache))data=fs.readFileSync(cache);
  else{const result=await extractor(p.input,{pooling:'mean',normalize:true});data=Buffer.from(result.data.buffer,result.data.byteOffset,result.data.byteLength);fs.writeFileSync(cache,data);computed++;}
  if(data.length!==model.dimensions*4)throw Error('Invalid cached embedding');vectors.push(data);delete p.input;
  if(i%1000===0)console.log(`${target.section}: embedded ${i+1}/${passages.length}`);
 }
 const {assets,...modelInfo}=model;
 const metadata={schema:1,...modelInfo,chunking:{strategy:'sentence-window',sentences:3,stride:1,version:1},scope:target.scope,...extra};
 const manifest=publishIndex(path.join(root,target.directory),metadata,passages,vectors,{retain,deduplicate:target.deduplicate});
 console.log(`${target.section}${target.version?' '+target.version:''}: ${manifest.passages} passages; ${computed} new embeddings in ${((performance.now()-began)/1000).toFixed(1)}s.`);
 return manifest;
}
