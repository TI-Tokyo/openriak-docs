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
   const metadata=require(`../../content/openriak-kv/metadata/${version}/kv-settings.json`);
   const total=Object.values(metadata.settings).filter(setting=>!setting.hidden).length;
   const catalogue=base+version+'/reference/configuration/all-configuration-settings-and-defaults/';
   assert.equal((await page.goto(catalogue)).status(),200);
   const table=page.locator('.configuration-reference-wrap');
   const rows=table.locator('tbody tr[data-configuration-key]');
   const visible=table.locator('tbody tr[data-configuration-key]:visible');
   assert.equal(await rows.count(),total);
   const checkAlternatives=async (cell,expected)=>{
    const list=cell.locator('ul.configuration-reference-values');
    assert.equal(await list.count(),1);
    const actual=await list.locator('li').evaluateAll(items=>items.map(item=>({
     value:item.querySelector('code, .configuration-reference-type').textContent,
     copy:item.querySelector('[data-copy-value]')?.dataset.copyValue || null,
     code:Boolean(item.querySelector('code'))
    })));
    assert.deepEqual(actual,expected.map(([value,literal])=>({value,copy:literal?value:null,code:literal})));
   };
   const datatype=name=>table.locator(`[data-configuration-key="${name}"] .configuration-reference-datatype`);
   await checkAlternatives(datatype('bitcask.fold.max_puts'),[['Integer',false],['unlimited',true]]);
   await checkAlternatives(datatype('bitcask.fold.max_age'),[['unlimited',true],['Duration (ms)',false]]);
   await checkAlternatives(datatype('anti_entropy.tree.expiry'),[['Duration (ms)',false],['never',true]]);
   await checkAlternatives(datatype('buckets.default.r'),[['quorum',true],['all',true],['Integer',false]]);
   await checkAlternatives(datatype('object.format'),[['1',true],['0',true]]);
   await checkAlternatives(datatype('datatypes.compression_level'),[['Integer',false],['on',true],['off',true]]);
   assert.match(await datatype('delete_mode').innerText(),/1 through 299999/);
   await checkAlternatives(datatype('anti_entropy.bloomfilter'),[['on',true],['off',true]]);
   await checkAlternatives(datatype('aae_tokenbucket'),[['enabled',true],['disabled',true]]);
   const feature=table.locator('[data-configuration-tag-filter="feature"]');
   const concept=table.locator('[data-configuration-tag-filter="concept"]');
   const repository=table.locator('[data-configuration-tag-filter="repository"]');
   const module=table.locator('[data-configuration-tag-filter="module"]');
   const metadataTag=table.locator('[data-configuration-tag-filter="metadata"]');
   const secretNames=Object.entries(metadata.settings)
    .filter(([,setting])=>!setting.hidden && (setting.tags || []).includes('secretSettings'))
    .map(([name])=>name).sort();
   assert.ok(secretNames.length>0);
   await metadataTag.selectOption('secretSettings');
   assert.deepEqual((await visible.evaluateAll(rows=>rows.map(row=>row.dataset.configurationKey))).sort(),secretNames);
   assert.equal(await visible.locator('[data-configuration-inferred-default]').count(),secretNames.length);
   assert.equal(await visible.locator('[data-configuration-default-empty]:visible').count(),0);
   const queueDefault=table.locator('[data-configuration-key="riak_kv.queue_raw_max_results"] [data-configuration-inferred-default]');
   assert.match(await queueDefault.innerText(),version==='3.4.0'?/Not applicable/:/1000/);
   const timeoutDefault=table.locator('[data-configuration-key="riak_kv.anti_entropy_timeout"] [data-configuration-inferred-default]');
   assert.match(await timeoutDefault.innerText(),/60000.*300000/);
   await page.locator('[data-os-trigger]').click();
   await page.locator('[data-os-id^="alpine-"]').first().click();
   assert.equal(await visible.locator('[data-configuration-default-empty]:visible').count(),0);
   assert.match(await timeoutDefault.innerText(),/60000.*300000/);
   await page.locator('[data-os-trigger]').click();
   await page.locator('[data-os-id^="ubuntu-"]').first().click();
   assert.equal(await visible.locator('[data-configuration-default-empty]:visible').count(),0);
   assert.equal(await table.locator('[data-configuration-results]').innerText(),`${secretNames.length} of ${total} rows`);
   await repository.selectOption('riak_kv');
   const secretKvCount=await visible.count();assert.ok(secretKvCount>0 && secretKvCount<secretNames.length);
   for(const tags of await visible.evaluateAll(rows=>rows.map(row=>JSON.parse(row.dataset.configurationTags)))) {
    assert.ok(tags.metadata.includes('secretSettings') && tags.repository.includes('riak_kv'));
   }
   await table.locator('[data-configuration-search]').fill('queue_raw_max_results');
   assert.equal(await visible.count(),1);
   await table.locator('[data-configuration-search]').fill('');
   await table.locator('[data-configuration-sort]').click();assert.equal(await visible.count(),secretKvCount);
   await table.locator('[data-configuration-reset]').click();assert.equal(await visible.count(),total);
   assert.equal(await metadataTag.inputValue(),'');
   await table.locator('[data-configuration-search]').fill('secretSettings');
   assert.deepEqual((await visible.evaluateAll(rows=>rows.map(row=>row.dataset.configurationKey))).sort(),secretNames);
   await table.locator('[data-configuration-reset]').click();
   await feature.selectOption('leveled');
   assert.ok(await visible.count()>10 && await visible.count()<total);
   await concept.selectOption('compression');
   const count=await visible.count();assert.ok(count>0 && count<10);
   for(const tags of await visible.evaluateAll(rows=>rows.map(row=>JSON.parse(row.dataset.configurationTags)))) {
    assert.ok(tags.feature.includes('leveled') && tags.concept.includes('compression'));
   }
   assert.match(await table.locator('[data-configuration-results]').innerText(),new RegExp(`^${count} of ${total} rows$`));
   await table.locator('[data-configuration-sort]').click();assert.equal(await visible.count(),count);
   await table.locator('[data-configuration-reset]').click();assert.equal(await visible.count(),total);
   await module.selectOption('riak_kv_vnode');assert.ok(await visible.count()>0);
   await repository.selectOption('riak_kv');assert.ok(await visible.count()>0);
   await repository.selectOption('riak');assert.equal(await visible.count(),0);
   await table.locator('[data-configuration-reset]').click();
   const search=table.locator('[data-configuration-search]');
   await search.fill('tictac-aae');assert.ok(await visible.count()>0 && await visible.count()<total);
   // Match a module tag through the table search.
   await search.fill('riak_kv_ttaaefs_manager');assert.ok(await visible.count()>0);
   await table.locator('[data-configuration-search-mode]').selectOption('regex');
   await search.fill('[');assert.match(await table.locator('[data-configuration-results]').innerText(),/Invalid/);
   await table.locator('[data-configuration-reset]').click();assert.equal(await visible.count(),total);
   await table.locator('[data-configuration-search-mode]').selectOption('contains');
   assert.equal(await table.locator('.configuration-related-settings').count(),0);
   const defaultBefore=await table.locator('[data-configuration-key="ring_size"] [data-configuration-default-value]').innerText();
   assert.match(defaultBefore,/^\d+$/);
   await page.setViewportSize({width:390,height:844});
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'mobile overflow');
   await page.setViewportSize({width:1440,height:1000});
   assert.equal((await page.goto(base+version+'/how-to/planning-a-deployment/choose-a-ring-size/')).status(),200);
   const detail=page.locator('.configuration-reference-item-wrap');
   assert.deepEqual(await detail.locator('.configuration-reference-description .configuration-setting-tag').evaluateAll(tags=>[...new Set(tags.map(tag=>tag.dataset.tagCategory))]),['feature','repository','module','concept']);
   const links=detail.locator('.configuration-related-settings a');assert.ok(await links.count()>0);
   assert.equal(await detail.locator('[data-configuration-default-value]').innerText(),defaultBefore);
   for(const href of await links.evaluateAll(links=>links.map(a=>a.href))) {
    const url=new URL(href);assert.ok(url.pathname.includes('/'+version+'/'));
    const response=await page.request.get(url.href);assert.equal(response.status(),200);
    const html = await response.text();
    assert.ok(await page.evaluate(({html, id}) =>
     Boolean(new DOMParser().parseFromString(html, 'text/html').getElementById(id)),
     {html, id: decodeURIComponent(url.hash.slice(1))}), 'Related anchor must exist in both minified and development HTML');
   }
   await links.first().click();await page.waitForLoadState('domcontentloaded');assert.ok(await page.locator('tr:target').count());
   assert.equal((await page.goto(base+version+'/to-do/tests/configuration-reference-table-test/')).status(),200);
   const inferredDetail=page.locator('tbody[data-configuration-key="ibrowse.inactivity_timeout"]');
   await checkAlternatives(page.locator('tbody[data-configuration-key="bitcask.fold.max_puts"] .configuration-reference-item-datatype'),[['Integer',false],['unlimited',true]]);
   await checkAlternatives(page.locator('tbody[data-configuration-key="bitcask.fold.max_age"] .configuration-reference-item-datatype'),[['unlimited',true],['Duration (ms)',false]]);
   assert.match(await inferredDetail.locator('[data-configuration-inferred-default]').innerText(),/10000/);
   assert.match(await inferredDetail.locator('.configuration-reference-item-datatype').innerText(),/Integer.*milliseconds/s);
   assert.equal(await inferredDetail.locator('[data-configuration-default-empty]').isVisible(),false);
   await page.locator('[data-os-trigger]').click();
   await page.locator('[data-os-id^="alpine-"]').first().click();
   assert.match(await inferredDetail.locator('[data-configuration-inferred-default]').innerText(),/10000/);
   assert.equal(await inferredDetail.locator('[data-configuration-default-empty]').isVisible(),false);
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
