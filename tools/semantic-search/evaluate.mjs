// Repeatable retrieval smoke test; scores alone do not establish relevance quality.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {pipeline,env} from '@huggingface/transformers';
import {rank,cosineScores} from '../../content/static/semantic-search/ranking.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const runtime=path.join(root,'content/static/semantic-search');
const base=process.argv.includes('--kv')?path.join(root,'content/static/semantic-indexes/openriak-kv/3.4.1'):path.join(root,'content/static/semantic-indexes/archived-technical-blog');
const manifest=JSON.parse(fs.readFileSync(path.join(base,'manifest.json')));
const passages=(manifest.indexParts||[manifest.index]).flatMap(file=>JSON.parse(fs.readFileSync(path.join(base,file))));
const bytes=Buffer.concat((manifest.vectorParts||[manifest.vectors]).map(file=>fs.readFileSync(path.join(base,file))));const vectors=new Float32Array(bytes.buffer,bytes.byteOffset,bytes.byteLength/4);
env.allowRemoteModels=false;env.localModelPath=runtime+'/';
const embed=await pipeline('feature-extraction',manifest.modelDirectory,{dtype:'q8',device:'cpu',session_options:{intraOpNumThreads:4,interOpNumThreads:1}});
const queries=['how to recover from a failed node','why do conflicting versions of data appear','how can I spread data across machines','n_val','sloppy quorum','vector clocks'];
const report=[];
for(const query of queries){const vector=await embed(query,{pooling:'mean',normalize:true});const results=rank(passages,query,cosineScores(vectors,vector.data),5);report.push({query,results:results.map(p=>({title:p.title,heading:p.heading,text:p.text,url:p.url}))});}
console.log(JSON.stringify({passages:passages.length,report},null,2));
