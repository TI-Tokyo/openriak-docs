'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const { generatePageProvenance, productSources } = require('./generate-version-mounts.js');
const { isRelevantChange, watchPageProvenance } = require('./watch-page-provenance.js');

const waitFor = async (predicate, timeoutMs = 3000) => {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (predicate()) return;
    await new Promise((resolve) => setTimeout(resolve, 25));
  }
  throw new Error('Timed out waiting for page provenance to regenerate');
};

test('recognises Markdown edits and all rename events', () => {
  assert.equal(isRelevantChange('change', 'page.md'), true);
  assert.equal(isRelevantChange('change', 'PAGE.MD'), true);
  assert.equal(isRelevantChange('change', 'image.svg'), false);
  assert.equal(isRelevantChange('rename', 'new-directory'), true);
});

test('regenerates provenance when a page is added', async () => {
  const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'openriak-provenance-watch-'));
  const contentRoot = path.join(fixture, 'content');
  const outputRoot = path.join(fixture, 'page-provenance');
  let watcher;
  try {
    for (const source of new Set(productSources.map((product) => product.source))) {
      fs.mkdirSync(path.join(contentRoot, source), { recursive: true });
    }
    const releaseRoot = path.join(contentRoot, 'openriak-kv', '3.4.1');
    fs.mkdirSync(releaseRoot, { recursive: true });
    fs.writeFileSync(path.join(releaseRoot, '_index.md'), '---\ntitle: OpenRiak KV\n---\n', 'utf8');
    generatePageProvenance(contentRoot, productSources, outputRoot);
    watcher = watchPageProvenance({ contentRoot, outputRoot, debounceMs: 20 });

    fs.writeFileSync(path.join(releaseRoot, 'new-page.md'), '---\ntitle: New page\n---\n\nNew.\n', 'utf8');
    const output = path.join(outputRoot, 'openriak-kv', '3.4.1.json');
    await waitFor(() => {
      try {
        return JSON.parse(fs.readFileSync(output, 'utf8'))['new-page']?.status === 'new';
      } catch (_) {
        return false;
      }
    });
  } finally {
    watcher?.close();
    fs.rmSync(fixture, { recursive: true, force: true });
  }
});
