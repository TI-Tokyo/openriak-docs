(() => {
 const sections=JSON.parse(document.getElementById('search-config')?.textContent||'[]');
 const key=id=>'openriak-docs-search:'+id;
 const valid=value=>value&&typeof value==='object'&&!Array.isArray(value)&&Object.entries(value).every(([k,v])=>k==='timing'?['asap','together'].includes(v):['text','semantic','highlight'].includes(k)&&typeof v==='boolean');
 const read=id=>{
  const defaults={text:true,semantic:true,highlight:true,timing:'asap',...sections.find(s=>s.id===id)?.defaults};
  try {const value=JSON.parse(localStorage.getItem(key(id))||'{}');return valid(value)?{...defaults,...value}:defaults;}catch{return defaults;}
 };
 const write=(id,changes)=>{
  if(!sections.some(s=>s.id===id)||!valid(changes))throw Error('Invalid search preference');
  const value=JSON.stringify({...read(id),...changes});
  window.OpenRiakSettings.write(key(id),value);
 };
 const section=manifest=>{
  const pathname=new URL(manifest,location.href).pathname;
  const match=pathname.match(/semantic-indexes\/([^/]+)/);
  return (match?.[1]||'archived-technical-blog').replace(/^riak-/,'openriak-');
 };
 window.OpenRiakSearchPreferences={sections,key,read,write,section};
})();
