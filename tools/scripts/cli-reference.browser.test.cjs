'use strict';
const assert = require('node:assert/strict');
const { chromium } = require('playwright');

(async () => {
  const base = process.env.OPENRIAK_CLI_TEST_URL || 'http://127.0.0.1:1480/docs/openriak-kv/3.4.0/reference/commands/';
  const browser = await chromium.launch({ executablePath: process.env.OPENRIAK_BROWSER_EXECUTABLE || undefined });
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, permissions: ['clipboard-read', 'clipboard-write'] });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(base);
    const search = page.locator('[data-cli-search]');
    await search.waitFor();
    const total = await page.locator('[data-cli-row]').count();
    assert.ok(total > 200);
    const links = await page.locator('[data-cli-row] td:first-child a').evaluateAll(elements => elements.map(e => e.href));
    assert.equal(new Set(links).size, total);
    const queue = [...links];
    await Promise.all(Array.from({ length: 6 }, async () => {
      while (queue.length) {
        const url = queue.pop();
        const response = await context.request.get(url);
        assert.equal(response.status(), 200, url);
        const html = await response.text();
        assert.ok(html.includes('id="options"'), `Options missing: ${url}`);
        assert.ok(html.includes('id="help"'), `Help missing: ${url}`);
      }
    }));
    await search.fill('repair_2i');
    assert.ok(await page.locator('[data-cli-row]:visible').count() > 0);
    assert.ok((await page.locator('[data-cli-row]:visible td:first-child').allTextContents()).every(t => t.includes('repair-2i')));
    await search.fill('not-a-command-123');
    assert.equal(await page.locator('[data-cli-row]:visible').count(), 0);
    assert.ok(await page.locator('[data-cli-empty]').isVisible());
    await search.fill('');
    assert.equal(await page.locator('[data-cli-row]:visible').count(), total);

    await page.goto(base + 'riak/admin/set/');
    await page.locator('.cli-options').waitFor();
    for (const flag of ['--node', '--all', '--format', '--help']) assert.ok((await page.locator('.cli-options').innerText()).includes(flag));
    await page.locator('[data-code-copy]').first().click();
    const copied = await page.evaluate(() => navigator.clipboard.readText());
    assert.match(copied, /riak-admin set <variable>=<value>/);
    assert.ok(!copied.includes('Usage: _'));

    await page.goto(base + 'riak/daemon/');
    await page.waitForFunction(() => Boolean(document.documentElement.dataset.selectedOs));
    assert.match((await page.locator('[data-cli-service-families]:visible').allTextContents()).join('\n'), /systemctl start riak/);
    await page.locator('[data-os-trigger]').click();
    await page.locator('[data-os-id^="alpine-"]').first().click();
    let serviceText = (await page.locator('[data-cli-service-families]:visible').allTextContents()).join('\n');
    assert.match(serviceText, /rc-service riak start/);
    assert.match(serviceText, /riak daemon/);
    assert.ok(!serviceText.includes('systemctl'));
    await page.reload();
    await page.waitForFunction(() => document.documentElement.dataset.selectedOs?.startsWith('alpine-'));
    serviceText = (await page.locator('[data-cli-service-families]:visible').allTextContents()).join('\n');
    assert.match(serviceText, /rc-service riak start/);
    await page.locator('[data-os-trigger]').click();
    await page.locator('[data-os-id^="ubuntu-"]').first().click();
    serviceText = (await page.locator('[data-cli-service-families]:visible').allTextContents()).join('\n');
    assert.match(serviceText, /systemctl start riak/);
    assert.ok(!serviceText.includes('rc-service'));

    await page.goto(base + 'riak/start/');
    assert.match(await page.locator('.cli-command-reference').innerText(), /deprecated/i);
    await page.goto(base + 'riak/admin/search/');
    assert.match(await page.locator('.cli-notice').innerText(), /unavailable/);
    await page.goto(base + 'erlang/riak-client/aae-fold/erase-keys/');
    const fold = await page.locator('.cli-command-reference').innerText();
    assert.match(fold, /aae_fold\/1/);
    assert.match(fold, /aae_fold\/2/);
    assert.match(fold, /erase_keys/);
    assert.match(fold, /Erlang shell/);
    await page.goto(base + 'erlang/riak-core-vnode-manager/kill-repairs/');
    assert.match(await page.locator('.cli-command-reference').innerText(), /Internal API/);

    const index = await (await context.request.get(new URL('../../index.json', base).href)).json();
    assert.ok(index.some(item => item.url.endsWith('/reference/commands/riak/admin/repair-2i/')), 'branch command pages must be searchable');
    for (const route of ['', 'riak/admin/set/', 'erlang/riak-client/aae-fold/erase-keys/']) {
      await page.setViewportSize({ width: 390, height: 844 });
      await page.goto(base + route);
      await page.locator('.doc-article').waitFor();
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), `Mobile overflow: ${route}`);
    }
    assert.deepEqual(errors, []);
    console.log(`CLI reference: ${total} linked topics, help/options, aliases, copy, OS switching, arities, status, search indexing and mobile layout passed.`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
