import {download} from './download.mjs?v=20261105-highlighting2';
export async function loadPassages(manifest,indexBase,request=fetch,onProgress=()=>{}){
 const pages=[],files=manifest.indexParts||[manifest.index];
 for(const [i,file] of files.entries()){
  const progress=e=>onProgress({phase:'Loading search passages',part:i+1,parts:files.length,...e});progress({});
  const part=await download(new URL(file,indexBase),{request,json:true,onProgress:progress});
  for(const page of part)pages.push(page);
 }
 if(pages.length!==manifest.passages)throw Error('Search index mismatch');
 return pages;
}
export async function loadVectors(manifest,indexBase,request=fetch,onProgress=()=>{}){
 const vectors=new Float32Array(manifest.passages*manifest.dimensions);let offset=0;
 const files=manifest.vectorParts||[manifest.vectors];
 for(const [i,file] of files.entries()){
  const progress=e=>onProgress({phase:'Loading search vectors',part:i+1,parts:files.length,...e});progress({});
  const part=new Float32Array(await download(new URL(file,indexBase),{request,onProgress:progress}));
  if(offset+part.length>vectors.length)throw Error('Search index dimensions do not match');
  vectors.set(part,offset);offset+=part.length;
 }
 if(offset!==vectors.length)throw Error('Search index dimensions do not match');
 return vectors;
}
