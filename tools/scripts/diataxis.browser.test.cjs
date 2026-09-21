'use strict';
const assert = require('node:assert/strict');
const { chromium } = require('playwright');

(async () => {
  const base = process.env.OPENRIAK_DOCS_TEST_URL || 'http://localhost:1410/docs/openriak-kv/';
  const browser = await chromium.launch({ executablePath: process.env.OPENRIAK_BROWSER_EXECUTABLE || undefined });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    for (const version of ['3.4.0', '3.4.1']) {
      await page.goto(base + version + '/reference/orientation-and-compatibility/backend-capability-matrix/');
      const table = page.locator('[data-configuration-reference]').first();
      await table.locator('[data-configuration-search]').fill('Leveled');
      assert.equal(await table.locator('tbody tr:visible').count(), 1);
      assert.match(await table.locator('tbody tr:visible').innerText(), /complex_query/);
      assert.doesNotMatch(await table.locator('tbody tr:visible').innerText(), /app_helper|define|record/);
      await table.locator('[data-configuration-search]').fill('');
      await table.locator('[data-configuration-sort]').click();
      const names = await table.locator('tbody tr td:first-child').allTextContents();
      assert.deepEqual(names, [...names].sort((a, b) => a.localeCompare(b)));
      await table.locator('[data-configuration-search-mode]').selectOption('regex');
      await table.locator('[data-configuration-search]').fill('[');
      assert.match(await table.locator('[data-configuration-results]').innerText(), /Invalid regular expression/);
      await table.locator('[data-configuration-search]').fill('Bitcask|Memory');
      assert.equal(await table.locator('tbody tr:visible').count(), 2);
      await table.locator('[data-configuration-search-mode]').selectOption('contains');

      await page.goto(base + version + '/tutorials/indexes-and-querying/combine-query-conditions/');
      const previous = page.locator('.doc-sequence a').first();
      const next = page.locator('.doc-sequence a').last();
      assert.match(await previous.getAttribute('href'), new RegExp('/' + version + '/tutorials/.*/search-projected-attributes/'));
      await next.click();
      assert.match(await page.locator('.doc-article > h1').innerText(), /Produce counts/);
      await page.locator('.doc-sequence a').first().click();
      assert.match(await page.locator('.doc-article > h1').innerText(), /Combine query conditions/);
      assert.ok(await page.locator('.related-documentation a').count() >= 3);
      const heading = await page.locator('.doc-article > h1').evaluate(e => ({ border: getComputedStyle(e).borderInlineStartWidth, size: parseFloat(getComputedStyle(e).fontSize) }));
      assert.ok(parseFloat(heading.border) > 0 && heading.size >= 32);
      await page.setViewportSize({ width: 390, height: 844 });
      await page.evaluate(() => document.documentElement.dataset.theme = 'dark');
      assert.ok(await page.locator('.doc-article > h1').isVisible());
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      assert.ok(overflow <= 1, `Mobile page overflow: ${overflow}`);
      await page.setViewportSize({ width: 1440, height: 1000 });
    }
    assert.deepEqual(errors, []);
    console.log('Diataxis reference filters, sorting, workflow links, headings and mobile layout passed for both versions.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
