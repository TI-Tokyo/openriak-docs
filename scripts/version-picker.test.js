'use strict';

const assert = require('node:assert/strict');
const {
  compareVersions,
  productForVersion,
  buildVersionCandidates
} = require('../static/js/version-picker.js');

assert.ok(compareVersions('1.10', '1.9') > 0, '1.10 must sort after 1.9');
assert.ok(compareVersions('3.4.1', '3.4.0') > 0, 'patch versions must sort numerically');
assert.equal(compareVersions('3.2', '3.2.0'), 0, 'missing version parts are zero');
assert.equal(productForVersion('3.4.0'), 'OpenRiak KV');
assert.equal(productForVersion('4.0.0'), 'OpenRiak KV');
assert.equal(productForVersion('3.2.5'), 'Riak KV');

assert.deepEqual(
  ['1.9', '1.10', '2.0', '1.8.12'].sort((left, right) => compareVersions(right, left)),
  ['2.0', '1.10', '1.9', '1.8.12']
);

assert.deepEqual(
  buildVersionCandidates({
    currentPath: '/docs/kv/3.4.1/how-to/configure/backends/',
    currentVersion: '3.4.1',
    targetLanding: '/docs/kv/3.2.5/',
    breadcrumbPaths: [
      '/docs/kv/3.4.1/',
      '/docs/kv/3.4.1/how-to/',
      '/docs/kv/3.4.1/how-to/configure/'
    ],
    origin: 'https://docs.example.test'
  }),
  [
    'https://docs.example.test/docs/kv/3.2.5/how-to/configure/backends/',
    'https://docs.example.test/docs/kv/3.2.5/how-to/configure/',
    'https://docs.example.test/docs/kv/3.2.5/how-to/',
    'https://docs.example.test/docs/kv/3.2.5/'
  ]
);

console.log('Version picker behavior tests passed.');
