'use strict';
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const base = process.env.OPENRIAK_SETTINGS_TEST_BASE || 'http://127.0.0.1:1410/docs/';

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.OPENRIAK_BROWSER_EXECUTABLE || undefined });
  try {
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const url = new URL('settings/search/', base).href;
    const ready = () => page.locator('[data-search-all="highlight"]').waitFor();
    await page.goto(url); await ready();
    const read = () => page.evaluate(() => Object.fromEntries(window.OpenRiakSearchPreferences.sections.map(section => [section.id, window.OpenRiakSearchPreferences.read(section.id)])));
    const first = Object.keys(await read())[0];
    // A bulk change must preserve each row's timing and the other columns.
    await page.evaluate(id => window.OpenRiakSearchPreferences.write(id, { timing: 'together' }), first);
    await page.reload(); await ready();
    for (const [type, name] of [['text', 'text search'], ['semantic', 'semantic search'], ['highlight', 'result highlighting']]) {
      const all = page.getByRole('checkbox', { name: `All sections: ${name}`, exact: true });
      const rows = page.locator(`.settings-search-table tbody input[aria-label$=": ${name}"]`);
      assert.equal(await rows.count(), Object.keys(await read()).length);
      assert.equal(await all.isChecked(), true);
      await rows.first().uncheck();
      assert.equal(await all.evaluate(input => input.indeterminate), true);
      await all.focus(); await page.keyboard.press('Space');
      assert.equal(await all.evaluate(input => input.indeterminate), false);
      assert.ok((await rows.evaluateAll(inputs => inputs.map(input => input.checked))).every(Boolean));
      const before = await read();
      const notices = await page.locator('.settings-notice').count();
      await all.uncheck();
      assert.equal(await page.locator('.settings-notice').count(), notices + 1);
      const after = await read();
      for (const [id, values] of Object.entries(before)) assert.deepEqual(after[id], { ...values, [type]: false });
      assert.ok((await rows.evaluateAll(inputs => inputs.map(input => input.checked))).every(value => !value));
      await page.reload(); await ready();
      assert.equal(await all.isChecked(), false);
      assert.equal(await all.evaluate(input => input.indeterminate), false);
      assert.deepEqual(await read(), after);
      await all.check();
      await page.reload(); await ready();
      assert.equal(await all.isChecked(), true);
    }
    assert.deepEqual(errors, []);
    console.log('Search column toggles: bulk changes, mixed states, keyboard use, persistence and independent preferences passed.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
