'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { watchDockerMetadata } = require('./watch-docker-metadata');
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
(async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'openriak-docker-metadata-test-'));
  const source = path.join(root, 'source');
  const target = path.join(root, 'target');
  fs.mkdirSync(source); fs.mkdirSync(target);
  const filename = '3.4.1.json';
  const from = path.join(source, filename), to = path.join(target, filename);
  const write = (file, value) => fs.writeFileSync(file, JSON.stringify(value));
  const read = () => JSON.parse(fs.readFileSync(to));
  const errors = [];
  let watcher;
  try {
    write(from, { dockerImages: ['old'] });
    fs.utimesSync(from, new Date(0), new Date(0));
    write(to, { dockerImages: ['fresh-preview'], operatingSystems: ['keep-preview-os'], marker: true });
    watcher = watchDockerMetadata({ source, target, intervalMs: 10, onError: error => errors.push(error) });
    assert.deepEqual(read().dockerImages, ['fresh-preview'], 'startup must preserve newer preview data');
    write(from + '.tmp', { dockerImages: ['passed-image'], operatingSystems: ['do-not-copy'] });
    fs.renameSync(from + '.tmp', from);
    await delay(60);
    assert.deepEqual(read(), { dockerImages: ['passed-image'], operatingSystems: ['keep-preview-os'], marker: true });
    const stamp = fs.statSync(to).mtimeMs;
    await delay(40);
    assert.equal(fs.statSync(to).mtimeMs, stamp, 'unchanged data must not trigger Hugo rebuilds');
    fs.writeFileSync(from, '{');
    await delay(30);
    assert.deepEqual(read().dockerImages, ['passed-image'], 'partial JSON must not corrupt preview data');
    write(from, { dockerImages: [] });
    await delay(60);
    assert.deepEqual(read().dockerImages, [], 'withdrawn files must disappear from the preview');
    assert.ok(errors.length > 0);
    write(path.join(source, '3.4.0.json'), { dockerImages: ['not-mounted'] });
    await delay(30);
    assert.equal(fs.existsSync(path.join(target, '3.4.0.json')), false);
    console.log('Docker metadata watcher tests passed.');
  } finally {
    watcher?.close();
    fs.rmSync(root, { recursive: true, force: true });
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
