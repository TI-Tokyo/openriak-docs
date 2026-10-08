'use strict';
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.OPENRIAK_BROWSER_EXECUTABLE});
 try {
  const page=await browser.newPage({viewport:{width:1440,height:960}});
  const base=process.env.OPENRIAK_DOCS_TEST_URL || 'http://localhost:1410/docs/';
  const topic='foundations/replication-and-repair/read-repair-and-tictac-anti-entropy/';
  for(const version of ['3.4.0','3.4.1']) {
   assert.equal((await page.goto(`${base}openriak-kv/${version}/${topic}`)).status(),200);
   const summary=page.locator('.doc-summary');
   assert.ok(await summary.locator('.doc-reading-time').isVisible());
   assert.deepEqual(await summary.locator('[data-tag-type="feature"]').allTextContents(),['Feature: read-repair','Feature: tictac-aae']);
   assert.equal(await summary.locator('[data-tag-type="concept"]').innerText(),'Concept: replica-repair');
   for(const link of await summary.locator('.page-tag').all()) {
    const href=await link.getAttribute('href');
    const response=await page.request.get(new URL(href,page.url()).href);
    assert.equal(response.status(),200,href);
    assert.ok((await response.text()).includes(`/openriak-kv/${version}/${topic}`),href);
   }
   const boxes=await summary.evaluate(e=>({read:e.querySelector('.doc-reading-time').getBoundingClientRect().toJSON(),tag:e.querySelector('.page-tag').getBoundingClientRect().toJSON()}));
   assert.ok(Math.abs(boxes.read.y-boxes.tag.y)<12,'tags sit beside read time at desktop width');
   await page.setViewportSize({width:390,height:844});
   assert.ok(await summary.locator('.page-tag').first().isVisible());
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'mobile header wraps without horizontal overflow');
   await page.setViewportSize({width:1440,height:960});
  }
  await page.goto(`${base}openriak-kv/3.4.1/reference/commands/riak/admin/cluster/commit/`);
  assert.ok(await page.locator('.doc-summary a[href$="/tags/feature/cluster-management/"]').isVisible());
  await page.locator('.doc-summary a[href$="/tags/feature/cluster-management/"]').click();
  assert.equal(await page.locator('main h1').innerText(),'Feature: cluster-management');
  const groups=await page.locator('.tag-document-group h2').allTextContents();
  assert.deepEqual(groups,['OpenRiak KV 3.4.0','OpenRiak KV 3.4.1']);
  assert.ok(await page.locator('main a[href$="/3.4.1/reference/commands/riak/admin/cluster/commit/"]').count());
  assert.ok(await page.locator('main a[href$="/3.4.1/how-to/cluster-lifecycle/plan-and-commit-a-membership-change/"]').count());
  await page.goto(`${base}openriak-kv/3.4.1/reference/tags/feature/handoff/`);
  assert.ok(await page.locator('main a[href$="/how-to/cluster-lifecycle/monitor-and-control-handoffs/"]').count(),'version-specific indexes include front-matter tags');
  console.log('Header tags, multiple values, typed indexes, release grouping, front-matter reference matches and mobile wrapping passed.');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
