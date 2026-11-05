import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {publishIndex} from './index-files.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const mime={'.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.wasm':'application/wasm','.html':'text/html','.css':'text/css','.png':'image/png','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{
 const inDocs=req.url.startsWith('/docs/');
 let url=new URL(req.url,'http://localhost').pathname.replace(/^\/docs\//,'/');
 if(url.endsWith('/'))url+='index.html';
 const name=decodeURIComponent(url).replace(/^\//,'');
 if(name.includes('..')){res.writeHead(400).end();return;}
 const roots=[...((name.startsWith('semantic-search/')||name.startsWith('semantic-indexes/'))?['content/static']:[]),inDocs?'tools/generated/blog-preview':'tools/generated/blog-preview-root','content/static/archived-technical-blog','content/static/common','layouts/common-docs/static','layouts/docs-theme/static'];
 const filename=roots.map(r=>path.join(root,r,name)).find(p=>fs.existsSync(p)&&fs.statSync(p).isFile());
 if(!filename){res.writeHead(404).end();return;}
 res.setHeader('Content-Type',mime[path.extname(filename)]||'application/octet-stream');fs.createReadStream(filename).pipe(res);
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin=`http://127.0.0.1:${server.address().port}`;
const browser=await chromium.launch({executablePath:process.env.OPENRIAK_BROWSER_EXECUTABLE,headless:true});
try{
 for(const prefix of ['/docs/','/']){
  const context=await browser.newContext();const page=await context.newPage();const errors=[];const external=[];
  page.on('pageerror',e=>{errors.push(e.message);console.log('PAGE ERROR',e.message);});
  page.on('console',m=>{if(['error','warning'].includes(m.type()))console.log('BROWSER',m.text());});
  page.on('requestfailed',r=>console.log('REQUEST FAILED',r.url(),r.failure()?.errorText));
  page.on('request',r=>{if(!r.url().startsWith(origin))external.push(r.url());});
  await page.goto(origin+prefix+'archived-technical-blog/');
  const input=page.locator('[data-search-input]'),status=page.locator('[data-search-status]');
  const began=Date.now();await input.fill('how to recover from a failed node');
  await page.waitForFunction(()=>document.querySelector('[data-search-status]').textContent.startsWith('Semantic + text search'),{},{timeout:60000});
  assert.ok((await status.boundingBox()).height>10,'Mode indicator must be visibly sized');
  assert.equal(await status.evaluate(e=>getComputedStyle(e).clip),'auto','Mode indicator must not be screen-reader-only');
  const links=page.locator('.search-results a');assert.ok(await links.count()>0);
  const href=await links.first().getAttribute('href');assert.ok(href.startsWith(origin+prefix+'archived-technical-blog/posts/'));
  console.log(prefix,await status.textContent(),`cold ${Date.now()-began}ms`,await links.first().innerText());
  const warm=Date.now();await input.fill('sloppy quorum');
  await page.waitForFunction(()=>document.querySelector('[data-search-status]').textContent.startsWith('Semantic + text search'),{},{timeout:30000});
  assert.match((await links.allInnerTexts()).join(' '),/quorum/i);console.log('Warm query:',Date.now()-warm,'ms');
  assert.equal(new Set(await links.evaluateAll(links=>links.map(l=>l.href))).size,await links.count());
  await input.press('Escape');await page.waitForTimeout(500);assert.equal(await page.locator('.search-results').isVisible(),false);assert.equal(await status.textContent(),'');
  assert.deepEqual(errors,[]);assert.deepEqual(external,[]);await context.close();
 }
 // Exercise multiple real vector/passage files through the browser worker.
 const source=path.join(root,'content/static/semantic-indexes/archived-technical-blog');
 const original=JSON.parse(fs.readFileSync(path.join(source,'manifest.json')));
 const all=JSON.parse(fs.readFileSync(path.join(source,original.index)));
 const bytes=fs.readFileSync(path.join(source,original.vectors));
 const selected=[];const seen=new Set();for(let i=0;i<all.length&&selected.length<6;i++)if(!seen.has(all[i].url)){seen.add(all[i].url);selected.push(i);}
 const directory=path.join(root,'tools/generated/semantic-render/browser-shards');
 const manifest=publishIndex(directory,original,selected.map(i=>all[i]),selected.map(i=>bytes.subarray(i*384*4,(i+1)*384*4)),{maxFileBytes:3072});
 assert.ok(manifest.vectorParts.length>1);
 const sharded=await browser.newContext();
 await sharded.route('**/semantic-indexes/archived-technical-blog/*',async route=>{
  const name=path.basename(new URL(route.request().url()).pathname);
  await route.fulfill({status:200,contentType:name.endsWith('.json')?'application/json':'application/octet-stream',body:fs.readFileSync(path.join(directory,name))});
 });
 const shardPage=await sharded.newPage();await shardPage.goto(origin+'/docs/archived-technical-blog/');await shardPage.locator('[data-search-input]').fill('distributed database');
 await shardPage.waitForFunction(()=>document.querySelector('[data-search-status]').textContent.startsWith('Semantic + text search'),{},{timeout:60000});
 assert.ok(await shardPage.locator('.search-results a').count()>0);console.log('PASS sharded index produces semantic results');await sharded.close();
 const context=await browser.newContext();await context.route('**/model_quantized.onnx',r=>r.abort());
 const page=await context.newPage();await page.goto(origin+'/docs/archived-technical-blog/');await page.locator('[data-search-input]').fill('vector clocks');
 await page.waitForFunction(()=>document.querySelector('[data-search-status]').textContent==='Text search only — semantic search unavailable.',{},{timeout:60000});
 assert.ok(await page.locator('.search-results a').count()>0);console.log('PASS model failure retains text results and explicit status');await context.close();
}finally{await browser.close();server.close();}
