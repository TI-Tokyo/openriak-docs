import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
const version='20261105-highlighting2';
const requests=[];
const server=http.createServer((req,res)=>{
 const url=new URL(req.url,'http://localhost');requests.push(url.pathname+url.search);
 res.setHeader('Cache-Control','max-age=3600');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end('<!doctype html><title>Cached search upgrade</title>');return;}
 const file=url.pathname.replace(/^\/docs\//,'');
 if(file.includes('..')){res.writeHead(400).end();return;}
 res.setHeader('Content-Type',file.endsWith('.mjs')||file.endsWith('.js')?'text/javascript':file.endsWith('.json')?'application/json':file.endsWith('.wasm')?'application/wasm':'application/octet-stream');
 if(!url.search&&file==='semantic-search/client.mjs'){res.end("import './index-loader.mjs';export const oldClient=true;");return;}
 if(!url.search&&file==='semantic-search/index-loader.mjs'){res.end("export function loadPassages(){throw Error('Stale loader reused');}");return;}
 const filename=path.join('content/static',file);
 if(!fs.existsSync(filename)){res.writeHead(404).end();return;}
 res.setHeader('Content-Length',fs.statSync(filename).size);fs.createReadStream(filename).pipe(res);
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const browser=await chromium.launch({executablePath:process.env.OPENRIAK_BROWSER_EXECUTABLE,headless:true});
try{
 const page=await browser.newPage();await page.goto(`http://127.0.0.1:${server.address().port}/`);
 await page.evaluate(()=>import('/docs/semantic-search/client.mjs'));
 await page.reload();
 const result=await page.evaluate(async version=>{
  const {createSearch}=await import('/docs/semantic-search/client.mjs?v='+version);
  const phases=[];const search=createSearch('/docs/semantic-indexes/settings/manifest.json',e=>phases.push(e.phase));
  const pages=await search('make text larger');return {phases,count:pages.length};
 },version);
 assert.ok(result.count>0);
 for(const phase of ['Loading search manifest','Loading search passages','Loading search vectors','Running semantic search'])assert.ok(result.phases.includes(phase),phase);
 assert.ok(requests.includes('/docs/semantic-search/index-loader.mjs?v='+version));
 assert.ok(requests.includes('/docs/semantic-search/search-worker.js?v='+version));
 console.log('PASS cached old client/loader bypassed; all download phases and semantic results received');
}finally{await browser.close();server.close();}
