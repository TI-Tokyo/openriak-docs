'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
(async () => {
  const browser = await chromium.launch({executablePath: process.env.OPENRIAK_BROWSER_EXECUTABLE});
  try {
    const page = await browser.newPage({viewport:{width:1280,height:900}});
    const root = (process.env.OPENRIAK_DOCS_TEST_URL || 'http://localhost:1410/docs/openriak-kv/') + '3.4.1/reference/commands/';
    await page.goto(root + 'riak/admin/status/');
    await page.evaluate(() => window.OpenRiakPageToolsReady);
    const blocks = page.locator('.doc-code-block.has-hidden-output').filter({visible:true});
    assert.ok(await blocks.count() >= 2, 'multiple long outputs including one above the selected block');
    const block = blocks.nth(1);
    const more = block.locator('[data-code-show-more]');
    await more.scrollIntoViewIfNeeded();
    const before = await block.evaluate(e => e.getBoundingClientRect().top);
    await more.click();
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    assert.ok(Math.abs(await block.evaluate(e => e.getBoundingClientRect().top) - before) < 2, 'expanding earlier blocks preserves current block position');
    assert.equal(await blocks.first().locator('[data-code-expand]').getAttribute('aria-expanded'), 'true');
    assert.equal(await more.isVisible(), false);
    await page.reload();
    await page.evaluate(() => window.OpenRiakPageToolsReady);
    assert.equal(await blocks.first().locator('[data-code-expand]').getAttribute('aria-expanded'), 'true', 'expanded preference survives reload');
    const top = block.locator('[data-code-expand]');
    await top.scrollIntoViewIfNeeded();
    const beforeCollapse = await block.evaluate(e => e.getBoundingClientRect().top);
    await top.click();
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    assert.ok(Math.abs(await block.evaluate(e => e.getBoundingClientRect().top) - beforeCollapse) < 2, 'collapsing earlier blocks preserves current block position');
    await page.goto(root + 'riak/admin/cluster/commit/');
    await page.evaluate(() => window.OpenRiakPageToolsReady);
    assert.equal(await page.locator('[data-code-expand]').first().getAttribute('aria-expanded'), 'false', 'collapsed preference survives navigation');
    console.log('Output preference persists across reloads and pages; expansion and collapse preserve the current block position.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode=1; });
