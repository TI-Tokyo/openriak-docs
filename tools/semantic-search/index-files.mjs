import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
export const hash=value=>createHash('sha256').update(value).digest('hex');
export function uniqueIndices(passages){
 const seen=new Set(),indices=[];
 passages.forEach((p,i)=>{const key=JSON.stringify([p.url,p.title,p.heading,p.text]);if(!seen.has(key)){seen.add(key);indices.push(i);}});
 return indices;
}
export function cleanOldFiles(directory,manifest){
 for(const file of fs.readdirSync(directory)){
  if(/^(passages-[a-f0-9]{16}\.json|vectors-[a-f0-9]{16}\.bin)$/.test(file)&&!Object.hasOwn(manifest.assets,file))fs.unlinkSync(path.join(directory,file));
 }
}
export function publishIndex(out,metadata,passages,vectors,{retain=false,deduplicate=true,maxFileBytes=45*1024*1024}={}){
 if(passages.length!==vectors.length)throw Error('Passage/vector count mismatch');
 if(vectors.some(v=>v.length!==metadata.dimensions*4))throw Error('Invalid vector dimensions');
 if(passages.some(p=>!p.url.startsWith(metadata.scope)))throw Error('Passage outside index scope');
 const indices=deduplicate?uniqueIndices(passages):passages.map((_,i)=>i);
 const groups=[];let group=[],jsonBytes=2;
 for(const i of indices){
  const size=Buffer.byteLength(JSON.stringify(passages[i]));
  if(size+2>maxFileBytes||vectors[i].length>maxFileBytes)throw Error('One passage exceeds the index file size limit');
  if(group.length&&(jsonBytes+size+1>maxFileBytes||(group.length+1)*metadata.dimensions*4>maxFileBytes)){groups.push(group);group=[];jsonBytes=2;}
  jsonBytes+=size+(group.length?1:0);group.push(i);
 }
 if(group.length||!groups.length)groups.push(group);
 const manifest={...metadata,sourcePassages:passages.length,passages:indices.length,assets:{}};
 const indexParts=[],vectorParts=[];
 fs.mkdirSync(out,{recursive:true});
 for(const ids of groups){
  const entries=JSON.stringify(ids.map(i=>passages[i])),binary=Buffer.concat(ids.map(i=>vectors[i]));
  const index=`passages-${hash(entries).slice(0,16)}.json`,vectorFile=`vectors-${hash(binary).slice(0,16)}.bin`;
  indexParts.push(index);vectorParts.push(vectorFile);
  for(const [file,data] of [[index,entries],[vectorFile,binary]]){
   manifest.assets[file]=hash(data);
   const destination=path.join(out,file),temporary=destination+'.tmp';
   fs.writeFileSync(temporary,data);
   if(hash(fs.readFileSync(temporary))!==manifest.assets[file])throw Error('Written index failed integrity check');
   fs.renameSync(temporary,destination);
  }
 }
 manifest.index=indexParts[0];manifest.vectors=vectorParts[0];
 if(groups.length>1){manifest.indexParts=indexParts;manifest.vectorParts=vectorParts;}
 fs.writeFileSync(path.join(out,'manifest.json.tmp'),JSON.stringify(manifest,null,2)+'\n');
 fs.renameSync(path.join(out,'manifest.json.tmp'),path.join(out,'manifest.json'));
 if(!retain)cleanOldFiles(out,manifest);
 return manifest;
}
