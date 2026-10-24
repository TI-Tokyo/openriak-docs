'use strict';
const assert = require('node:assert/strict');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.OPENRIAK_BROWSER_EXECUTABLE });
  const base = process.env.OPENRIAK_DOCS_TEST_URL || 'http://localhost:1410/docs/';
  try {
    for (const javaScriptEnabled of [false, true]) {
      const context = await browser.newContext({ javaScriptEnabled, viewport: { width: 1920, height: 960 } });
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      for (const version of ['3.4.0', '3.4.1']) {
        const response = await page.goto(`${base}openriak-kv/${version}/to-do/tests/mermaid/`);
        assert.equal(response.status(), 200);
        assert.equal(await page.locator('.doc-diagram svg').count(), 8);
        assert.equal(await page.locator('.doc-diagram svg:visible').count(), 4);
        assert.equal(await page.locator('.doc-diagram-render--wide svg:visible').count(), 4);
        assert.equal(await page.locator('script[src*="pele"], script[src*="mermaid"]').count(), 0);
        assert.ok((await response.text()).includes('<svg'), 'SVG is present in server HTML');
        for (const svg of await page.locator('.doc-diagram svg:visible').all()) assert.ok(await svg.isVisible());
        const light = await page.locator('.doc-diagram svg').first().evaluate(svg => getComputedStyle(svg).color);
        await page.evaluate(() => { document.documentElement.dataset.theme = 'dark'; });
        const dark = await page.locator('.doc-diagram svg').first().evaluate(svg => getComputedStyle(svg).color);
        assert.notEqual(light, dark, 'SVG colors follow the theme without rendering again');
        await page.evaluate(() => { document.documentElement.dataset.theme = 'light'; });
        await page.locator('.doc-diagram summary').first().click();
        assert.ok(await page.locator('.doc-diagram pre').first().isVisible());
        const flowchart = page.locator('.doc-diagram').first();
        const positions = async () => flowchart.locator('svg:visible').evaluate(svg =>
          ['Client', 'Coordinator'].map(id => {
            const node = svg.querySelector(`[data-id="${id}"]`);
            const matrix = node.transform.baseVal.consolidate().matrix;
            return [matrix.e, matrix.f];
          }));
        const wide = await positions();
        assert.equal(wide[0][1], wide[1][1], 'wide layout has a horizontal client/coordinator row');
        assert.ok(wide[1][0] > wide[0][0]);
        // Test the actual container boundary independently of the viewport width.
        await flowchart.evaluate(el => { el.style.boxSizing = 'content-box'; el.style.width = '639px'; });
        assert.equal(await flowchart.locator('.doc-diagram-render--narrow svg:visible').count(), 1);
        await flowchart.evaluate(el => { el.style.width = '640px'; });
        assert.equal(await flowchart.locator('.doc-diagram-render--wide svg:visible').count(), 1);
        await flowchart.evaluate(el => { el.style.width = '320px'; });
        const narrowColumn = await positions();
        assert.equal(narrowColumn[0][0], narrowColumn[1][0], 'narrow desktop column selects vertical layout');
        assert.ok(narrowColumn[1][1] > narrowColumn[0][1]);
        await flowchart.evaluate(el => { el.style.removeProperty('width'); el.style.removeProperty('box-sizing'); });
        await page.setViewportSize({ width: 390, height: 844 });
        assert.equal(await page.locator('.doc-diagram-render--narrow svg:visible').count(), 4);
        assert.equal(await page.locator('.doc-diagram-render--wide svg:visible').count(), 0);
        assert.deepEqual(await positions(), narrowColumn, 'mobile uses the same pre-rendered narrow layout');
        const mobileLight = await flowchart.locator('svg:visible').evaluate(svg => getComputedStyle(svg).color);
        await page.evaluate(() => { document.documentElement.dataset.theme = 'dark'; });
        assert.notEqual(await flowchart.locator('svg:visible').evaluate(svg => getComputedStyle(svg).color), mobileLight);
        await page.evaluate(() => { document.documentElement.dataset.theme = 'light'; });
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'no mobile page overflow');
        const duplicateIDs = await page.evaluate(() => {
          const ids = [...document.querySelectorAll('.doc-diagram [id]')].map(el => el.id);
          return ids.length !== new Set(ids).size;
        });
        assert.equal(duplicateIDs, false, 'SVG IDs are unique across diagrams');
        await page.setViewportSize({ width: 1920, height: 960 });
      }
      assert.deepEqual(errors, []);
      await context.close();
    }
    console.log('Build-time SVGs, no-JavaScript rendering, themes, source disclosures, release inheritance and adaptive container layouts passed.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
