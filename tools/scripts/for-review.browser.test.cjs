'use strict';

const assert = require('node:assert/strict');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.OPENRIAK_BROWSER_EXECUTABLE || undefined });
  try {
    const page = await browser.newPage();
    const url = process.env.OPENRIAK_REVIEW_TEST_URL || 'http://localhost:1410/docs/openriak-kv/3.4.0/to-do/for-review/';
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(url);
    await page.locator('[data-review-filters]').waitFor();
    const rows = await page.locator('[data-review-values]').evaluateAll(elements => elements.map(element => ({
      href: element.querySelector('a').getAttribute('href'), values: JSON.parse(element.dataset.reviewValues)
    })));
    const fields = ['draft', 'status', 'review_scope', 'editorial_review', 'technical_review', 'review-by'];
    assert.ok(rows.every(row => row.href !== new URL(url).pathname), 'the nested report must exclude itself');
    assert.ok(rows.some(row => row.href.endsWith('/foundations/')), 'the nested report must still include the whole documentation version');
    const select = field => page.locator(`[data-review-filter="${field}"]`);
    const check = async filters => {
      const expected = rows.filter(row => Object.entries(filters).every(([key, value]) => value === null
        ? row.values[key].length === 0 : row.values[key].includes(value))).map(row => row.href).sort();
      const actual = await page.locator('[data-review-values]:visible a').evaluateAll(links => links.map(link => link.getAttribute('href')).sort());
      assert.deepEqual(actual, expected);
      assert.equal(await page.locator('[data-review-count]').textContent(), `${expected.length} of ${rows.length} pages`);
      assert.equal(await page.locator('[data-review-empty]').isVisible(), expected.length === 0);
      assert.ok(await page.locator('[data-review-group]').evaluateAll(groups => groups.every(group =>
        group.hidden === [...group.querySelectorAll('[data-review-values]')].every(row => row.hidden))));
    };

    await check({});
    assert.ok(await select('review-by').locator('option').evaluateAll(options => options.some(option => option.textContent === 'Unassigned')));
    assert.ok(await page.locator('[data-review-values]').evaluateAll(elements => elements.every(element => {
      const expected = JSON.parse(element.dataset.reviewValues)['review-by'].join(', ');
      const label = [...element.querySelectorAll('dt')].find(node => node.textContent === 'Review by:');
      return label?.nextElementSibling.textContent === expected;
    })));
    for (const field of fields) {
      const expected = new Set(rows.flatMap(row => row.values[field].length ? row.values[field] : [null]).map(JSON.stringify));
      const options = await select(field).locator('option').evaluateAll(options => options.map(option => option.value).filter(Boolean));
      assert.deepEqual(new Set(options), expected, `${field} offers individual values`);
      const value = options[0];
      await select(field).selectOption(value);
      await check({ [field]: JSON.parse(value) });
      if (expected.has('null')) {
        await select(field).selectOption('null');
        await check({ [field]: null });
      }
      await page.locator('[data-review-reset]').click();
    }

    const releaseNotes = rows.find(row => row.href.endsWith('/release-notes/'));
    const filters = { draft: 'true', status: 'needs-review', review_scope: 'content', technical_review: 'done', 'review-by': releaseNotes.values['review-by'][0] };
    for (const [field, value] of Object.entries(filters)) await select(field).selectOption(JSON.stringify(value));
    await check(filters);
    assert.ok(await page.locator('[data-review-values]:visible').count() > 0);
    await page.reload();
    await page.locator('[data-review-filters]').waitFor();
    for (const [field, value] of Object.entries(filters)) assert.equal(await select(field).inputValue(), JSON.stringify(value));
    await check(filters);
    await select('draft').selectOption(JSON.stringify('false'));
    await check({ ...filters, draft: 'false' });
    await page.locator('[data-review-reset]').click();
    await check({});
    await page.reload();
    await page.locator('[data-review-filters]').waitFor();
    await check({});

    await page.evaluate(() => localStorage.setItem('openriak-docs-review-filters:openriak-kv', 'invalid JSON'));
    await page.reload();
    await page.locator('[data-review-filters]').waitFor();
    await check({});
    await select('status').evaluate(element => {
      element.focus({ preventScroll: true });
      window.scrollTo(0, 1000);
    });
    await page.keyboard.press('Control+Home');
    await page.waitForFunction(() => window.scrollY === 0);
    assert.equal(await select('status').inputValue(), '');
    assert.ok(await page.locator('.skip-link').evaluate(element => element.getBoundingClientRect().bottom <= 0));
    assert.deepEqual(errors, []);
    await page.setViewportSize({ width: 390, height: 844 });
    assert.ok(await page.locator('[data-review-filters]').evaluate(element => {
      const rect = element.getBoundingClientRect();
      return rect.left >= 0 && rect.right <= window.innerWidth;
    }));
    console.log('Review filters: all six fields, Unassigned defaults, combined matching, saved/reset selections, and responsive controls passed.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
