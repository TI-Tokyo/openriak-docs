import {pipeline,env} from './transformers.min.js';
import {cosineScores} from './ranking.mjs';
import {loadVectors} from './index-loader.mjs';
const assets=new URL('./',import.meta.url);
env.allowRemoteModels=false;
env.allowLocalModels=true;
env.localModelPath=assets.href;
env.backends.onnx.wasm.wasmPaths=assets.href;
// Works on ordinary static hosts without cross-origin isolation headers.
env.backends.onnx.wasm.numThreads=1;
env.backends.onnx.wasm.proxy=false;
let ready;let pending;let running=false;
async function initialise(manifest,indexBase){
 const vectors=await loadVectors(manifest,indexBase||assets);
 const extractor=await pipeline('feature-extraction',manifest.modelDirectory,{dtype:'q8',device:'wasm'});
 return {vectors,extractor};
}
self.onmessage=async({data})=>{
 pending=data;
 if(running)return;
 running=true;
 while(pending){
  const current=pending;pending=null;
  try {
   ready ||= initialise(current.manifest,current.indexBase);
   const {vectors,extractor}=await ready;
   const result=await extractor(current.query,{pooling:'mean',normalize:true,truncation:true,max_length:256});
   self.postMessage({id:current.id,scores:cosineScores(vectors,result.data)});
  }catch(error){self.postMessage({id:current.id,error:String(error.message||error)});ready=null;}
 }
 running=false;
};
