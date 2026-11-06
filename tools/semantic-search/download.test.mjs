import {test} from 'node:test';
import assert from 'node:assert/strict';
import {download} from '../../content/static/semantic-search/download.mjs';
import {mergeResults} from '../../content/static/semantic-search/client.mjs';
test('network errors and transient HTTP failures retry, with visible progress',async()=>{
 let attempts=0;const events=[];
 const bytes=await download('https://example.test/index',{request:async()=>{
  attempts++;if(attempts===1)throw TypeError('Network failure');
  if(attempts===2)return new Response('',{status:503});
  return new Response('complete',{headers:{'content-length':'8'}});
 },delay:async()=>{},onProgress:e=>events.push(e)});
 assert.equal(new TextDecoder().decode(bytes),'complete');assert.equal(attempts,3);
 assert.deepEqual(events.filter(e=>e.retry).map(e=>e.retry),[1,2]);assert.equal(events.at(-1).loaded,8);
});
test('404 is not retried and repeated server failures stop after three attempts',async()=>{
 for(const [status,expected] of [[404,1],[403,1],[429,3],[500,3]]){
  let attempts=0;
  await assert.rejects(download('https://example.test/missing',{request:async()=>{attempts++;return new Response('',{status});},delay:async()=>{}}));
  assert.equal(attempts,expected);
 }
});
test('interrupted response bodies are retried from the start',async()=>{
 let attempts=0;
 const data=await download('https://example.test/index',{request:async()=>++attempts===1?new Response(new ReadableStream({start(c){c.error(TypeError('Disconnected'));}})):new Response('ok'),delay:async()=>{}});
 assert.equal(new TextDecoder().decode(data),'ok');assert.equal(attempts,2);
});
test('specialised exact results and semantic results merge without duplicates',()=>{
 const a={url:'a'},b={url:'b'},c={url:'c'};
 assert.deepEqual(mergeResults([a,b],[b,c],x=>x.url),[b,a,c]);
});
