import {pipeline,env} from './transformers.min.js';
import {cosineScores} from './ranking.mjs?v=20261105-highlighting2';
import {download} from './download.mjs?v=20261105-highlighting2';
import {loadVectors} from './index-loader.mjs?v=20261105-highlighting2';
const assets=new URL('./',import.meta.url);
env.allowRemoteModels=false;
env.allowLocalModels=true;
env.localModelPath=assets.href;
env.backends.onnx.wasm.wasmPaths=assets.href;
// Works on ordinary static hosts without cross-origin isolation headers.
env.backends.onnx.wasm.numThreads=1;
env.backends.onnx.wasm.proxy=false;
let ready;let pending;let running=false;let activeID;
const progress=event=>self.postMessage({id:pending?.id||activeID,progress:event});
const nativeFetch=self.fetch.bind(self);
// Model and WASM downloads use the same bounded retry policy as the index.
self.fetch=async(url,options={})=>{
 const bytes=await download(url,{request:(target,extra)=>nativeFetch(target,{...options,...extra}),onProgress:e=>progress({phase:'Loading semantic model',...e})});
 return new Response(bytes,{headers:{'Content-Type':String(url).includes('.wasm')?'application/wasm':'application/octet-stream'}});
};
async function initialise(manifest,indexBase){
 const vectors=await loadVectors(manifest,indexBase||assets,nativeFetch,progress);
 progress({phase:'Preparing semantic model'});
 const extractor=await pipeline('feature-extraction',manifest.modelDirectory,{dtype:'q8',device:'wasm'});
 return {vectors,extractor};
}
self.onmessage=async({data})=>{
 pending=data;
 if(running)return;
 running=true;
 while(pending){
  const current=pending;pending=null;activeID=current.id;
  try {
   ready ||= initialise(current.manifest,current.indexBase);
   const {vectors,extractor}=await ready;
   // Loading is shared; once ready, prefer the newest queued query.
   if(pending)continue;
   progress({phase:'Running semantic search'});
   const result=await extractor(current.query,{pooling:'mean',normalize:true,truncation:true,max_length:256});
   self.postMessage({id:current.id,scores:cosineScores(vectors,result.data)});
  }catch(error){self.postMessage({id:current.id,error:String(error.message||error)});ready=null;}
 }
 running=false;
};
