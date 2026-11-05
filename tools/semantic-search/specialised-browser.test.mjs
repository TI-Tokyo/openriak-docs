import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
let server;
let base=process.env.OPENRIAK_SEARCH_TEST_BASE||'http://localhost:1410/docs/';
if(process.env.OPENRIAK_SEARCH_STATIC_TEST){
 const roots=['tools/generated/semantic-render/panels','build/archives','content/static','content/static/archive-mailing-list','content/static/archived-technical-blog','content/static/common','layouts/common-docs/static','layouts/docs-theme/static'];
 server=http.createServer((req,res)=>{
  let name=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\/docs\//,'');
  if(name.includes('..')){res.writeHead(400).end();return;}
  if(name.endsWith('/'))name+='index.html';
  const activeRoots=name.startsWith('semantic-search/')||name.startsWith('semantic-indexes/')?['content/static',...roots]:roots;
  const file=activeRoots.map(root=>path.join(root,name)).find(file=>fs.existsSync(file)&&fs.statSync(file).isFile());
  if(!file){res.writeHead(404).end();return;}
  const type={'.js':'text/javascript','.mjs':'text/javascript','.html':'text/html','.json':'application/json','.wasm':'application/wasm','.css':'text/css'}[path.extname(file)]||'application/octet-stream';
  res.writeHead(200,{'Content-Type':type,'Content-Length':fs.statSync(file).size});fs.createReadStream(file).pipe(res);
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));base=`http://127.0.0.1:${server.address().port}/docs/`;
}
const browser=await chromium.launch({executablePath:process.env.OPENRIAK_BROWSER_EXECUTABLE,headless:true});
try {
 for(const [scope,inputSelector,statusSelector,resultsSelector,query] of [
  ['settings/','[data-settings-search]','[data-settings-search-status]','[data-settings-results]','make the text larger'],
  ['archived-mailing-list/','[data-mailing-list-search-input]','[data-mailing-list-search-status]','[data-mailing-list-search-results]','recover from a failed node']
 ]) {
  const context=await browser.newContext(),page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  let modelRequests=0,releaseModel;
  const modelGate=new Promise(resolve=>releaseModel=resolve);
  await context.route('**/model_quantized.onnx',async route=>{
    modelRequests++;
    if(modelRequests===1)return route.fulfill({status:503,body:'Temporary failure'});
    await modelGate;return route.continue();
  });
  await page.goto(base+scope);
  await page.evaluate(selector=>{
    window.searchProgress=[];
    new MutationObserver(()=>window.searchProgress.push(document.querySelector(selector).textContent)).observe(document.querySelector(selector),{childList:true,subtree:true,characterData:true});
  },statusSelector);
  await page.locator(inputSelector).fill(query);
  const initialHeight=(await page.locator(statusSelector).boundingBox()).height;
  assert.ok(await page.locator(statusSelector).evaluate(node=>node.closest('.search-results')!==null));
  await page.waitForFunction(selector=>document.querySelector(selector).textContent.includes('retry 1 of 2'),statusSelector,{timeout:180000});
  await page.locator(inputSelector).fill(query+' available');
  await page.waitForTimeout(1800);
  const before=await page.locator(statusSelector).textContent();
  assert.match(before,/Loading semantic model/,'new keystrokes must retain the active download stage');
  await page.waitForTimeout(1200);
  assert.notEqual(await page.locator(statusSelector).textContent(),before,'loading timer must continue after editing');
  assert.equal((await page.locator(statusSelector).boundingBox()).height,initialHeight);
  assert.match(await page.locator(statusSelector+' [data-search-text-status]').innerText(),/Text search/);
  assert.match(await page.locator(statusSelector+' [data-search-semantic-status]').innerText(),/semantic model/);
  releaseModel();
  await page.waitForFunction(selector=>document.querySelector(selector).textContent.startsWith('Semantic + text search'),statusSelector,{timeout:180000});
  assert.ok(await page.locator(resultsSelector+' a').count());
  assert.equal((await page.locator(statusSelector).boundingBox()).height,initialHeight);
  assert.equal(await page.locator(statusSelector+' [data-search-text-status]').innerText(),'Semantic + text search');
  assert.match(await page.locator(statusSelector+' [data-search-semantic-status]').innerText(),/\d+ (conversations|items) found\./);
  assert.equal(modelRequests,2,'transient model download must retry once');
  const progress=await page.evaluate(()=>window.searchProgress.join('\n'));
  assert.match(progress,/MiB/);assert.match(progress,/retry 1 of 2/);
  assert.ok((await page.locator(statusSelector).boundingBox()).height>0);
  for(const href of await page.locator(resultsSelector+' a').evaluateAll(a=>a.map(x=>x.href)))assert.ok(href.startsWith(base+scope),href);
  // Refocusing must not rerun a completed query or replace its result/status.
  const completed=await page.locator(statusSelector).textContent();
  const linksBefore=await page.locator(resultsSelector+' a').evaluateAll(a=>a.map(x=>x.href));
  await page.locator(inputSelector).blur();await page.locator(inputSelector).click();
  await page.waitForTimeout(400);
  assert.equal(await page.locator(statusSelector).textContent(),completed);
  assert.deepEqual(await page.locator(resultsSelector+' a').evaluateAll(a=>a.map(x=>x.href)),linksBefore);
  if(scope==='archived-mailing-list/'){
    await page.locator(inputSelector).fill('expand a clister');
    await page.waitForFunction(selector=>document.querySelector(selector).textContent.startsWith('Semantic + text search'),statusSelector,{timeout:30000});
    assert.match(await page.locator(resultsSelector).innerText(),/adding nodes to cluster/i);
  }
  await page.locator(inputSelector).fill('qu');await page.locator(inputSelector).fill('');await page.waitForTimeout(700);
  assert.equal((await page.locator(statusSelector).textContent()).trim(),'');
  assert.deepEqual(errors,[]);await context.close();
  const fallback=await browser.newContext();await fallback.route('**/semantic-indexes/**/manifest.json',r=>r.abort());
  const fp=await fallback.newPage();await fp.goto(base+scope);await fp.locator(inputSelector).fill(scope==='settings/'?'font':'quorum');
  await fp.waitForFunction(selector=>document.querySelector(selector).textContent.includes('Semantic search unavailable'),statusSelector,{timeout:30000});
  assert.ok(await fp.locator(resultsSelector+' a').count());await fallback.close();
  console.log('PASS',scope,'semantic mode, scoped results, clearing and original text fallback');
 }
} finally {await browser.close();server?.close();}
