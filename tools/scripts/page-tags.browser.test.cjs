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
   assert.equal(await page.locator(`#docs-sidebar a[href^="/docs/openriak-kv/${version}/tags/"]`).count(),0);
   for (const route of ['tags/','tags/feature/','tags/feature/client-operations/']) {
    assert.equal((await page.request.get(`${base}openriak-kv/${version}/${route}`)).status(),200);
   }
   const search=await (await page.request.get(`${base}openriak-kv/${version}/index.json`)).json();
   assert.ok(search.every(entry=>!entry.url.includes(`/${version}/tags/`)),'search excludes tag pages');
   const summary=page.locator('.doc-summary');
   assert.ok(await summary.locator('.doc-reading-time').isVisible());
   assert.deepEqual(await summary.locator('[data-tag-type="feature"]').allTextContents(),['Feature: read-repair','Feature: tictac-aae']);
   assert.equal(await summary.locator('[data-tag-type="concept"]').innerText(),'Concept: replica-repair');
   for(const link of await summary.locator('.page-tag').all()) {
    const href=await link.getAttribute('href');
    assert.ok(href.startsWith(`/docs/openriak-kv/${version}/tags/`));
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
  assert.ok(await page.locator('.doc-summary a[href$="/3.4.1/tags/feature/cluster-management/"]').isVisible());
  await page.locator('.doc-summary a[href$="/3.4.1/tags/feature/cluster-management/"]').click();
  assert.equal(await page.locator('main h1').innerText(),'Feature: cluster-management');
  assert.equal(await page.locator('main a[href*="/3.4.0/"]').count(),0,'only the selected release is indexed');
  assert.ok(await page.locator('main a[href$="/3.4.1/reference/commands/riak/admin/cluster/commit/"]').count());
  assert.ok(await page.locator('main a[href$="/3.4.1/how-to/cluster-lifecycle/plan-and-commit-a-membership-change/"]').count());
  await page.goto(`${base}openriak-kv/3.4.1/tags/feature/handoff/`);
  assert.ok(await page.locator('main a[href$="/how-to/cluster-lifecycle/monitor-and-control-handoffs/"]').count(),'version-specific indexes include front-matter tags');
  for(const version of ['3.4.0','3.4.1']) {
   await page.goto(`${base}openriak-kv/${version}/reference/commands/erlang/riak-client/ensemble/`);
   for(const link of await page.locator('.annotation-tag').all()) {
    const href=await link.getAttribute('href');
    assert.ok(href.startsWith(`/docs/openriak-kv/${version}/tags/`),href);
    assert.equal((await page.request.get(new URL(href,page.url()).href)).status(),200,href);
   }
   await page.goto(`${base}openriak-kv/${version}/reference/configuration/all-configuration-settings-and-defaults/`);
   const links=await page.locator('a.configuration-setting-tag').evaluateAll(es=>[...new Set(es.map(e=>e.href))]);
   assert.ok(links.some(url=>url.includes('/tags/repository/')));
   assert.ok(links.some(url=>url.includes('/tags/module/')));
   assert.ok(links.some(url=>url.includes('/tags/metadata/')));
   for(const href of links) {
    assert.ok(href.includes(`/openriak-kv/${version}/tags/`),href);
    assert.equal((await page.request.get(href)).status(),200,href);
   }
  }
  console.log('Header tags, multiple values, typed indexes, release isolation, front-matter reference matches and mobile wrapping passed.');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
