import {highlightText,resultURL} from './highlight.mjs?v=20261105-highlighting2';
import {createSearch,mergeResults,createProgress} from './client.mjs?v=20261105-highlighting2';
export function mountSearch({root,input,status,results,manifestURL,textSearch,noun='pages',label=''}) {
 const ui=window.OpenRiakSearchStatus,prefs=window.OpenRiakSearchPreferences;
 // Keep the live status separate from the replaceable list, including when an
 // older cached template is upgraded by this runtime.
 let itemsRoot=results.querySelector('[data-search-items]');
 if(!itemsRoot){itemsRoot=document.createElement('div');itemsRoot.dataset.searchItems='';results.replaceChildren(status,itemsRoot);}
 else if(!results.contains(status))results.prepend(status);
 const section=prefs.section(manifestURL);let sequence=0,timer,state,semantic,previous;
 root.dataset.sharedSearchReady='true';root.dataset.semanticSearch='true';
 const count=items=>`${items.length} ${items.length===1?noun.replace(/s$/,''):noun} found.`;
 const enable=(event,changes)=>{
  event.preventDefault();event.stopPropagation();
  // The control is replaced when preferences change. Retain focus and the
  // open panel rather than treating this action as result-link navigation.
  input.focus({preventScroll:true});prefs.write(section,changes);results.hidden=false;
  if(input.value.trim().length<2){
   itemsRoot.replaceChildren();const prompt=document.createElement('p');prompt.textContent='Enter at least two characters to search.';itemsRoot.append(prompt);itemsRoot.hidden=false;
  }
 };
 const disabled=(type,row)=>{
  const node=status.querySelector(row===0?'[data-search-text-status]':'[data-search-semantic-status]');
  const link=document.createElement('button');link.type='button';link.className='search-enable';link.textContent=`Turn on ${type} search`;
  link.addEventListener('click',event=>enable(event,{[type]:true}));node.replaceChildren(link);node.removeAttribute('title');
 };
 const modes=options=>{
  if(!options.text)disabled('text',0);
  if(!options.semantic)disabled('semantic',1);
 };
 const choose=()=>{
  itemsRoot.replaceChildren();const p=document.createElement('p');p.textContent='Search is turned off for this site section. Choose a search type to enable it and search here.';itemsRoot.append(p);
  for(const [title,options] of [['Text + semantic search',{text:true,semantic:true}],['Text search',{text:true,semantic:false}],['Semantic search',{text:false,semantic:true}]]){
   const button=document.createElement('button');button.type='button';button.textContent=title;button.addEventListener('click',event=>enable(event,options));itemsRoot.append(button);
  }
  itemsRoot.hidden=false;results.hidden=false;
 };
 const render=items=>{
  itemsRoot.replaceChildren();
  for(const item of items){
   const a=document.createElement('a'),title=document.createElement('strong'),description=document.createElement('span');
   const query=state?.query||input.value.trim(),highlight=state?.options.highlight!==false;
   a.href=resultURL(item.url,query,highlight);
   highlightText(title,item.title,query,highlight);highlightText(description,item.description||item.text?.slice(0,220)||'',query,highlight);
   a.append(title,description);itemsRoot.append(a);
  }
  if(!items.length){const p=document.createElement('p');p.textContent='No matching results.';itemsRoot.append(p);}
  itemsRoot.hidden=false;results.hidden=false;
 };
 const update=()=>{
  if(!state)return;
  const {options,text,semantic:meaning,textDone,semanticDone,textFailed,semanticFailed}=state;
  const finished=(!options.text||textDone)&&(!options.semantic||semanticDone);
  let items=options.text&&options.semantic?mergeResults(text,meaning,p=>{const url=new URL(p.url,location.href);url.search='';return url.href;},30):options.text?text:meaning;
  if(options.timing==='asap'||finished)render(items);
  else {itemsRoot.hidden=true;results.hidden=false;}
  if(options.text&&!textFailed)ui.text(status,textDone?`Text search · ${count(text)}`:'Text search — finding matches…');
  if(options.semantic&&semanticDone&&!semanticFailed)ui.semantic(status,`Semantic search · ${count(meaning)}`);
  if(options.text&&options.semantic&&finished&&!textFailed&&!semanticFailed)ui.complete(status,count(items));
  modes(options);itemsRoot.setAttribute('aria-busy',String(!finished));
 };
 const progress=createProgress(status,()=>!!state?.options.semantic&&!state.semanticDone&&input.value.trim().length>=2);
 const search=()=>{
  clearTimeout(timer);const id=++sequence,query=input.value.trim(),options=prefs.read(section);
  if(previous?.semantic&&!options.semantic){semantic?.dispose();semantic=null;}
  previous=options;state=null;ui.clear(status);itemsRoot.setAttribute('aria-busy','false');modes(options);
  if(!options.text&&!options.semantic){choose();return;}
  if(query.length<2){itemsRoot.replaceChildren();results.hidden=true;return;}
  state={query,options,text:[],semantic:[],textDone:false,semanticDone:false,textFailed:false,semanticFailed:false};
  if(options.text)ui.text(status,'Text search — finding matches…');
  if(options.semantic)ui.semantic(status,'Semantic search — loading…');
  itemsRoot.replaceChildren();itemsRoot.hidden=true;results.hidden=false;itemsRoot.setAttribute('aria-busy','true');
  if(options.text)Promise.resolve().then(()=>textSearch(query)).then(items=>{
   if(id!==sequence)return;state.text=items.slice(0,30);state.textDone=true;update();
  }).catch(()=>{if(id!==sequence)return;state.textDone=true;state.textFailed=true;ui.text(status,'Text search unavailable.');update();});
  if(options.semantic){
   semantic ||= createSearch(manifestURL,progress);
   semantic(query,{text:false}).then(items=>{
    if(id!==sequence)return;state.semantic=items.map(p=>({...p,description:[label,p.heading,p.text.slice(0,220)].filter(Boolean).join(' · ')}));state.semanticDone=true;update();
   }).catch(error=>{
    if(id!==sequence||error.name==='AbortError')return;state.semanticDone=true;state.semanticFailed=true;ui.unavailable(status);update();
   });
  }
 };
 input.addEventListener('input',()=>{
  clearTimeout(timer);sequence++;state=null;itemsRoot.hidden=true;results.hidden=false;ui.clear(status);
  const options=prefs.read(section);
  if(options.text)ui.text(status,'Text search — waiting…');
  if(options.semantic)ui.semantic(status,'Semantic search — waiting…');
  modes(options);
  if(input.value.trim().length<2){itemsRoot.replaceChildren();results.hidden=true;ui.clear(status);modes(options);return;}
  timer=setTimeout(search,200);
 });
 input.addEventListener('click',()=>{if(!prefs.read(section).text&&!prefs.read(section).semantic)choose();else if(input.value.trim()||!prefs.read(section).text||!prefs.read(section).semantic)results.hidden=false;});
 input.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();event.stopPropagation();input.value='';search();results.hidden=true;}});
 document.addEventListener('click',event=>{if(!event.composedPath().includes(root))results.hidden=true;});
 const changed=event=>{const key='key' in event?event.key:event.detail?.key;if(key===null||key===prefs.key(section))search();};
 window.addEventListener('storage',changed);
 document.addEventListener('openriak:settings-changed',event=>{if(!('StorageEvent' in window))changed(event);});
 search();
 return {refresh:search};
}
