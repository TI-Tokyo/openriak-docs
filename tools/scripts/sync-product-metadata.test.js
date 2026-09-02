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
const readAdapter = (version) => JSON.parse(fs.readFileSync(path.join(versionsRoot, `${version}.json`), 'utf8'));
const adapterDownloads = (version) => Object.values(readAdapter(version).downloads).flat();
const downloadNamed = (version, filename) => adapterDownloads(version).find((download) => download.filename === filename);

assert.deepEqual(generatedVersions, [...legacyVersions, ...openRiakVersions].map(({ raw }) => raw).sort());

for (const { raw: version, sourceDirectory } of legacyVersions) {
  const adapter = readAdapter(version);
  assert.equal(adapter.generatedFrom, `content/openriak-kv/metadata/${version}`);
  assert.equal(adapter.metadataStatus.supportedOs, 'complete');
  assert.equal(adapter.metadataStatus.downloads, 'complete');
  assert.equal(adapter.metadataStatus.defaults, 'not_generated');
  assert.deepEqual(adapter.operatingSystems, []);
  assert.equal(adapter.defaultOs, null);
  assert.ok(adapter.downloadOperatingSystems.length > 0);
  assert.ok(Object.values(adapter.downloads).flat().length > 0);
  assert.ok(Object.values(adapter.downloads).flat().every((download) => download.checksum?.algorithm === 'sha256'));
  assert.ok(Object.values(adapter.downloads).flat().every((download) => /^[0-9a-f]{64}$/.test(download.checksum?.value || '')));
  if (version.startsWith('2.')) {
    assert.ok(Object.values(adapter.downloads).flat().every((download) => download.otp === 'R16B02'));
  } else {
    assert.ok(Object.values(adapter.downloads).flat().every((download) => download.otp !== null && download.otp !== ''));
  }
  assert.deepEqual(adapter.values, {});
  assert.equal(resolveOs('ubuntu-noble-amd64', null, adapter), null);
}

for (const { raw: version } of openRiakVersions) {
  const adapter = readAdapter(version);
  assert.equal(adapter.generatedFrom, `content/openriak-kv/metadata/${version}`);
  assert.ok(adapter.operatingSystems.length > 0);
  assert.deepEqual(adapter.downloadOperatingSystems, adapter.operatingSystems);
  assert.ok(Object.values(adapter.downloads).flat().every((download) => download.otp !== null && download.otp !== ''));
}

assert.equal(downloadNamed('3.0.1', 'riak_3.0.1-OTP20.3_amd64.deb').otp, 20);
assert.equal(downloadNamed('3.0.1', 'riak_3.0.1-OTP22.3_amd64.deb').otp, 22);
assert.equal(downloadNamed('3.2.0', 'riak_3.2.0-tiot2-OTP22_arm64.deb').otp, 22);
assert.equal(downloadNamed('3.2.0', 'riak_3.2.0-tiot2-OTP24_arm64.deb').otp, 24);
assert.equal(downloadNamed('3.2.0', 'riak_3.2.0-tiot2-OTP25_arm64.deb').otp, 25);
assert.equal(downloadNamed('3.4.1', 'riak-3.4.1.24-r1.apk').otp, 24);
assert.equal(downloadNamed('3.4.1', 'riak-3.4.1.26-r1.apk').otp, 26);

console.log('Product metadata synchronization tests passed.');
