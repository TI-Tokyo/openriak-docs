'use strict';
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
(async () => {
 const browser=await chromium.launch({executablePath:process.env.OPENRIAK_BROWSER_EXECUTABLE});
 try {
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  const base=process.env.OPENRIAK_DOCS_TEST_URL || 'http://localhost:1410/docs/openriak-kv/';
  for(const version of ['3.4.0','3.4.1']) {
   const catalogue=base+version+'/reference/configuration/all-configuration-settings-and-defaults/';
   assert.equal((await page.goto(catalogue)).status(),200);
   const table=page.locator('.configuration-reference-wrap');
   const rows=table.locator('tbody tr[data-configuration-key]');
   const visible=table.locator('tbody tr[data-configuration-key]:visible');
   assert.equal(await rows.count(),427);
   const feature=table.locator('[data-configuration-tag-filter="feature"]');
   const concept=table.locator('[data-configuration-tag-filter="concept"]');
   const repository=table.locator('[data-configuration-tag-filter="repository"]');
   const module=table.locator('[data-configuration-tag-filter="module"]');
   await feature.selectOption('leveled');
   assert.ok(await visible.count()>10 && await visible.count()<427);
   await concept.selectOption('compression');
   const count=await visible.count();assert.ok(count>0 && count<10);
   for(const tags of await visible.evaluateAll(rows=>rows.map(row=>JSON.parse(row.dataset.configurationTags)))) {
    assert.ok(tags.feature.includes('leveled') && tags.concept.includes('compression'));
   }
   assert.match(await table.locator('[data-configuration-results]').innerText(),new RegExp(`^${count} of 427 rows$`));
   await table.locator('[data-configuration-sort]').click();assert.equal(await visible.count(),count);
   await table.locator('[data-configuration-reset]').click();assert.equal(await visible.count(),427);
   await module.selectOption('riak_kv_vnode');assert.ok(await visible.count()>0);
   await repository.selectOption('riak_kv');assert.ok(await visible.count()>0);
   await repository.selectOption('riak');assert.equal(await visible.count(),0);
   await table.locator('[data-configuration-reset]').click();
   const search=table.locator('[data-configuration-search]');
   await search.fill('tictac-aae');assert.ok(await visible.count()>0 && await visible.count()<427);
   // Match a module tag that never occurs in displayed prose or the setting name.
   await search.fill('riak_kv_ttaaefs_manager');assert.ok(await visible.count()>0);
   await table.locator('[data-configuration-search-mode]').selectOption('regex');
   await search.fill('[');assert.match(await table.locator('[data-configuration-results]').innerText(),/Invalid/);
   await table.locator('[data-configuration-reset]').click();assert.equal(await visible.count(),427);
   await table.locator('[data-configuration-search-mode]').selectOption('contains');
   assert.equal(await table.locator('.configuration-related-settings').count(),0);
   const defaultBefore=await table.locator('[data-configuration-key="ring_size"] [data-configuration-default-value]').innerText();
   assert.match(defaultBefore,/^\d+$/);
   await page.setViewportSize({width:390,height:844});
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'mobile overflow');
   await page.setViewportSize({width:1440,height:1000});
   assert.equal((await page.goto(base+version+'/how-to/planning-a-deployment/choose-a-ring-size/')).status(),200);
   const detail=page.locator('.configuration-reference-item-wrap');
   assert.equal(await detail.locator('.annotation-tags dt').count(),4);
   const links=detail.locator('.configuration-related-settings a');assert.ok(await links.count()>0);
   assert.equal(await detail.locator('[data-configuration-default-value]').innerText(),defaultBefore);
   for(const href of await links.evaluateAll(links=>links.map(a=>a.href))) {
    const url=new URL(href);assert.ok(url.pathname.includes('/'+version+'/'));
    const response=await page.request.get(url.href);assert.equal(response.status(),200);
    assert.ok((await response.text()).includes(`id="${url.hash.slice(1)}"`));
   }
   await links.first().click();await page.waitForLoadState('domcontentloaded');assert.ok(await page.locator('tr:target').count());
   for(const route of ['riak/admin/describe','erlang/riak-client/get']) {
    assert.equal((await page.goto(base+version+'/reference/commands/'+route+'/')).status(),200);
    assert.equal(await page.locator('.cli-command-reference > .annotation-tags dt').count(),4);
   }
   await page.goto(base+version+'/reference/commands/');
   const index=page.locator('[data-cli-index]');
   await index.locator('[data-cli-tag-filter="feature"]').selectOption('cluster-management');
   const cliRows=index.locator('[data-cli-row]:visible');assert.ok(await cliRows.count()>0);
   await index.locator('[data-cli-search]').fill('riak_core_console');assert.ok(await cliRows.count()>0);
   for(const tags of await cliRows.evaluateAll(rows=>rows.map(row=>JSON.parse(row.dataset.cliTags)))) assert.ok(tags.feature.includes('cluster-management') && tags.module.includes('riak_core_console'));
   await index.locator('[data-cli-reset]').click();assert.equal(await cliRows.count(),version==='3.4.0'?269:276);
   console.log(version+': tag filters, tag search, sorting, reset, mobile layout, detail links and command tags passed.');
  }
  assert.deepEqual(errors,[]);
 } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
