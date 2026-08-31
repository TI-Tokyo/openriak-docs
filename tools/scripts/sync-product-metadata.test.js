'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { resolveOs } = require('../../layouts/docs-theme/static/js/docs-runtime.js');
const { discoverVersions, productSources } = require('./generate-version-mounts.js');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const versionsRoot = path.join(repositoryRoot, 'tools', 'generated', 'openriak-kv', 'data', 'versions');
const contentRoot = path.join(repositoryRoot, 'content');
const versionsFor = (source) => discoverVersions(
  contentRoot,
  productSources.find((product) => product.source === source)
);
const legacyVersions = versionsFor('riak-kv');
const openRiakVersions = versionsFor('openriak-kv');
const generatedVersions = fs.readdirSync(versionsRoot)
  .filter((file) => file.endsWith('.json'))
  .map((file) => file.slice(0, -5))
  .sort();

assert.deepEqual(generatedVersions, [...legacyVersions, ...openRiakVersions].map(({ raw }) => raw).sort());

for (const { raw: version, sourceDirectory } of legacyVersions) {
  const adapter = JSON.parse(fs.readFileSync(path.join(versionsRoot, `${version}.json`), 'utf8'));
  assert.equal(adapter.generatedFrom, `content/openriak-kv/metadata/${version}`);
  assert.equal(adapter.metadataStatus.supportedOs, 'complete');
  assert.equal(adapter.metadataStatus.downloads, 'complete');
  assert.equal(adapter.metadataStatus.defaults, 'not_generated');
  assert.deepEqual(adapter.operatingSystems, []);
  assert.equal(adapter.defaultOs, null);
  assert.ok(adapter.downloadOperatingSystems.length > 0);
  assert.ok(Object.values(adapter.downloads).flat().length > 0);
  assert.deepEqual(adapter.values, {});
  assert.equal(resolveOs('ubuntu-noble-amd64', null, adapter), null);
}

for (const { raw: version } of openRiakVersions) {
  const adapter = JSON.parse(fs.readFileSync(path.join(versionsRoot, `${version}.json`), 'utf8'));
  assert.equal(adapter.generatedFrom, `content/openriak-kv/metadata/${version}`);
  assert.ok(adapter.operatingSystems.length > 0);
  assert.deepEqual(adapter.downloadOperatingSystems, adapter.operatingSystems);
}

console.log('Product metadata synchronization tests passed.');
