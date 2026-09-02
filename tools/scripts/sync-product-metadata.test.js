'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { resolveOs } = require('../../layouts/docs-theme/static/js/docs-runtime.js');
const { compareSemver, discoverVersions, productSources } = require('./generate-version-mounts.js');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const contentRoot = path.join(repositoryRoot, 'content');
const generatedRoot = path.join(repositoryRoot, 'tools', 'generated');
const versionsFor = (source) => discoverVersions(
  contentRoot,
  productSources.find((product) => product.source === source)
);
const productCases = [
  { id: 'openriak-kv', sources: ['riak-kv', 'openriak-kv'], forcedOtpMajor: '2' },
  { id: 'openriak-cs', sources: ['riak-cs', 'openriak-cs'], forcedOtpMajor: '2' },
  { id: 'openriak-ts', sources: ['riak-ts', 'openriak-ts'], forcedOtpMajor: '1' }
];

const readAdapter = (product, version) => JSON.parse(fs.readFileSync(
  path.join(generatedRoot, product, 'data', 'versions', `${version}.json`),
  'utf8'
));
const adapterDownloads = (product, version) => Object.values(readAdapter(product, version).downloads).flat();
const downloadNamed = (product, version, filename) => adapterDownloads(product, version)
  .find((download) => download.filename === filename);

for (const product of productCases) {
  const versionsRoot = path.join(generatedRoot, product.id, 'data', 'versions');
  const discoveredVersions = product.sources.flatMap(versionsFor);
  const generatedVersions = fs.readdirSync(versionsRoot)
    .filter((file) => file.endsWith('.json'))
    .map((file) => file.slice(0, -5))
    .sort();
  assert.deepEqual(generatedVersions, discoveredVersions.map(({ raw }) => raw).sort());

  for (const { raw: version } of discoveredVersions) {
    const adapter = readAdapter(product.id, version);
    const downloads = Object.values(adapter.downloads).flat();
    const modernKv = product.id === 'openriak-kv' && compareSemver(version, '3.4.0') >= 0;
    assert.equal(adapter.generatedFrom, `content/${product.id}/metadata/${version}`);
    assert.equal(adapter.metadataStatus.supportedOs, adapter.metadataStatus.downloads);
    if (modernKv) assert.ok(['complete', 'partial'].includes(adapter.metadataStatus.defaults));
    else assert.equal(adapter.metadataStatus.defaults, 'not_generated');
    if (adapter.metadataStatus.downloads === 'unavailable') {
      assert.deepEqual(adapter.downloadOperatingSystems, []);
      assert.deepEqual(downloads, []);
      continue;
    }
    assert.equal(adapter.metadataStatus.downloads, 'complete');
    assert.ok(adapter.downloadOperatingSystems.length > 0);
    assert.ok(downloads.length > 0);
    assert.ok(downloads.every((download) => download.checksum?.algorithm === 'sha256'));
    assert.ok(downloads.every((download) => /^[0-9a-f]{64}$/.test(download.checksum?.value || '')));
    if (version.startsWith(`${product.forcedOtpMajor}.`)) {
      assert.ok(downloads.every((download) => download.otp === 'R16B02'));
    }
    if (modernKv) {
      assert.ok(adapter.operatingSystems.length > 0);
      assert.ok(adapter.defaultOs);
    } else {
      assert.deepEqual(adapter.operatingSystems, []);
      assert.equal(adapter.defaultOs, null);
      assert.deepEqual(adapter.values, {});
    }
    if (product.id !== 'openriak-kv') assert.equal(resolveOs(adapter.downloadOperatingSystems[0].id, null, adapter), null);
  }
}

assert.equal(downloadNamed('openriak-kv', '3.0.1', 'riak_3.0.1-OTP20.3_amd64.deb').otp, 20);
assert.equal(downloadNamed('openriak-kv', '3.0.1', 'riak_3.0.1-OTP22.3_amd64.deb').otp, 22);
assert.equal(downloadNamed('openriak-kv', '3.2.0', 'riak_3.2.0-tiot2-OTP22_arm64.deb').otp, 22);
assert.equal(downloadNamed('openriak-kv', '3.2.0', 'riak_3.2.0-tiot2-OTP24_arm64.deb').otp, 24);
assert.equal(downloadNamed('openriak-kv', '3.2.0', 'riak_3.2.0-tiot2-OTP25_arm64.deb').otp, 25);
assert.equal(downloadNamed('openriak-kv', '3.4.1', 'riak-3.4.1.24-r1.apk').otp, 24);
assert.equal(downloadNamed('openriak-kv', '3.4.1', 'riak-3.4.1.26-r1.apk').otp, 26);

for (const product of ['openriak-cs', 'openriak-ts']) {
  for (const version of productCases.find((item) => item.id === product).sources.flatMap(versionsFor).filter(({ major }) => major === 3)) {
    assert.ok(adapterDownloads(product, version.raw).every((download) => download.otp === null || Number.isInteger(download.otp)));
  }
}

console.log('Product metadata synchronization tests passed.');
