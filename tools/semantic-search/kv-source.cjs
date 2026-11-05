// Canonicalise rendered Hugo input so deployment hostname/base path do not affect it.
const {createHash}=require('node:crypto');
function canonicalPages(source,scope='openriak-kv/3.4.1/',normaliseHighlighting=true){
 const base=new URL(source.baseURL);
 const prefix=base.pathname.replace(/\/?$/,'/');
 return source.pages.map(page=>{
  const url=new URL(page.url,base);
  if(url.origin!==base.origin||!url.pathname.startsWith(prefix+scope))throw Error(`Page outside KV/configured scope: ${page.url}`);
  let html=(normaliseHighlighting?page.html.replace(/<span class="err">(\s*)<\/span>/g,'$1'):page.html).replace(/<(script|style|template)\b[^>]*>[\s\S]*?<\/\1>/gi,'').split(base.href).join('/');
  if(prefix!=='/')html=html.split(prefix).join('/');
  return {title:page.title,url:url.pathname.slice(prefix.length),html};
 }).sort((a,b)=>a.url.localeCompare(b.url));
}
function sourceDigestV1(source,scope){return createHash('sha256').update(JSON.stringify(canonicalPages(source,scope))).digest('hex');}
function sourceDigest(source,scope='openriak-kv/3.4.1/'){
 // Stylesheet injection depends on which output Hugo renders first. Ignore
 // presentation-only links/indentation, but retain code whitespace and structure.
 const pages=canonicalPages(source,scope).map(page=>({...page,html:page.html.split(/(<pre\b[\s\S]*?<\/pre>)/gi).map(part=>/^<pre\b/i.test(part)?part:part.replace(/<link\b[^>]*>/gi,'').replace(/>\s+</g,'> <').trim()).join('')}));
 return createHash('sha256').update(JSON.stringify(pages)).digest('hex');
}
function legacySourceDigest(source,scope){return createHash('sha256').update(JSON.stringify(canonicalPages(source,scope,false))).digest('hex');}
module.exports={canonicalPages,sourceDigest,sourceDigestV1,legacySourceDigest};
