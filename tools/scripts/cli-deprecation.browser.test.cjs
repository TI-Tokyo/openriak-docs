'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const {buildAnnotatedReference} = require('./cli-annotations');
(async () => {
  const browser = await chromium.launch({executablePath: process.env.OPENRIAK_BROWSER_EXECUTABLE});
  try {
    const page = await browser.newPage();
    const root = process.env.OPENRIAK_DOCS_TEST_URL || 'http://localhost:1410/docs/openriak-kv/';
    let checked = 0;
    for (const version of ['3.4.0', '3.4.1']) {
      const reference = buildAnnotatedReference(require(`../../content/openriak-kv/metadata/${version}/kv-cli-commands.json`));
      for (const command of reference.pages.filter(p => p.deprecated)) {
        assert.equal((await page.goto(`${root}${version}/reference/commands/${command.route}/`)).status(), 200);
        const warning = page.locator('.cli-command-reference > .admonition.warning');
        assert.equal(await warning.count(), 1, command.key);
        assert.equal(await warning.locator('.admonition-header').innerText(), 'Deprecated Command');
        assert.equal(await warning.locator('strong').innerText(), 'Do not use it');
        assert.match(await warning.innerText(), /This command may be removed in future versions\./);
        assert.ok(await warning.evaluate(e => {
          const toc = document.querySelector('.doc-table-of-contents');
          const summary = document.querySelector('.cli-summary');
          return Boolean(toc.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING)
            && Boolean(e.compareDocumentPosition(summary) & Node.DOCUMENT_POSITION_FOLLOWING);
        }), 'TOC, warning, summary order');
        const links = await warning.locator('a').evaluateAll(es => es.map(e => e.href));
        assert.ok(links.length, command.key + ': replacement links');
        for (const link of links) {
          assert.ok(link.includes(`/openriak-kv/${version}/reference/commands/`), link);
          assert.equal((await page.request.get(link)).status(), 200, link);
        }
        checked++;
      }
      await page.goto(`${root}${version}/reference/commands/riak/admin/cluster/join/`);
      assert.equal(await page.locator('.cli-command-reference > .admonition.warning').count(), 0);
    }
    console.log(`Deprecation warnings and replacement links verified on ${checked} pages across both releases.`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
