'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const {buildAnnotatedReference} = require('./cli-annotations');
const reference = buildAnnotatedReference(require('../../content/openriak-kv/metadata/3.4.1/kv-cli-commands.json'));
(async () => {
  const browser = await chromium.launch({executablePath: process.env.OPENRIAK_BROWSER_EXECUTABLE});
  try {
    const page = await browser.newPage({permissions: ['clipboard-read', 'clipboard-write']});
    const root = (process.env.OPENRIAK_DOCS_TEST_URL || 'http://localhost:1410/docs/openriak-kv/') + '3.4.1/reference/commands/';
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    for (const route of ['riak/admin/status', 'riak/admin/cluster/join', 'riak/admin/cluster/commit', 'riak/admin/aae-status', 'riak/restart', 'riak/admin/backup', 'erlang/riak-client/get']) {
      assert.equal((await page.goto(root + route + '/')).status(), 200);
      assert.equal(await page.locator('#other-info').getAttribute('open'), null);
      assert.equal(await page.locator('#help').isVisible(), false);
      assert.equal(await page.locator('#reference-sources').isVisible(), false);
      const aliases = page.locator('#aliases');
      if (await aliases.count()) assert.equal(await aliases.getAttribute('open'), null);
      assert.equal(await page.locator('#expected-results').evaluate(e => e.tagName), 'H2');
      assert.ok(await page.locator('#errors').evaluate(e => !!(e.compareDocumentPosition(document.querySelector('#examples')) & Node.DOCUMENT_POSITION_FOLLOWING)));
      for (const row of await page.locator('.cli-errors tbody tr').all()) {
        const link = row.locator('td').first().locator('a[href^="#example-"]');
        assert.equal(await link.count(), 1);
        assert.match(await link.innerText(), /^Example \d+: .+/);
        assert.equal(await page.locator(await link.getAttribute('href')).count(), 1);
      }
      for (const link of await page.locator('#related-errors + ul a').all()) assert.match(await link.getAttribute('href'), /#errors$/);
      const hrefs = await page.locator('.related-documentation li a').evaluateAll(es => es.map(e => e.href.replace(/\/(?=#|$)/, '')));
      assert.equal(new Set(hrefs).size, hrefs.length, route + ': deduplicated related documents');
      const record = reference.pages.find(p => p.route.replace(/^\/+|\/+$/g, '') === route);
      assert.ok(record, route);
      for (const example of record.reference.examples) {
        const card = page.locator(`[data-cli-example-id="${example.id}"]`);
        const steps = card.locator(':scope > .cli-steps > .cli-step');
        assert.equal(await steps.count(), example.steps.length);
        for (let i = 0; i < example.steps.length; i++) {
          const step = steps.nth(i), expected = example.steps[i];
          assert.match(await step.locator('p strong').first().innerText(), new RegExp('^Step ' + (i+1) + ':'));
          assert.ok(!expected.invocation.includes('&&'));
          for (const [field, label] of [['stdout', 'Standard output'], ['stderr', 'Standard error']]) {
            if (!expected[field]) continue;
            const output = step.locator(`[data-cli-output-stream="${label}"]`);
            assert.equal(await output.locator('.doc-code-block').count(), 1, 'one complete code block');
            const toggle = output.locator('[data-code-expand]');
            if (await toggle.isVisible()) {
              const pre = output.locator('.doc-code-highlight pre');
              assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
              const collapsed = await pre.evaluate(e => {
                const s = getComputedStyle(e);
                return {height:e.getBoundingClientRect().height, limit:15 * parseFloat(s.lineHeight) + parseFloat(s.paddingTop) + parseFloat(s.paddingBottom), overflow:s.overflowY};
              });
              assert.ok(collapsed.height <= collapsed.limit + 1, 'at most 15 rendered lines');
              assert.equal(collapsed.overflow, 'hidden');
              assert.notEqual(await output.locator('.doc-code-highlight').evaluate(e => getComputedStyle(e).maskImage), 'none');
              const showMore = output.locator('[data-code-show-more]');
              assert.equal(await showMore.isVisible(), true);
              await showMore.click();
              assert.equal(await showMore.isVisible(), false);
              assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
              assert.ok(await pre.evaluate(e => e.clientHeight >= e.scrollHeight - 1), 'all output visible');
              assert.notEqual(await pre.evaluate(e => e.getBoundingClientRect().height), collapsed.height);
              await toggle.click();
              assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
              assert.equal(await showMore.isVisible(), true);
            }
            const source = output.locator('[data-code-source]').last();
            const captured = await (await page.request.get(new URL(await source.getAttribute('data-json-src'), page.url()).href)).json();
            assert.equal(captured, expected[field], example.id + ': full ' + field);
          }
        }
      }
      const tags = await page.locator('.annotation-tags a').evaluateAll(es => es.map(e => e.href));
      assert.ok(tags.length > 0);
      for (const tag of tags) {
        const response = await page.request.get(tag);
        assert.equal(response.status(), 200, tag);
        assert.ok((await response.text()).includes('reference-tag-documents'));
        assert.ok((await response.text()).includes('/reference/commands/' + route + '/'), tag + ': current document indexed');
      }
    }
    await page.goto(root + 'riak/admin/cluster/commit/');
    const firstExample = page.locator('.cli-example').first();
    await firstExample.locator('.cli-test-details > summary').click();
    await firstExample.getByText('Exact execution records', {exact: true}).click();
    const recordBlock = firstExample.locator('.cli-test-details details').filter({has:page.getByText('Exact execution records', {exact:true})}).locator('.doc-code-block');
    const bottom = recordBlock.locator('[data-code-show-more]');
    await bottom.waitFor({state:'visible'});
    const boxes = await recordBlock.evaluate(e => ({block:e.getBoundingClientRect().toJSON(), button:e.querySelector('[data-code-show-more]').getBoundingClientRect().toJSON()}));
    assert.ok(Math.abs((boxes.button.x + boxes.button.width/2) - (boxes.block.x + boxes.block.width/2)) < 1, 'Show more is centred');
    assert.ok(boxes.button.width < boxes.block.width/2, 'Show more has compact width');
    assert.ok(Math.abs(boxes.button.y - boxes.block.bottom) <= 2, 'Show more attaches beneath the bottom border');
    const original = await (await page.request.get(new URL(await recordBlock.locator('[data-code-source]').getAttribute('data-json-src'), page.url()).href)).json();
    await recordBlock.locator('[data-code-copy]').click();
    assert.equal(await page.evaluate(() => navigator.clipboard.readText()), original, 'copy includes hidden lines');
    await bottom.click();
    assert.equal(await bottom.isVisible(), false);
    const top = recordBlock.locator('[data-code-expand]');
    assert.equal(await top.getAttribute('aria-expanded'), 'true');
    await top.focus();
    await page.keyboard.press('Enter');
    assert.equal(await bottom.isVisible(), true);
    await page.goto(root + 'riak/admin/status/');
    await page.setViewportSize({width: 390, height: 844});
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'mobile page does not overflow horizontally');
    assert.deepEqual(errors, []);
    console.log('Command layout: full streams, single-block 15-line clipping and toolbar expansion, numbered steps, error links, collapsed sections, tag pages, related-document deduplication and mobile width passed.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
