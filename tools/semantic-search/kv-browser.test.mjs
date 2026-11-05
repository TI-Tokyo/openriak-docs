import {chromium} from 'playwright';
import assert from 'node:assert/strict';
const base=(process.env.OPENRIAK_KV_TEST_BASE||'http://localhost:1410/docs/').replace(/\/?$/,'/');
const browser=await chromium.launch({executablePath:process.env.OPENRIAK_BROWSER_EXECUTABLE,headless:true});
try{
 const context=await browser.newContext();const page=await context.newPage();const errors=[],external=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('request',r=>{if(new URL(r.url()).origin!==new URL(base).origin)external.push(r.url());});
 let manifest;
 page.on('response',async r=>{if(r.url().endsWith('/semantic-indexes/openriak-kv/3.4.1/manifest.json'))manifest=await r.json();});
 for(const route of ['openriak-kv/3.4.1/','openriak-kv/3.4.1/foundations/overview/what-openriak-kv-is/']){
  await page.goto(base+route);
  const root=page.locator('[data-sidebar-search]');assert.match(await root.getAttribute('data-semantic-index-url'),/semantic-indexes\/openriak-kv\/3\.4\.1\/manifest.json/);
  const input=root.locator('[data-search-input]'),status=root.locator('[data-search-status]');
  const began=Date.now();await input.fill('sloppy quorum');
  await page.waitForFunction(()=>document.querySelector('[data-search-status]').textContent.startsWith('Semantic + text search'),{},{timeout:120000});
  assert.equal(manifest.scope,'openriak-kv/3.4.1/');
  assert.ok((await status.boundingBox()).height>10);assert.equal(await status.evaluate(e=>getComputedStyle(e).clip),'auto');
  const links=root.locator('.search-results a');assert.ok(await links.count()>0);
  for(const href of await links.evaluateAll(a=>a.map(x=>x.href)))assert.ok(href.startsWith(base+'openriak-kv/3.4.1/'),href);
  const texts=(await links.allInnerTexts()).join(' ');assert.match(texts,/OpenRiak KV 3\.4\.1/);assert.doesNotMatch(texts,/ · Archive/);
  console.log(route,await status.innerText(),Date.now()-began,'ms');console.log(await links.first().innerText());
  await input.fill('n_val');await page.waitForFunction(()=>document.querySelector('[data-search-status]').textContent.startsWith('Semantic + text search'),{},{timeout:30000});
  assert.match((await links.allInnerTexts()).join(' '),/n_val/i);
  await input.press('Escape');assert.equal((await status.textContent()).trim(),'');assert.equal(await root.locator('.search-results').isVisible(),false);
 }
 await page.goto(base+'openriak-kv/3.4.0/');assert.match(await page.locator('[data-sidebar-search]').getAttribute('data-semantic-index-url'),/semantic-indexes\/openriak-kv\/3\.4\.0\/manifest.json/);
 assert.equal(await page.locator('script[src*="semantic-search/search.js"]').count(),1);
 for(const scope of ['openriak-kv/3.4.0/','openriak-kv/3.2.5/','openriak-cs/3.0.1/','openriak-ts/3.0.0/','community/']){
  await page.goto(base+scope);
  await page.locator('[data-search-input]').fill('distributed database');
  await page.waitForFunction(()=>document.querySelector('[data-search-status]').textContent.startsWith('Semantic + text search'),{},{timeout:120000});
  const links=await page.locator('.search-results a').evaluateAll(nodes=>nodes.map(n=>n.href));
  assert.ok(links.length>0,scope);
  assert.ok(links.every(url=>url.startsWith(base+scope)),scope);
  console.log(scope,await page.locator('[data-search-status]').textContent());
 }
 assert.deepEqual(errors,[]);assert.deepEqual(external,[]);await context.close();
 const fallback=await browser.newContext();await fallback.route('**/model_quantized.onnx',r=>r.abort());
 const p=await fallback.newPage();await p.goto(base+'openriak-kv/3.4.1/');await p.locator('[data-search-input]').fill('n_val');
 await p.waitForFunction(()=>document.querySelector('[data-search-status]').textContent.includes('Semantic search unavailable'),{},{timeout:120000});
 assert.ok(await p.locator('.search-results a').count()>0);await fallback.close();
 console.log('PASS version scoping, inherited pages, visible mode, exact terms, model fallback and 3.4.0 enabled');
}finally{await browser.close();}
