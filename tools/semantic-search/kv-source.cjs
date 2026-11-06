// Canonicalise rendered Hugo input so deployment hostname/base path do not affect it.
const {createHash}=require('node:crypto');
function rewriteSiteURLs(html,from,to=null){
 const base=new URL(from),target=to?new URL(to):null;
 const prefix=base.pathname.replace(/\/?$/,'/'),replacement=target?target.pathname.replace(/\/?$/,'/'):'/';
 const rewrite=value=>{
  if(value.startsWith(base.href))return (target?.href||'/')+value.slice(base.href.length);
  const protocolRelative='//'+base.host+prefix;
  if(value.startsWith(protocolRelative))return (target?'//'+target.host+replacement:'/')+value.slice(protocolRelative.length);
  // Archived product links sometimes retain a previous deployment prefix.
  // Their versioned route identifies the same documentation at any base path.
  if(!target&&!value.startsWith('//')){
   const product=value.match(/^\/(?:[^?#]*\/)?(openriak-(?:kv|cs|ts)\/\d+\.\d+\.\d+(?:[-+][\w.-]+)?(?:\/|[?#]|$).*)$/);
   if(product)return '/'+product[1];
  }
  if(value.startsWith(prefix)&&!value.startsWith('//'))return replacement+value.slice(prefix.length);
  return value;
 };
 // Match whole tags and attribute values without serialising HTML: changing its
 // quoting/whitespace would invalidate historical fingerprints. Absolute links
 // back to this site can also occur as text in generated download commands.
 const attributes=html.split(/(<[a-z][^>"']*(?:(?:"[^"]*"|'[^']*')[^>"']*)*>)/gi).map((part,index)=>index%2?part.replace(
  /(\s(?:href|src|action|poster|data-(?:(?:[\w-]+-)?(?:url|src|href)|copy-value))\s*=\s*)(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))/gi,
  (attribute,start,double,single,bare)=>{
   const value=double??single??bare,changed=rewrite(value);
   if(changed===value)return attribute;
   return start+(double!==undefined?'"'+changed+'"':single!==undefined?"'"+changed+"'":changed);
  }):part.split(base.href).join(target?.href||'/')).join('');
 // Archived pages also contain unrendered Markdown links after baseurl
 // shortcode expansion, sometimes inside malformed code blocks. In code, only
 // recognise links to product documentation, preserving ordinary literal paths.
 const markdown=(part,code)=>{
  const destination=url=>code&&!url.startsWith(prefix+'openriak-')?url:rewrite(url);
  return part.replace(/(\]\s*\(\s*)([^\s<)]+)/g,(_,lead,url)=>lead+destination(url))
   .replace(/((?:^|\n|<p>)\s*\[{1,2}[^\]\n]*\](?::|(?=[ \t]))[ \t]*)([^\s<]+)/g,(_,lead,url)=>lead+destination(url));
 };
 return attributes.split(/(<pre\b[\s\S]*?<\/pre>|<code\b[\s\S]*?<\/code>)/gi).map(part=>markdown(part,/^<(?:pre|code)\b/i.test(part))).join('');
}
function rebaseSource(source,baseURL){
 const from=new URL(source.baseURL),to=new URL(baseURL),prefix=from.pathname.replace(/\/?$/,'/');
 return {...source,baseURL:to.href,pages:source.pages.map(page=>{
  const url=new URL(page.url,from);
  if(url.origin!==from.origin||!url.pathname.startsWith(prefix))throw Error(`Page outside source deployment: ${page.url}`);
  return {...page,url:new URL(url.pathname.slice(prefix.length)+url.search+url.hash,to).href,html:rewriteSiteURLs(page.html,from.href,to.href)};
 })};
}
function pagesFor(source,scope,normaliseHighlighting,legacyURLs){
 const base=new URL(source.baseURL);
 const prefix=base.pathname.replace(/\/?$/,'/');
 return source.pages.map(page=>{
  const url=new URL(page.url,base);
  if(url.origin!==base.origin||!url.pathname.startsWith(prefix+scope))throw Error(`Page outside KV/configured scope: ${page.url}`);
  let html=(normaliseHighlighting?page.html.replace(/<span class="err">(\s*)<\/span>/g,'$1'):page.html).replace(/<(script|style|template)\b[^>]*>[\s\S]*?<\/\1>/gi,'');
  if(legacyURLs){
   html=html.split(base.href).join('/');
   if(prefix!=='/')html=html.split(prefix).join('/');
  }else html=rewriteSiteURLs(html,base.href);
  return {title:page.title,url:url.pathname.slice(prefix.length),html};
 }).sort((a,b)=>a.url.localeCompare(b.url));
}
const canonicalPages=(source,scope='openriak-kv/3.4.1/')=>pagesFor(source,scope,true,false);
const digest=pages=>createHash('sha256').update(JSON.stringify(pages)).digest('hex');
function presentationIndependent(pages){
 // Stylesheet injection depends on which output Hugo renders first. Ignore
 // presentation-only links/indentation, but retain code whitespace and structure.
 return pages.map(page=>({...page,html:page.html.split(/(<pre\b[\s\S]*?<\/pre>)/gi).map(part=>/^<pre\b/i.test(part)?part:part.replace(/<link\b[^>]*>/gi,'').replace(/>\s+</g,'> <').trim()).join('')}));
}
function sourceDigest(source,scope='openriak-kv/3.4.1/'){return digest(presentationIndependent(canonicalPages(source,scope)));}
// Diagnostic fingerprints use exactly the same input as the index fingerprint.
// They do not replace the full freshness check or affect existing indexes.
function sourcePageDigests(source,scope){
 return Object.fromEntries(presentationIndependent(canonicalPages(source,scope)).map(page=>[page.url,digest(page)]));
}
function sourceMismatchDetails(source,scope,manifest){
 const details=[`stored ${manifest.sourceDigest}, current ${sourceDigest(source,scope)} (normalisation ${manifest.sourceNormalization??'legacy'} -> 3)`];
 if(manifest.sourceNormalization===3&&manifest.sourcePageDigests){
  const before=manifest.sourcePageDigests,after=sourcePageDigests(source,scope);
  const changed=[...new Set([...Object.keys(before),...Object.keys(after)])].sort()
   .filter(url=>before[url]!==after[url])
   .map(url=>`${!Object.hasOwn(before,url)?'added':!Object.hasOwn(after,url)?'removed':'changed'} ${url}`);
  details.push(`page differences (${changed.length}): ${changed.slice(0,10).join(', ')}${changed.length>10?', …':''}`);
 }else details.push('page fingerprints unavailable; the next rebuild will record them');
 return details.join('; ');
}
function sourceDigestV2(source,scope='openriak-kv/3.4.1/'){return digest(presentationIndependent(pagesFor(source,scope,true,true)));}
function sourceDigestV1(source,scope='openriak-kv/3.4.1/'){return digest(pagesFor(source,scope,true,true));}
function legacySourceDigest(source,scope='openriak-kv/3.4.1/'){return digest(pagesFor(source,scope,false,true));}
function matchesSourceDigest(source,scope,manifest){
 if(manifest.sourceNormalization===3)return sourceDigest(source,scope)===manifest.sourceDigest;
 // Earlier fingerprints stripped the base path from external links too. Keep
 // their original rules, but compare in the verified original deployment so a
 // change of deployment does not change those historical fingerprints.
 const original=manifest.sourceBaseURL?rebaseSource(source,manifest.sourceBaseURL):source;
 if(manifest.sourceNormalization===2)return sourceDigestV2(original,scope)===manifest.sourceDigest;
 if(manifest.sourceNormalization===1)return sourceDigestV1(original,scope)===manifest.sourceDigest;
 if(manifest.sourceNormalization)throw Error(`Unsupported source normalisation: ${manifest.sourceNormalization}`);
 return [sourceDigestV2(original,scope),sourceDigestV1(original,scope),legacySourceDigest(original,scope)].includes(manifest.sourceDigest);
}
module.exports={canonicalPages,sourceDigest,sourcePageDigests,sourceMismatchDetails,sourceDigestV2,sourceDigestV1,legacySourceDigest,rebaseSource,matchesSourceDigest};
