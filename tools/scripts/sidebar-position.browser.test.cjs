'use strict';
const assert = require('node:assert/strict');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.OPENRIAK_BROWSER_EXECUTABLE || undefined });
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await context.newPage();
    const base = process.env.OPENRIAK_DOCS_TEST_URL || 'http://localhost:1410/docs/openriak-kv/';
    const catalogue = version => `${base}${version}/reference/configuration/all-configuration-settings-and-defaults/`;
    const top = () => page.locator('#docs-sidebar').evaluate(el => el.scrollTop);
    const setTop = async value => {
      await page.locator('#docs-sidebar').evaluate((el, value) => { el.scrollTop = value; }, value);
      await page.waitForFunction(value => document.querySelector('#docs-sidebar').scrollTop === value, value);
    };
    const near = async expected => assert.ok(Math.abs(await top() - expected) <= 1, `Expected sidebar offset ${expected}, got ${await top()}`);
    const currentVisible = async () => assert.ok(await page.locator('#docs-sidebar').evaluate(sidebar => {
      const bounds = sidebar.getBoundingClientRect();
      const item = sidebar.querySelector('.sidebar-page-tree [aria-current="page"]').getBoundingClientRect();
      return item.top >= bounds.top - 1 && item.bottom <= bounds.bottom + 1;
    }), 'The current page must be visible after a version switch');

    await page.goto(catalogue('3.4.1'));
    const extraBranch = page.locator('[data-nav-tree-toggle][aria-expanded="false"]').first();
    const branchId = await extraBranch.getAttribute('aria-controls');
    await extraBranch.click();
    const destination = page.locator('.sidebar-page-tree a').filter({ hasText: 'Configuration files, syntax, and precedence' }).first();
    const destinationURL = await destination.getAttribute('href');
    await destination.scrollIntoViewIfNeeded();
    const beforeClick = await top();
    assert.ok(beforeClick > 0);
    await destination.click();
    await page.waitForURL(url => url.pathname === destinationURL);
    await near(beforeClick);
    assert.equal(await page.locator(`[aria-controls="${branchId}"]`).getAttribute('aria-expanded'), 'true');

    await setTop(300);
    await page.reload();
    await near(300);
    await page.goto(catalogue('3.4.1'));
    await near(300);
    await setTop(450);
    await page.goBack();
    await near(450);
    await page.goForward();
    await near(450);

    await setTop(300);
    await page.goto(catalogue('3.4.0'));
    await currentVisible();
    await setTop(200);
    await page.goto(catalogue('3.4.1'));
    await currentVisible();
    const restoredVersionTop = await top();

    // Switching back through the real picker must leave an already-visible item alone.
    await page.goto(catalogue('3.4.0'));
    await page.locator('[data-version-picker] .picker-trigger').click();
    await page.getByRole('button', { name: '3.4.1', exact: true }).click();
    await page.waitForURL(catalogue('3.4.1'));
    await currentVisible();
    await near(restoredVersionTop);
    assert.equal(await page.evaluate(() => window.scrollY), 0, 'Revealing a menu item must not scroll the document');

    // A saved offset below the current item must be corrected upward too.
    await page.evaluate(() => {
      const key = 'openriak-sidebar-position:' + document.querySelector('[data-index-url]').dataset.indexUrl.replace('/3.4.1/', '/3.4.0/');
      const saved = JSON.parse(sessionStorage.getItem(key));
      saved.top = 1000000;
      sessionStorage.setItem(key, JSON.stringify(saved));
    });
    await page.goto(catalogue('3.4.0'));
    await currentVisible();
    await page.goto(catalogue('3.4.1'));
    await near(restoredVersionTop);

    await page.locator('[data-sidebar-collapse]').evaluate(el => el.click());
    await page.reload();
    await page.locator('[data-sidebar-expand]').click();
    await near(restoredVersionTop);

    await page.setViewportSize({ width: 390, height: 844 });
    await page.locator('[data-nav-toggle]').click();
    await setTop(250);
    await page.reload();
    await page.locator('[data-nav-toggle]').click();
    await near(250);
    await page.goto(catalogue('3.4.0'));
    await page.locator('[data-nav-toggle]').click();
    await currentVisible();

    const otherTab = await context.newPage();
    await otherTab.goto(catalogue('3.4.1'));
    assert.equal(await otherTab.locator('#docs-sidebar').evaluate(el => el.scrollTop), 0);

    const restricted = await context.newPage();
    const errors = [];
    restricted.on('pageerror', error => errors.push(error.message));
    await restricted.addInitScript(() => {
      Object.defineProperty(window, 'sessionStorage', {
        get() { throw new DOMException('Storage unavailable', 'SecurityError'); }
      });
    });
    await restricted.goto(catalogue('3.4.1'));
    const toggle = restricted.locator('[data-nav-tree-toggle]').first();
    const previous = await toggle.getAttribute('aria-expanded');
    await toggle.click();
    assert.notEqual(await toggle.getAttribute('aria-expanded'), previous);
    assert.deepEqual(errors, []);
    console.log('Sidebar position survives navigation, reload, history, collapse, and mobile reopening; versions and tabs remain independent.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
