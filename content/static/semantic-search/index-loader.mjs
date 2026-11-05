export async function loadPassages(manifest,indexBase,request=fetch){
 const pages=[];
 for(const file of manifest.indexParts||[manifest.index]){
  const response=await request(new URL(file,indexBase));if(!response.ok)throw Error('Search index unavailable');
  const part=await response.json();for(const page of part)pages.push(page);
 }
 if(pages.length!==manifest.passages)throw Error('Search index mismatch');
 return pages;
}
export async function loadVectors(manifest,indexBase,request=fetch){
 const vectors=new Float32Array(manifest.passages*manifest.dimensions);let offset=0;
 for(const file of manifest.vectorParts||[manifest.vectors]){
  const response=await request(new URL(file,indexBase));if(!response.ok)throw Error('Could not load search vectors');
  const part=new Float32Array(await response.arrayBuffer());
  if(offset+part.length>vectors.length)throw Error('Search index dimensions do not match');
  vectors.set(part,offset);offset+=part.length;
 }
 if(offset!==vectors.length)throw Error('Search index dimensions do not match');
 return vectors;
}
