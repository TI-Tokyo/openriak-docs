import {rank} from './ranking.mjs';
import {loadPassages} from './index-loader.mjs';
const root=document.querySelector('[data-sidebar-search]');
const input=root?.querySelector('[data-search-input]');
const results=root?.querySelector('[data-search-results]');
const status=root?.querySelector('[data-search-status]');
if(root&&input&&results&&status){
 root.dataset.sharedSearchReady='true';
 root.dataset.semanticSearch='true';
 const assets=new URL('./',import.meta.url);
 const siteBase=new URL('../',assets);
 const manifestURL=root.dataset.semanticIndexUrl?new URL(root.dataset.semanticIndexUrl,location.href):new URL('semantic-indexes/archived-technical-blog/manifest.json',siteBase);
 const indexBase=new URL('./',manifestURL);
 const label=root.dataset.semanticScopeLabel||'Archive';
 let indexPromise,worker,workerFailed=false,workerReady=false,sequence=0,timer;
 const load=()=>indexPromise ||= (async()=>{
  const response=await fetch(manifestURL);if(!response.ok)throw Error('Search manifest unavailable');
  const manifest=await response.json();
  const passages=await loadPassages(manifest,indexBase);
  return {manifest,passages};
 })().catch(error=>{indexPromise=null;throw error;});
 const render=(pages,semantic)=>{
  results.replaceChildren();
  for(const p of pages){
   const link=document.createElement('a'),title=document.createElement('strong'),description=document.createElement('span');
   link.href=new URL(p.url,siteBase).href;title.textContent=p.title;
   description.textContent=`${p.date?p.date+' · ':''}${label}${p.heading?' · '+p.heading:''} — ${p.text.slice(0,220)}${p.text.length>220?'…':''}`;
   link.append(title,description);results.append(link);
  }
  if(!pages.length)results.textContent=root.dataset.emptyMessage||'No matching pages.';
  results.hidden=false;results.setAttribute('aria-busy','false');
  const countLabel=`${pages.length} ${pages.length===1?'result':'results'}`;
  status.textContent=semantic?`Semantic + text search · ${countLabel}.`:workerFailed?'Text search only — semantic search unavailable.':`Text search — ${workerReady?'semantic search running':'semantic model loading'} · ${countLabel}.`;
 };
 const search=async(id,query)=>{
  try{
   const {manifest,passages}=await load();if(id!==sequence)return;
   render(rank(passages,query),false);
   if(workerFailed)return;
   if(!window.Worker){workerFailed=true;render(rank(passages,query),false);return;}
   if(!worker){
    worker=new Worker(new URL('./search-worker.js',import.meta.url),{type:'module'});
    worker.onerror=(event)=>{console.warn('Semantic search worker failed:',event.message);workerFailed=true;worker?.terminate();worker=null;status.textContent='Text search only — semantic search unavailable.';};
    worker.onmessage=({data})=>{
     if(data.id!==sequence)return;
     if(data.error){console.warn('Semantic search failed:',data.error);workerFailed=true;worker.terminate();worker=null;status.textContent='Text search only — semantic search unavailable.';return;}
     workerReady=true;
     render(rank(passages,input.value.trim(),data.scores),true);
    };
   }
   worker.postMessage({id,query,manifest,indexBase:indexBase.href});
  }catch(error){
   if(id!==sequence)return;
   results.setAttribute('aria-busy','false');status.textContent='Search is temporarily unavailable.';
  }
 };
 input.addEventListener('input',()=>{
  clearTimeout(timer);const id=++sequence;const query=input.value.trim();results.hidden=true;
  if(query.length<2){results.replaceChildren();results.setAttribute('aria-busy','false');status.textContent='';return;}
  results.setAttribute('aria-busy','true');status.textContent='Text search — finding matches…';
  timer=setTimeout(()=>search(id,query),250);
 });
 input.addEventListener('keydown',event=>{
  if(event.key==='Escape'){event.preventDefault();event.stopPropagation();clearTimeout(timer);sequence++;input.value='';results.replaceChildren();results.hidden=true;results.setAttribute('aria-busy','false');status.textContent='';}
 });
 input.addEventListener('click',()=>{if(results.childNodes.length)results.hidden=false;});
 document.addEventListener('click',event=>{if(!root.contains(event.target)){sequence++;results.hidden=true;}});
}
