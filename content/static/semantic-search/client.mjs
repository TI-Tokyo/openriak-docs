import {watchWorker} from './worker-watch.mjs?v=20261105-highlighting2';
import {download} from './download.mjs?v=20261105-highlighting2';
import {loadPassages} from './index-loader.mjs?v=20261105-highlighting2';
import {rank,normaliseQuery} from './ranking.mjs?v=20261105-highlighting2';

// Adapter for section panels that retain their specialised text search.
export function createSearch(manifestURL,onProgress=()=>{}) {
 const url=new URL(manifestURL,location.href),indexBase=new URL('./',url);
 const siteBase=new URL('../',import.meta.url);
 const controller=new AbortController();
 const request=(url,options={})=>fetch(url,{...options,signal:AbortSignal.any([controller.signal,...(options.signal?[options.signal]:[])])});
 let ready,worker,watch,pending,sequence=0,failed,lastProgress,workerReady=false;
 const report=event=>{if(controller.signal.aborted)return;lastProgress=event;onProgress(event);};
 const fail=error=>{failed=error;watch?.stop();worker?.terminate();pending?.reject(error);pending=null;};
 const search=async (query,{text=true}={})=>{
  if(failed)throw failed;
  const id=++sequence;
  if(workerReady)report({phase:'Running semantic search',restart:true});
  else if(lastProgress)onProgress(lastProgress);
  pending?.reject(new DOMException('Superseded query','AbortError'));pending=null;
  ready ||= (async()=>{
   const manifest=await download(url,{request,json:true,onProgress:e=>report({phase:'Loading search manifest',...e})});
   report({phase:'Loading search passages'});
   const passages=await loadPassages(manifest,indexBase,request,report);
   worker=new Worker(new URL('./search-worker.js?v=20261105-highlighting2',import.meta.url),{type:'module'});
   watch=watchWorker(worker,fail);
   worker.onerror=()=>fail(Error('Semantic worker unavailable'));
   worker.onmessage=({data})=>{
    if(data.progress){report(data.progress);return;}
    if(data.id!==pending?.id)return;
    if(data.error){fail(Error(data.error));return;}
    watch.stop();workerReady=true;
    pending.resolve(rank(passages,pending.query,data.scores,30,{text:pending.text}).map(p=>({...p,url:new URL(p.url,siteBase).href})));
    pending=null;
   };
   return {manifest,passages};
  })().catch(error=>{fail(error);throw error;});
  const {manifest,passages}=await ready;
  if(id!==sequence)throw new DOMException('Superseded query','AbortError');
  if(failed)throw failed;
  return new Promise((resolve,reject)=>{
   pending={id,query,text,resolve,reject};watch.start();worker.postMessage({id,query:normaliseQuery(passages,query),manifest,indexBase:indexBase.href});
  });
 };
 search.dispose=()=>{controller.abort();fail(new DOMException('Search disabled','AbortError'));};
 return search;
}

// Reciprocal rank fusion retains exact text matches and adds semantic matches.
export function mergeResults(text,semantic,key,limit=30) {
 const entries=new Map();
 for(const list of [text,semantic])list.slice(0,60).forEach((item,i)=>{
  const id=key(item),old=entries.get(id);
  if(old)old.score+=1/(20+i);else entries.set(id,{item,score:1/(20+i)});
 });
 return [...entries.values()].sort((a,b)=>b.score-a.score).slice(0,limit).map(x=>x.item);
}

export {progressText,createProgress} from './download.mjs?v=20261105-highlighting2';
