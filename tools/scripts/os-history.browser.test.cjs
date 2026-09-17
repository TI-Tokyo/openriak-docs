'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const { chromium } = require('playwright');

const systems = [
  { id: 'ubuntu-amd64', family: 'ubuntu', version: '24.04', architecture: 'amd64', displayName: 'Ubuntu 24.04' },
  { id: 'alpine-x86_64', family: 'alpine', version: '3.21', architecture: 'x86_64', displayName: 'Alpine 3.21' },
  { id: 'alpine-aarch64', family: 'alpine', version: '3.21', architecture: 'aarch64', displayName: 'Alpine 3.21' }
].map(os => ({ ...os, name: os.family, logo: 'os.svg' }));
const version = {
  version: '3.4.1', defaultOs: systems[0].id, operatingSystems: systems,
  values: Object.fromEntries(systems.map(os => [os.id, { example: os.id }]))
};
const context = { product: { id: 'openriak-kv' }, currentVersion: version.version, versions: [version], assetBase: '/' };
const runtime = fs.readFileSync(path.join(__dirname, '../../layouts/docs-theme/static/js/docs-runtime.js'));
const html = `<!doctype html><html><body>
  <script id="docs-context" type="application/json">${JSON.stringify(context)}</script>
  <script>
    window.OpenRiakMetadata = { read: async node => JSON.parse(node.textContent) };
    window.addEventListener('pageshow', event => { window.restoredFromCache = event.persisted; });
  </script>
  <div data-os-control>
    <button data-os-trigger><img data-os-logo alt=""><span data-os-label></span></button>
    <div data-os-picker hidden></div>
  </div>
  ${systems.map(os => `<button data-download-os-select="${os.id}">${os.displayName}</button>
    <div data-download-panel-os="${os.id}">${os.id}</div>`).join('')}
  <div data-download-architecture-picker><ul data-download-architecture-options></ul></div>
  <span data-doc-value="example"></span>
  <span data-selected-download-os></span>
  <div data-configuration-reference>
    <script type="application/json" data-configuration-reference-defaults>${JSON.stringify({ example:
      Object.fromEntries(systems.map(os => [os.id, { hasDefault: true, value: os.id }])) })}</script>
    <div data-configuration-key="example"><span data-configuration-default-value></span></div>
  </div>
  <a href="/downloads">Downloads</a>
  <script src="/runtime.js"></script>
</body></html>`;

(async () => {
  const server = http.createServer((request, response) => {
    response.setHeader('Content-Type', request.url === '/runtime.js' ? 'text/javascript' : 'text/html');
    response.end(request.url === '/runtime.js' ? runtime : html);
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  try {
    browser = await chromium.launch({
      executablePath: process.env.OPENRIAK_BROWSER_EXECUTABLE || undefined,
      // Playwright normally disables the cache this regression needs to exercise.
      ignoreDefaultArgs: ['--disable-back-forward-cache']
    });
    const page = await browser.newPage();
    page.setDefaultTimeout(10000);
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
    const checkOs = async id => {
      await page.waitForFunction(expected => document.documentElement.dataset.selectedOs === expected, id);
      const os = systems.find(candidate => candidate.id === id);
      assert.equal(await page.locator('[data-os-label]').textContent(), os.displayName);
      assert.equal(await page.locator('[data-selected-download-os]').textContent(), os.displayName);
      assert.equal(await page.locator('[data-doc-value]').textContent(), id);
      assert.equal(await page.locator('[data-configuration-default-value]').textContent(), id);
      assert.equal(await page.locator(`[data-download-panel-os="${id}"]`).isVisible(), true);
      assert.equal(await page.locator('[data-download-panel-os]:visible').count(), 1);
      assert.equal(await page.locator(`[data-download-architecture-select="${id}"]`).getAttribute('aria-pressed'), 'true');
      assert.equal(await page.evaluate(() => localStorage.getItem('openriak-docs-os:openriak-kv')), id);
    };
    await page.goto(`http://127.0.0.1:${server.address().port}/guide?os=alpine-x86_64`);
    await checkOs('alpine-x86_64');
    assert.equal(new URL(page.url()).searchParams.has('os'), false);
    await page.getByRole('link', { name: 'Downloads' }).click();
    await checkOs('alpine-x86_64');
    await page.locator('[data-download-os-select="ubuntu-amd64"]').click();
    await checkOs('ubuntu-amd64');
    await page.goBack({ waitUntil: 'commit' });
    assert.equal(await page.evaluate(() => window.restoredFromCache), true, 'Back must restore a cached document');
    await checkOs('ubuntu-amd64');

    // Forward must also refresh, including architecture choices saved on the other page.
    await page.locator('[data-download-os-select="alpine-x86_64"]').click();
    await page.locator('[data-download-architecture-select="alpine-aarch64"]').click();
    await checkOs('alpine-aarch64');
    await page.goForward({ waitUntil: 'commit' });
    assert.equal(await page.evaluate(() => window.restoredFromCache), true, 'Forward must restore a cached document');
    await checkOs('alpine-aarch64');
    await page.goBack({ waitUntil: 'commit' });
    await checkOs('alpine-aarch64');
    assert.deepEqual(errors, []);
    console.log('Browser back/forward restores the saved OS, architecture, picker, downloads, values, and configuration defaults.');
  } finally {
    await browser?.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
