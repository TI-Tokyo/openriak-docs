'use strict';

const assert = require('node:assert/strict');
const { defaultsByOs } = require('./defaults-by-os');
const { resolveValue, configurationDefaultForOs } = require('../../layouts/docs-theme/static/js/docs-runtime');

const alpine = { ring_size: { has_default: true, value: 64 } };
const targets = [
  { id: 'alpine-3.21-x86_64', family: 'alpine' },
  { id: 'alpine-3.21-aarch64', family: 'alpine' },
  { id: 'alpine-3.24-x86_64', family: 'alpine' }
];
const old = { schema_version: 1, effective_defaults: {
  'alpine-3.21-x86_64': alpine, 'alpine-3.21-aarch64': structuredClone(alpine)
} };
assert.deepEqual(defaultsByOs(old, targets), { alpine });
assert.deepEqual(defaultsByOs({ schema_version: 2, defaults_scope: 'os', effective_defaults: { alpine } }, targets), { alpine });
assert.throws(() => defaultsByOs({ ...old, effective_defaults: {
  ...old.effective_defaults, 'alpine-3.21-aarch64': { ring_size: { has_default: true, value: 128 } }
} }, targets), /Conflicting defaults/);
assert.throws(() => defaultsByOs({ schema_version: 3 }, targets), /Unsupported defaults/);

const version = { product: 'openriak-kv', version: '3.4.1',
  operatingSystems: targets.map(os => ({ ...os, defaultsKey: os.family })),
  values: { alpine: { ring_size: 64 } } };
for (const os of version.operatingSystems) {
  assert.equal(resolveValue(version, os.id, 'ring_size'), 64);
  assert.equal(configurationDefaultForOs({ alpine: { hasDefault: true, value: 64 } }, os.defaultsKey).value, '64');
}
// Package aliases use the source OS defaults without duplicating their data.
version.operatingSystems.push({ id: 'rocky-9-x86_64', family: 'rocky', defaultsKey: 'rhel' });
version.values.rhel = { ring_size: 32 };
assert.equal(resolveValue(version, 'rocky-9-x86_64', 'ring_size'), 32);
console.log('OS defaults migration and new-release lookup tests passed.');
