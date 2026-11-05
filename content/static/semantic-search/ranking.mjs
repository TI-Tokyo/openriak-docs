// Shared by the browser and relevance tests. One result per article.
export function rank(passages, query, similarities=null, limit=8) {
 const terms=[...new Set(query.toLowerCase().match(/[\p{L}\p{N}_-]+/gu)||[])];
 if(!terms.length)return [];
 const phrase=query.toLowerCase().trim();
 const lexical=passages.map((p,i)=>{
  const title=p.title.toLowerCase(),heading=p.heading.toLowerCase(),text=p.text.toLowerCase();
  const hits=terms.filter(t=>text.includes(t)||title.includes(t)||heading.includes(t)).length;
  let score=hits===terms.length?10:0;
  for(const term of terms)score+=(title.includes(term)?5:0)+(heading.includes(term)?3:0)+(text.includes(term)?1:0);
  if(title.includes(phrase))score+=30;
  if(text.includes(phrase)||heading.includes(phrase))score+=15;
  return {i,score};
 }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.i-b.i);
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
