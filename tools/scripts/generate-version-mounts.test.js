'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {
  compareSemver,
  createVersionMounts,
  generateConfig,
  generatePageProvenance,
  parseArguments,
  productSources
} = require('./generate-version-mounts.js');

const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'openriak-version-mounts-'));
const makeVersions = (product, versions) => {
  fs.mkdirSync(path.join(fixture, product), { recursive: true });
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
  makeVersions('riak-cs', ['2.1.2-new-release', '3.0.1-new-release']);
  makeVersions('openriak-cs', []);
  makeVersions('riak-ts', ['1.5.2-new-release', '3.0.0-new-release']);
  makeVersions('openriak-ts', []);

  const writePage = (relative, body) => {
    const filename = path.join(fixture, relative);
    fs.mkdirSync(path.dirname(filename), { recursive: true });
    fs.writeFileSync(filename, `---\ntitle: Test\n---\n\n${body}\n`, 'utf8');
  };
  writePage('openriak-kv/3.4.0-new-release/stable.md', 'Unchanged body.');
  writePage('openriak-kv/3.4.0-new-release/changed.md', 'Original body.');
  writePage('openriak-kv/3.4.0-new-release/whats-changed.md', 'Everything changed.');
  writePage('openriak-kv/3.4.1/changed.md', 'Updated body.');
  writePage('openriak-kv/3.4.1/new-page.md', 'New body.');

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
  assert.deepEqual(sourcesFor('content/openriak-cs/3.0.1'), ['riak-cs/3.0.1-new-release']);
  assert.deepEqual(sourcesFor('content/openriak-ts/3.0.0'), ['riak-ts/3.0.0-new-release']);
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
    'riak-cs/3.0.1-new-release'
  ]);
  assert.deepEqual(sourcesFor('content/riak-cs/latest'), [
    '../tools/generated/latest-redirects/riak-cs',
    'riak-cs/3.0.1-new-release'
  ]);

  const developmentMounts = createVersionMounts(fixture, productSources, { 'riak-kv': ['2.1.1'] });
  const developmentSourcesFor = (target) => developmentMounts
    .filter((mount) => mount.target === target)
    .map((mount) => mount.source);
  assert.deepEqual(developmentSourcesFor('content/openriak-kv/2.1.1'), [
    'riak-kv/2.1.1',
    'riak-kv/2.1.0-new-release'
  ]);
  assert.deepEqual(developmentSourcesFor('content/openriak-kv/2.0.3'), []);
  assert.deepEqual(developmentSourcesFor('content/openriak-kv/3.4.2'), [
    'openriak-kv/3.4.2',
    'openriak-kv/3.4.1',
    'openriak-kv/3.4.0-new-release'
  ]);
  assert.throws(
    () => createVersionMounts(fixture, productSources, { 'riak-kv': ['9.9.9'] }),
    /Requested version 9\.9\.9 does not exist/
  );
  assert.deepEqual(parseArguments(['--include-version', 'riak-kv=2.1.1']).includeVersions, {
    'riak-kv': ['2.1.1']
  });
  assert.deepEqual(parseArguments(['--include-latest', 'riak-cs']).includeLatest, ['riak-cs']);

  const baseConfig = path.join(fixture, 'hugo.yaml');
  const output = path.join(fixture, 'generated.yaml');
  const latestRedirectRoot = path.join(fixture, 'latest-redirects');
  const pageProvenanceRoot = path.join(fixture, 'page-provenance');
  fs.writeFileSync(baseConfig, `module:\n  mounts:\n    - {source: '../tools/generated/openriak-kv/data/versions', target: 'data/versions/openriak-kv'}\n    - {source: '../tools/generated/openriak-kv/data/configuration-reference', target: 'data/configuration-reference/openriak-kv'}\n    - {source: '../tools/generated/openriak-cs/data/versions', target: 'data/versions/openriak-cs'}\n    - {source: '../tools/generated/openriak-ts/data/versions', target: 'data/versions/openriak-ts'}\n    # GENERATED_VERSION_MOUNTS\n`, 'utf8');
  generateConfig({ contentRoot: fixture, baseConfig, output, latestRedirectRoot, pageProvenanceRoot, products: productSources });
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
  const provenance341 = JSON.parse(fs.readFileSync(path.join(pageProvenanceRoot, 'openriak-kv', '3.4.1.json'), 'utf8'));
  const provenance342 = JSON.parse(fs.readFileSync(path.join(pageProvenanceRoot, 'openriak-kv', '3.4.2.json'), 'utf8'));
  assert.deepEqual(provenance341.stable, { status: 'inherited', since: '3.4.0' });
  assert.deepEqual(provenance341.changed, { status: 'updated', since: '3.4.1' });
  assert.deepEqual(provenance341['new-page'], { status: 'new', since: '3.4.1' });
  assert.equal(provenance341['whats-changed'], undefined, "What's Changed must not have generated provenance");
  assert.deepEqual(provenance342.changed, { status: 'inherited', since: '3.4.1' });
  assert.deepEqual(provenance342['new-page'], { status: 'inherited', since: '3.4.1' });
  assert.equal(provenance342['whats-changed'], undefined, "What's Changed must remain outside generated provenance");
  const unchangedProvenanceFile = path.join(pageProvenanceRoot, 'openriak-kv', '3.4.1.json');
  const unchangedProvenanceMtime = fs.statSync(unchangedProvenanceFile).mtimeMs;
  generatePageProvenance(fixture, productSources, pageProvenanceRoot);
  assert.equal(fs.statSync(unchangedProvenanceFile).mtimeMs, unchangedProvenanceMtime, 'unchanged provenance files must not be rewritten');

  const filteredOutput = path.join(fixture, 'development.yaml');
  const filteredDataRoot = path.join(fixture, 'development-data', 'openriak-kv', 'versions');
  const filteredCsDataRoot = path.join(fixture, 'development-data', 'openriak-cs', 'versions');
  generateConfig({
    contentRoot: fixture,
    baseConfig,
    output: filteredOutput,
    latestRedirectRoot,
    pageProvenanceRoot,
    products: productSources,
    includeVersions: { 'riak-kv': ['2.1.1'] },
    versionDataRoots: {
      'openriak-kv': filteredDataRoot,
      'openriak-cs': filteredCsDataRoot
    }
  });
  const filteredConfig = fs.readFileSync(filteredOutput, 'utf8');
  assert.match(filteredConfig, new RegExp(`source: '${filteredDataRoot.replace(/\\/g, '/')}'`));
  assert.match(filteredConfig, new RegExp(`source: '${filteredCsDataRoot.replace(/\\/g, '/')}'`));
  assert.match(filteredConfig, new RegExp(`source: '${path.join(path.dirname(filteredDataRoot), 'configuration-reference').replace(/\\/g, '/')}'`));

  const latestOnlyOutput = path.join(fixture, 'latest-only.yaml');
  generateConfig({
    contentRoot: fixture,
    baseConfig,
    output: latestOnlyOutput,
    latestRedirectRoot,
    pageProvenanceRoot,
    products: productSources,
    includeLatest: ['riak-cs', 'riak-ts']
  });
  const latestOnlyConfig = fs.readFileSync(latestOnlyOutput, 'utf8');
  assert.match(latestOnlyConfig, /source: 'riak-cs\/3\.0\.1-new-release', target: 'content\/openriak-cs\/3\.0\.1'/);
  assert.doesNotMatch(latestOnlyConfig, /target: 'content\/openriak-cs\/2\.1\.2'/);
  assert.match(latestOnlyConfig, /source: 'riak-ts\/3\.0\.0-new-release', target: 'content\/openriak-ts\/3\.0\.0'/);
  assert.doesNotMatch(latestOnlyConfig, /target: 'content\/openriak-ts\/1\.5\.2'/);

  makeVersions('duplicate-product', ['1.0.0', '1.0.0-new-release']);
  assert.throws(
    () => createVersionMounts(fixture, [{ source: 'duplicate-product', target: 'duplicate-product' }]),
    /Duplicate public version 1\.0\.0/
  );
} finally {
  fs.rmSync(fixture, { recursive: true, force: true });
}

console.log('Version mount generation tests passed.');
