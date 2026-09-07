const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const pathModule=require('node:path');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.OPENRIAK_BROWSER_EXECUTABLE || undefined,headless:true});
 try {
  const context=await browser.newContext({permissions:['clipboard-read','clipboard-write']});
  await context.addInitScript(()=>localStorage.setItem('openriak-docs-code-language','java'));
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/metadata/*.json',async route=>{await new Promise(r=>setTimeout(r,150));await route.continue();});
  const base=process.env.OPENRIAK_SEARCH_TEST_BASE || 'http://localhost:1410/docs/openriak-kv/3.4.0/';
  for(const path of ['reference/data/buckets-and-bucket-types/','reference/commands/riak-control/']) {
   await page.goto(base+path+'?highlight=bob');
   await page.locator('.search-highlight-clear').waitFor();
   const marks=page.locator('mark.search-highlight');
   assert.ok(await marks.count()>0);
   const first=marks.first();assert.equal(await first.isVisible(),true);
   assert.equal((await first.textContent()).toLowerCase(),'bob');
   assert.equal(await page.evaluate(()=>localStorage.getItem('openriak-docs-code-language')),'java');
   const block=first.locator('xpath=ancestor::*[@data-code-block][1]');
   assert.equal(await block.isVisible(),true);
   if(path.includes('buckets'))assert.equal(await block.getAttribute('data-code-language'),'csharp');
   const source=await block.locator('[data-code-source]').evaluate(e=>OpenRiakMetadata.read(e));
   const tabGroup=block.locator('xpath=ancestor::*[contains(@class,"doc-code-tabs")][1]');
   const copy=await tabGroup.count()?tabGroup.locator('[data-code-copy]:visible'):block.locator('[data-code-copy]');
   await copy.click();assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),source);
   await page.locator('.search-highlight-clear').click();
   assert.equal(await marks.count(),0);assert.ok(!page.url().includes('highlight='));
   console.log('PASS visible code match, preference preserved, exact copy, clear:',path);
  }
  await page.goto(base+'reference/data/buckets-and-bucket-types/');
  await page.evaluate(()=>window.OpenRiakPageToolsReady);
  assert.equal(await page.locator('.search-highlight-clear').count(),0);
  for(const group of await page.locator('.doc-code-tabs').all()) {
   if(await group.getByRole('tab',{name:'Java',exact:true}).count())assert.equal(await group.locator('[role="tab"][aria-selected="true"]').textContent(),'Java');
  }
  // Archive-style pages have no code controls or readiness promise.
  await page.goto(base+'reference/commands/riak-control/?highlight=bob');
  await page.locator('.search-highlight-clear').waitFor();
  await page.setContent('<main data-search-highlight-root><details><summary>Example</summary><p>Bob in a disclosure</p></details></main>');
  await page.evaluate(()=>delete window.OpenRiakPageToolsReady);
  await page.addScriptTag({content:fs.readFileSync(pathModule.resolve(__dirname,'../../layouts/common-docs/static/js/search-highlight.js'),'utf8')});
  await page.locator('mark.search-highlight').waitFor();
  assert.equal(await page.locator('details').getAttribute('open'),'');
  assert.deepEqual(errors,[]);
  console.log('PASS normal language preference and archive/disclosure fallback');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
