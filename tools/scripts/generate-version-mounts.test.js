'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {
  compareSemver,
  createVersionMounts,
  generateConfig,
  productSources
} = require('./generate-version-mounts.js');

const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'openriak-version-mounts-'));
const makeVersions = (product, versions) => {
  for (const version of versions) fs.mkdirSync(path.join(fixture, product, version), { recursive: true });
};

try {
  makeVersions('riak-kv', [
    '2.0.0-new-release',
    '2.0.1',
    '2.0.2',
    '2.0.3',
    '2.1.0-new-release',
    '2.1.1',
    '2.2.0-new-release',
    '2.2.1-new-release'
  ]);
  makeVersions('openriak-kv', ['3.4.0-new-release', '3.4.1', '3.4.2']);
  makeVersions('openriak-cs', ['2.1.3-new-release', '2.1.4']);
  makeVersions('openriak-ts', ['1.5.2-new-release']);

  const mounts = createVersionMounts(fixture, productSources);
  const sourcesFor = (target) => mounts.filter((mount) => mount.target === target).map((mount) => mount.source);

  assert.deepEqual(sourcesFor('content/openriak-kv/2.0.3'), [
    'riak-kv/2.0.3',
    'riak-kv/2.0.2',
    'riak-kv/2.0.1',
    'riak-kv/2.0.0-new-release'
  ]);
  assert.deepEqual(sourcesFor('content/openriak-kv/2.1.0'), [
    'riak-kv/2.1.0-new-release'
  ]);
  assert.deepEqual(sourcesFor('content/openriak-kv/2.1.1'), [
    'riak-kv/2.1.1',
    'riak-kv/2.1.0-new-release'
  ]);
  assert.deepEqual(sourcesFor('content/openriak-kv/2.2.0'), [
    'riak-kv/2.2.0-new-release'
  ]);
  assert.deepEqual(sourcesFor('content/openriak-kv/2.2.1'), [
    'riak-kv/2.2.1-new-release'
  ]);
  assert.deepEqual(sourcesFor('content/openriak-kv/3.4.2'), [
    'openriak-kv/3.4.2',
    'openriak-kv/3.4.1',
    'openriak-kv/3.4.0-new-release'
  ]);
  assert.deepEqual(sourcesFor('content/openriak-cs/2.1.4'), [
    'openriak-cs/2.1.4',
    'openriak-cs/2.1.3-new-release'
  ]);
  assert.deepEqual(sourcesFor('content/openriak-ts/1.5.2'), ['openriak-ts/1.5.2-new-release']);
  assert.ok(sourcesFor('content/openriak-kv/3.4.2').every((source) => source.startsWith('openriak-kv/')));
  assert.ok(sourcesFor('content/openriak-kv/2.2.1').every((source) => source.startsWith('riak-kv/')));
  assert.ok(compareSemver('3.10.0', '3.9.9') > 0);
  assert.deepEqual(sourcesFor('content/openriak-kv/latest'), [
    '../tools/generated/latest-redirects/openriak-kv',
    'openriak-kv/3.4.2',
    'openriak-kv/3.4.1',
    'openriak-kv/3.4.0-new-release'
  ]);
  assert.deepEqual(sourcesFor('content/riak-kv/latest'), [
    '../tools/generated/latest-redirects/riak-kv',
    'openriak-kv/3.4.2',
    'openriak-kv/3.4.1',
    'openriak-kv/3.4.0-new-release'
  ]);
  assert.deepEqual(sourcesFor('content/riak-kv'), [
    '../tools/generated/latest-redirects/riak-kv-section'
  ]);
  assert.deepEqual(sourcesFor('content/openriak-cs/latest'), [
    '../tools/generated/latest-redirects/openriak-cs',
    'openriak-cs/2.1.4',
    'openriak-cs/2.1.3-new-release'
  ]);

  const baseConfig = path.join(fixture, 'hugo.yaml');
  const output = path.join(fixture, 'generated.yaml');
  const latestRedirectRoot = path.join(fixture, 'latest-redirects');
  fs.writeFileSync(baseConfig, `module:\n  mounts:\n    # GENERATED_VERSION_MOUNTS\n`, 'utf8');
  generateConfig({ contentRoot: fixture, baseConfig, output, latestRedirectRoot, products: productSources });
  const generated = fs.readFileSync(output, 'utf8');
  assert.match(generated, /source: 'openriak-kv\/3\.4\.0-new-release', target: 'content\/openriak-kv\/3\.4\.2'/);
  assert.doesNotMatch(generated, /target: 'content\/openriak-kv\/[^']*-new-release'/);
  assert.match(generated, /source: '\.\.\/tools\/generated\/latest-redirects\/riak-kv', target: 'content\/riak-kv\/latest'/);
  const legacyLatestRoot = fs.readFileSync(path.join(latestRedirectRoot, 'riak-kv', '_index.md'), 'utf8');
  assert.match(legacyLatestRoot, /latest_redirect_product: openriak-kv/);
  assert.match(legacyLatestRoot, /latest_redirect_version: 3\.4\.2/);
  const legacySectionRoot = fs.readFileSync(path.join(latestRedirectRoot, 'riak-kv-section', '_index.md'), 'utf8');
  assert.match(legacySectionRoot, /outputs: \[\]/);
  assert.match(legacySectionRoot, /render: never/);

  makeVersions('duplicate-product', ['1.0.0', '1.0.0-new-release']);
  assert.throws(
    () => createVersionMounts(fixture, [{ source: 'duplicate-product', target: 'duplicate-product' }]),
    /Duplicate public version 1\.0\.0/
  );
} finally {
  fs.rmSync(fixture, { recursive: true, force: true });
}

console.log('Version mount generation tests passed.');
