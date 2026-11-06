export function queryTerms(query) {
 return [...new Map(String(query).trim().split(/\s+/).filter(term=>[...term].length>=2).slice(0,8).map(term=>[term.toLowerCase().slice(0,200),term.slice(0,200)])).values()].sort((a,b)=>b.length-a.length);
}
export function resultURL(value,query,enabled,base=location.href) {
 const url=new URL(value,base);url.searchParams.delete('highlight');
 if(enabled)for(const term of queryTerms(query))url.searchParams.append('highlight',term);
 return url.href;
}
export function highlightText(element,value,query,enabled=true) {
 const text=String(value??''),terms=enabled?queryTerms(query):[];
 element.replaceChildren();
 if(!terms.length){element.textContent=text;return;}
 const escaped=terms.map(term=>term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'));
 const parts=text.split(new RegExp(`(${escaped.join('|')})`,'gi'));
 parts.forEach((part,index)=>{
  if(index%2){const mark=element.ownerDocument.createElement('mark');mark.className='search-highlight';mark.textContent=part;element.append(mark);}
  else if(part)element.append(element.ownerDocument.createTextNode(part));
 });
}
