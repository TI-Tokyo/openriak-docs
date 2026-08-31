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
  assert.equal(adapter.generatedFrom, `content/riak-kv/${sourceDirectory}`);
  assert.equal(adapter.metadataStatus.supportedOs, 'unavailable');
  assert.deepEqual(adapter.operatingSystems, []);
  assert.deepEqual(adapter.downloads, {});
  assert.equal(resolveOs('ubuntu-noble-amd64', { family: 'ubuntu' }, adapter), null);
}

for (const { raw: version } of openRiakVersions) {
  const adapter = JSON.parse(fs.readFileSync(path.join(versionsRoot, `${version}.json`), 'utf8'));
  assert.equal(adapter.generatedFrom, `content/openriak-kv/metadata/${version}`);
  assert.ok(adapter.operatingSystems.length > 0);
}

console.log('Product metadata synchronization tests passed.');
