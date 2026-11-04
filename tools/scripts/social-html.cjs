// Small head-only parser: values are decoded before comparison. Hugo emits quoted attributes.
const decode=s=>s.replace(/&(?:#(x[0-9a-f]+|[0-9]+)|([a-z]+));/gi,(all,num,name)=>num?String.fromCodePoint(num[0].toLowerCase()==='x'?parseInt(num.slice(1),16):+num):({amp:'&',quot:'"',apos:"'",lt:'<',gt:'>',nbsp:' '})[name]||all);
function parseHTML(html){
 const head=html.match(/<head\b[^>]*>([\s\S]*?)<\/head>/i)?.[1]||'';
 const meta=new Map(),canonical=[],titles=[...head.matchAll(/<title\b[^>]*>([\s\S]*?)<\/title>/gi)].map(m=>decode(m[1]));
 for(const m of head.matchAll(/<(meta|link)\b([^>]+)>/gi)) {
  const attrs={};for(const a of m[2].matchAll(/([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/g))attrs[a[1].toLowerCase()]=decode(a[2]??a[3]??a[4]);
  if(m[1].toLowerCase()==='link' && attrs.rel==='canonical')canonical.push(attrs.href);
  if(m[1].toLowerCase()==='meta') {const key=attrs.property||attrs.name;if(key){if(!meta.has(key))meta.set(key,[]);meta.get(key).push(attrs.content||'');}}
 }
 return {meta,canonical,titles};
}
module.exports={parseHTML};
