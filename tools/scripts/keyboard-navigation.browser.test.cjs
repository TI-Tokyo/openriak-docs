'use strict';

const assert = require('node:assert/strict');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.OPENRIAK_BROWSER_EXECUTABLE || undefined });
  try {
    const page = await browser.newPage();
    const base = process.env.OPENRIAK_KEYBOARD_TEST_BASE || 'http://localhost:1410/docs/openriak-kv/3.4.0/';
    await page.goto(`${base}reference/data/buckets-and-bucket-types/`);
    await page.evaluate(() => window.OpenRiakPageToolsReady);
    await page.locator('[data-os-picker] .os-option').first().waitFor({ state: 'attached' });

    // The skip link remains available with Tab, but must not linger after Ctrl+Home.
    await page.keyboard.press('Tab');
    assert.equal(await page.locator('.skip-link').evaluate(element => document.activeElement === element), true);
    assert.ok(await page.locator('.skip-link').evaluate(element => element.getBoundingClientRect().top >= 0));
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.keyboard.press('Control+Home');
    await page.waitForFunction(() => window.scrollY === 0 && !document.querySelector('.skip-link').matches(':focus'));
    assert.ok(await page.locator('.skip-link').evaluate(element => element.getBoundingClientRect().bottom <= 0));
    await page.locator('.skip-link').focus();
    await page.keyboard.press('Enter');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'main-content');

    const checkPageEnds = async () => {
      for (let repetition = 0; repetition < 2; repetition += 1) {
        await page.keyboard.press('Control+Home');
        await page.waitForFunction(() => window.scrollY === 0);
        await page.keyboard.press('Control+End');
        await page.waitForFunction(() => {
          const scroller = document.scrollingElement;
          return scroller.scrollHeight > scroller.clientHeight
            && Math.abs(scroller.scrollHeight - scroller.clientHeight - scroller.scrollTop) <= 1;
        });
      }
    };
    await checkPageEnds();

    const checkKeys = async selector => {
      const control = page.locator(selector).first();
      for (const key of ['Home', 'End']) {
        for (const modifier of ['ctrlKey', 'metaKey', 'altKey']) {
          const result = await control.evaluate((element, { key, modifier }) => {
            element.focus({ preventScroll: true });
            const event = new KeyboardEvent('keydown', { key, [modifier]: true, bubbles: true, cancelable: true });
            element.dispatchEvent(event);
            return { prevented: event.defaultPrevented, sameFocus: document.activeElement === element };
          }, { key, modifier });
          const pageNavigation = modifier !== 'altKey';
          assert.deepEqual(result, { prevented: pageNavigation, sameFocus: true }, `${selector}: ${modifier}+${key}`);
        }
        const prevented = await control.evaluate((element, key) => {
          const event = new KeyboardEvent('keydown', { key, bubbles: true, cancelable: true });
          element.dispatchEvent(event);
          return event.defaultPrevented;
        }, key);
        assert.equal(prevented, true, `${selector}: plain ${key} still navigates the control`);
      }
    };

    await checkKeys('.doc-code-tab-list [role="tab"]');
    const tab = page.locator('.doc-code-tab-list [role="tab"]').first();
    await tab.evaluate(element => { element.focus({ preventScroll: true }); window.scrollTo(0, document.body.scrollHeight); });
    await page.keyboard.press('Control+Home');
    await page.waitForFunction(() => window.scrollY === 0);
    await checkPageEnds();

    await page.locator('[data-os-trigger]').click();
    await checkKeys('[data-os-picker] .os-option');
    await page.keyboard.press('Escape');
    await page.locator('.share-trigger').click();
    await checkKeys('[data-share-panel] [role="menuitem"]:visible');
    await page.keyboard.press('Escape');
    await page.evaluate(() => {
      const editor = document.createElement('textarea');
      editor.id = 'keyboard-test-editor';
      editor.style.cssText = 'position:fixed;top:200px;left:350px';
      editor.value = 'First line\nSecond line';
      document.body.append(editor);
      editor.focus();
      editor.setSelectionRange(editor.value.length, editor.value.length);
      window.scrollTo(0, 800);
    });
    await page.keyboard.press('Control+Home');
    assert.equal(await page.locator('#keyboard-test-editor').evaluate(el => el.selectionStart), 0);
    assert.ok(await page.evaluate(() => window.scrollY > 0), 'Text editing must not force the page to its top');
    const editorScroll = await page.evaluate(() => window.scrollY);
    await page.keyboard.press('Control+End');
    assert.equal(await page.locator('#keyboard-test-editor').evaluate(el => el.selectionStart === el.value.length), true);
    assert.equal(await page.evaluate(() => window.scrollY), editorScroll, 'Text editing must not force the page to its bottom');
    console.log('Repeated Ctrl+Home/End navigation reaches both document ends; skip links, widgets, and text editing still work.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
