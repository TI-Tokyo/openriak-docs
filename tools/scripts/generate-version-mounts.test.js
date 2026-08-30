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
  makeVersions('riak-kv', ['2.0.0', '3.2.4', '3.2.5']);
  makeVersions('openriak-kv', ['3.4.0', '3.4.1', '3.4.2']);
  makeVersions('openriak-cs', ['2.1.3', '2.1.4']);
  makeVersions('openriak-ts', ['1.5.2']);

  const mounts = createVersionMounts(fixture, productSources);
  const sourcesFor = (target) => mounts.filter((mount) => mount.target === target).map((mount) => mount.source);

  assert.deepEqual(sourcesFor('content/openriak-kv/3.4.2'), [
    'openriak-kv/3.4.2',
    'openriak-kv/3.4.1',
    'openriak-kv/3.4.0'
  ]);
  assert.deepEqual(sourcesFor('content/openriak-kv/3.2.5'), [
    'riak-kv/3.2.5',
    'riak-kv/3.2.4',
    'riak-kv/2.0.0'
  ]);
  assert.deepEqual(sourcesFor('content/openriak-cs/2.1.4'), [
    'openriak-cs/2.1.4',
    'openriak-cs/2.1.3'
  ]);
  assert.deepEqual(sourcesFor('content/openriak-ts/1.5.2'), ['openriak-ts/1.5.2']);
  assert.ok(sourcesFor('content/openriak-kv/3.4.2').every((source) => source.startsWith('openriak-kv/')));
  assert.ok(sourcesFor('content/openriak-kv/3.2.5').every((source) => source.startsWith('riak-kv/')));
  assert.ok(compareSemver('3.10.0', '3.9.9') > 0);

  const baseConfig = path.join(fixture, 'hugo.yaml');
  const output = path.join(fixture, 'generated.yaml');
  fs.writeFileSync(baseConfig, `module:\n  mounts:\n    # GENERATED_VERSION_MOUNTS\n`, 'utf8');
  generateConfig({ contentRoot: fixture, baseConfig, output, products: productSources });
  const generated = fs.readFileSync(output, 'utf8');
  assert.match(generated, /source: 'openriak-kv\/3\.4\.2', target: 'content\/openriak-kv\/3\.4\.2'/);
  assert.doesNotMatch(generated, /source: 'riak-kv\/3\.2\.5', target: 'content\/openriak-kv\/3\.4\.2'/);
} finally {
  fs.rmSync(fixture, { recursive: true, force: true });
}

console.log('Version mount generation tests passed.');
