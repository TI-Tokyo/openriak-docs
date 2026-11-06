const vocabularies=new WeakMap();
const stopWords=new Set('a an the of to for in on and or is with how can i'.split(' '));
export function oneEditApart(a,b) {
 if(Math.abs(a.length-b.length)>1)return false;
 if(a.length===b.length){
  const mismatches=[];for(let i=0;i<a.length;i++)if(a[i]!==b[i])mismatches.push(i);
  return mismatches.length===1||(mismatches.length===2&&mismatches[1]===mismatches[0]+1&&a[mismatches[0]]===b[mismatches[1]]&&a[mismatches[1]]===b[mismatches[0]]);
 }
 if(a.length>b.length)[a,b]=[b,a];
 let i=0,j=0;while(i<a.length&&j<b.length){if(a[i]===b[j])i++;j++;if(j-i>1)return false;}return true;
}
// Suggest only familiar words from this section's titles/headings. Never alter
// identifiers, short words, or a word already present in the indexed content.
export function normaliseQuery(passages,query) {
 let vocabulary=vocabularies.get(passages);
 if(!vocabulary){
  const counts=new Map(),seen=new Set();
  for(const p of passages){const text=(p.title+' '+p.heading).toLowerCase();if(seen.has(text))continue;seen.add(text);
   for(const word of new Set(text.match(/\b[a-z]{5,}\b/g)||[]))counts.set(word,(counts.get(word)||0)+1);
  }
  vocabulary={counts,cache:new Map()};vocabularies.set(passages,vocabulary);
 }
 return query.replace(/[\p{L}\p{N}_-]+/gu,token=>{
  const term=token.toLowerCase();if(!/^[a-z]{5,}$/.test(term)||vocabulary.counts.has(term))return token;
  if(vocabulary.cache.has(term))return vocabulary.cache.get(term)||token;
  const candidates=[...vocabulary.counts].filter(([word,count])=>count>=2&&oneEditApart(term,word)).sort((a,b)=>b[1]-a[1]);
  let replacement='';
  if(candidates.length&&(!candidates[1]||candidates[0][1]>=2*candidates[1][1])&&!passages.some(p=>p.text.toLowerCase().includes(term)))replacement=candidates[0][0];
  if(vocabulary.cache.size>=200)vocabulary.cache.clear();vocabulary.cache.set(term,replacement);
  return replacement||token;
 });
}
// Shared by the browser and relevance tests. One result per article.
export function rank(passages, query, similarities=null, limit=8, {text:includeText=true}={}) {
 const corrected=normaliseQuery(passages,query);
 const queries=[query,...(corrected===query?[]:[corrected])];
 const tokens=q=>[...new Set(q.toLowerCase().match(/[\p{L}\p{N}_-]+/gu)||[])].filter(t=>!stopWords.has(t));
 const terms=tokens(query);
 if(!terms.length)return [];
 const lexical=includeText?passages.map((p,i)=>{
  const title=p.title.toLowerCase(),heading=p.heading.toLowerCase(),text=p.text.toLowerCase();
  const score=Math.max(...queries.map((q,variant)=>{
   const words=tokens(q),phrase=q.toLowerCase().trim();
   const hits=words.filter(t=>text.includes(t)||title.includes(t)||heading.includes(t)).length;
   let value=hits===words.length?10:0;
   for(const term of words)value+=(title.includes(term)?5:0)+(heading.includes(term)?3:0)+(text.includes(term)?1:0);
   if(title.includes(phrase))value+=30;
   if(text.includes(phrase)||heading.includes(phrase))value+=15;
   return value*(variant?0.85:1);
  }));
  return {i,score};
 }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.i-b.i):[];
 const scores=new Map();
 lexical.slice(0,60).forEach((x,r)=>scores.set(x.i,1/(20+r)));
 if(similarities) {
  similarities.map((score,i)=>({score,i})).filter(x=>x.score>=0.25).sort((a,b)=>b.score-a.score||a.i-b.i).slice(0,60)
   .forEach((x,r)=>scores.set(x.i,(scores.get(x.i)||0)+1/(20+r)));
 }
 const seen=new Set();
 return [...scores].sort((a,b)=>b[1]-a[1]||a[0]-b[0]).flatMap(([i])=>{
  const p=passages[i];if(seen.has(p.url))return [];seen.add(p.url);return [p];
 }).slice(0,limit);
}
export function cosineScores(vectors, query) {
 if(vectors.length%query.length!==0)throw Error('Invalid vector dimensions');
 const scores=[];
 for(let offset=0;offset<vectors.length;offset+=query.length){let dot=0;for(let j=0;j<query.length;j++)dot+=vectors[offset+j]*query[j];scores.push(dot);}
 return scores;
}
