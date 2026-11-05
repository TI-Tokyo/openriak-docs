import {parseHTML} from 'linkedom';
import {marked} from '../scripts/vendor/marked/marked-18.1.1.mjs';

const clean=text=>text.replace(/\s+/g,' ').trim();
const segmenter=new Intl.Segmenter('en-GB',{granularity:'sentence'});

// Protect technical literals before sentence segmentation, then restore them.
export function sentences(text){
 const literals=[];
 const protectedText=text.replace(/`[^`]+`|https?:\/\/[^\s]+|\b(?:e\.g\.|i\.e\.|etc\.|Mr\.|Mrs\.|Dr\.|vs\.)|\b\d+(?:\.\d+)+\b/g,value=>{
  let suffix='';if(/^https?:/.test(value)&&/[.!?]$/.test(value)){suffix=value.slice(-1);value=value.slice(0,-1);}
  return `\uE000${literals.push(value)-1}\uE001${suffix}`;
 });
 return [...segmenter.segment(protectedText)].map(({segment})=>clean(segment.replace(/\uE000(\d+)\uE001/g,(_,i)=>literals[Number(i)]))).filter(Boolean);
}

export function articleSections(markdown,html=false){
 const {document}=parseHTML('<html><body>'+(html?markdown:marked.parse(markdown))+'</body></html>');
 document.querySelectorAll('script,style,template,nav,img,button,[role=tablist],.doc-code-copy,.doc-code-header').forEach(node=>node.remove());
 // Preserve inline commands as indivisible sentence-segmentation literals.
 document.querySelectorAll('code').forEach(node=>{if(node.parentElement?.tagName!=='PRE')node.textContent='`'+node.textContent+'`';});
 const sections=[];let heading='',blocks=[];
 const flush=()=>{if(blocks.length)sections.push({heading,blocks});blocks=[];};
 const walk=node=>{
  if(/^H[1-6]$/.test(node.tagName)){flush();heading=clean(node.textContent);return;}
  if(['PRE','UL','OL','TABLE'].includes(node.tagName)){
   const selector=node.tagName==='PRE'?null:node.tagName==='TABLE'?'tr':'li';
   const units=selector?[...node.querySelectorAll(selector)].map(n=>clean(n.textContent)):node.textContent.split('\n').map(clean);
   blocks.push({kind:node.tagName==='PRE'?'code':'list',units:units.filter(Boolean)});return;
  }
  if(['DIV','SECTION','ARTICLE','BLOCKQUOTE','DETAILS'].includes(node.tagName)){for(const child of node.childNodes)if(child.nodeType===1||child.nodeType===3)walk(child);return;}
  const text=clean(node.textContent);if(text)blocks.push({kind:'prose',units:sentences(text)});
 };
 for(const node of document.body.children)walk(node);
 flush();return sections;
}

// Split oversized units without dropping the tail or silently truncating input.
function fitUnits(units,prefix,count,maxTokens){
 const chunks=[];let current='';
 const emit=()=>{if(current)chunks.push(current);current='';};
 for(let unit of units){
  if(unit.length<=4096&&count(prefix+(current?current+' ':'')+unit)<=maxTokens){current+=(current?' ':'')+unit;continue;}
  emit();
  while(unit&&(unit.length>4096||count(prefix+unit)>maxTokens)){
   let low=1,high=Math.min(unit.length,4096),size=0;
   while(low<=high){const mid=(low+high)>>1;if(count(prefix+unit.slice(0,mid))<=maxTokens){size=mid;low=mid+1;}else high=mid-1;}
   if(!size)throw Error('No token budget remains for passage text');
   const boundary=unit.lastIndexOf(' ',size);
   if(boundary>size/2)size=boundary;
   chunks.push(unit.slice(0,size).trim());unit=unit.slice(size).trim();
  }
  current=unit;
 }
 emit();return chunks;
}

export function makePassages(title,markdown,count,maxTokens=256,html=false){
 return makeSectionPassages(title,articleSections(markdown,html),count,maxTokens);
}
export function makeSectionPassages(title,sections,count,maxTokens=256){
 const output=[];
 for(const section of sections){
  // Keep most of the budget for the body, even with unusually long headings.
  const shorten=(text,budget)=>{let value=clean(text);while(value&&count(value)>budget)value=value.slice(0,Math.max(0,value.length-8)).trim();return value;};
  const prefix=shorten(title,48)+'\n'+shorten(section.heading,40)+'\n';
  const append=(units,kind)=>{
   for(const text of fitUnits(units,prefix,count,maxTokens)){
    const input=prefix+text;
    output.push({heading:section.heading,text,input,kind});
   }
  };
  let prose=[];let context='';
  const flush=()=>{
   if(!prose.length)return;
   for(let start=0;start<Math.max(1,prose.length-2);start++)append(prose.slice(start,start+3),'prose');
   context=prose.at(-1);prose=[];
  };
  for(const block of section.blocks){
   if(block.kind==='prose')prose.push(...block.units);
   else {flush();append([...(context?[context]:[]),...block.units],block.kind);context='';}
  }
  flush();
 }
 return output;
}
