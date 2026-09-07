'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');
const source = fs.readFileSync(path.join(__dirname, '../../layouts/docs-theme/static/js/metadata.js'), 'utf8');

function loader(fetch) {
  const window = { location: { origin: 'https://docs.example' } };
  vm.runInNewContext(source, { window, document: { baseURI: 'https://docs.example/docs/page/' }, URL, fetch });
  return window.OpenRiakMetadata;
}

test('equivalent URLs and concurrent consumers share one cached JSON request', async () => {
  const calls = [];
  const value = { versions: [{ version: '3.4.1' }] };
  const metadata = loader(async (url, options) => {
    calls.push({ url, options });
    return { ok: true, json: async () => value };
  });
  const first = metadata.load('/docs/metadata/hash.json');
  const second = metadata.read({ dataset: { jsonSrc: 'https://docs.example/docs/metadata/hash.json' } });
  assert.equal(first, second);
  assert.equal(await first, value);
  assert.equal(await metadata.load('/docs/metadata/hash.json'), value);
  assert.equal(calls.length, 1);
  assert.equal(calls[0].options.cache, 'force-cache');
  assert.equal(calls[0].options.credentials, 'same-origin');
  await metadata.load('/docs/metadata/changed-hash.json');
  assert.equal(calls.length, 2, 'changed content must use a fresh cache entry');
});

for (const failure of ['http', 'network', 'json']) {
  test(`${failure} failures can be retried`, async () => {
    let calls = 0;
    const metadata = loader(async () => {
      if (calls++ === 0) {
        if (failure === 'network') throw new Error('Offline');
        return { ok: failure !== 'http', status: 404, json: async () => { throw new Error('Invalid JSON'); } };
      }
      return { ok: true, json: async () => 'recovered' };
    });
    await assert.rejects(metadata.load('/docs/metadata/hash.json'));
    assert.equal(await metadata.load('/docs/metadata/hash.json'), 'recovered');
    assert.equal(calls, 2);
  });
}

test('helpers stay same-origin and older inline pages remain readable', async () => {
  let calls = 0;
  const metadata = loader(async () => { calls++; });
  await assert.rejects(metadata.load('https://other.example/metadata.json'), /same-origin/);
  assert.equal(await metadata.read({ dataset: {}, textContent: '"raw code\\n"' }), 'raw code\n');
  assert.equal(calls, 0);
});
