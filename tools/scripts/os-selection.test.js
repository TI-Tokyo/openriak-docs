'use strict';

const assert = require('node:assert/strict');
const { osReleaseKey, groupOsReleases, resolveReleaseArchitecture } = require('../../layouts/docs-theme/static/js/docs-runtime');

const os = (family, version, architecture) => ({ family, version, architecture, id: `${family}-${version}-${architecture}` });
const alpine = [os('alpine', '3.21', 'aarch64'), os('alpine', '3.21', 'x86_64')];
const ubuntu = [os('ubuntu', '24.04', 'amd64'), os('ubuntu', '24.04', 'arm64')];
const newer = [os('alpine', '3.24', 'x86_64')];
const preferences = { 'alpine/3.21': 'aarch64', 'ubuntu/24.04': 'amd64' };

assert.deepEqual(groupOsReleases([...alpine, ...ubuntu, ...newer]), [alpine, ubuntu, newer]);
assert.notEqual(osReleaseKey(alpine[0]), osReleaseKey(newer[0]));
assert.equal(resolveReleaseArchitecture(alpine, preferences, 'amd64').architecture, 'aarch64');
assert.equal(resolveReleaseArchitecture(ubuntu, preferences, 'aarch64').architecture, 'amd64');
assert.equal(resolveReleaseArchitecture(ubuntu, {}, 'aarch64').architecture, 'arm64');
assert.equal(resolveReleaseArchitecture(alpine, {}, 'amd64').architecture, 'x86_64');
assert.equal(resolveReleaseArchitecture(alpine, {}).architecture, 'x86_64');
assert.equal(resolveReleaseArchitecture(alpine, {}, undefined, alpine[0].id).architecture, 'aarch64');
// Missing architectures temporarily fall back without modifying saved choices.
const before = JSON.stringify(preferences);
assert.equal(resolveReleaseArchitecture([alpine[1]], preferences).architecture, 'x86_64');
assert.equal(JSON.stringify(preferences), before);
assert.equal(resolveReleaseArchitecture(alpine, preferences).architecture, 'aarch64');
assert.equal(resolveReleaseArchitecture([], preferences), null);
console.log('OS release grouping and independent architecture preference tests passed.');
