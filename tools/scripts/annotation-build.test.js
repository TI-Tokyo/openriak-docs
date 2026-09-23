'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const repository = path.resolve(__dirname, '../..');

test('production Docker inputs include annotation sources before metadata regeneration', () => {
  const dockerfile = fs.readFileSync(path.join(repository, 'docker/Dockerfile'), 'utf8');
  const metadata = dockerfile.split(' AS core-metadata\n')[1].split('\nFROM ')[0];
  assert.match(metadata, /COPY content\/annotations \.\/content\/annotations[\s\S]*RUN case/);
  const core = dockerfile.split(' AS core-build\n')[1].split('\nFROM ')[0];
  assert.doesNotMatch(core, /--panicOnWarning/, 'editorial correction warnings must not abort the core build');
  const archives = dockerfile.split(' AS archive-build\n')[1].split('\nFROM ')[0];
  assert.match(archives, /--panicOnWarning/, 'archives retain their strict warning policy');
});

test('packaged adapters reject missing default annotation inputs instead of publishing raw fallback data', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'annotation-build-'));
  try {
    // Reproduce Docker's separate /project tree without altering the checkout or dev server.
    fs.cpSync(__dirname, path.join(directory, 'tools/scripts'), {recursive: true});
    execFileSync(process.execPath, ['-e', `
      const assert = require('node:assert/strict');
      const fs = require('node:fs');
      const {annotateSettings} = require('./tools/scripts/settings-annotations');
      const {buildAnnotatedReference} = require('./tools/scripts/cli-annotations');
      assert.throws(() => annotateSettings({}, {}), /Missing settings annotation directory/);
      assert.throws(() => buildAnnotatedReference({}), /Missing CLI annotation directory/);
      // Copying only the parent CLI directory must not hide a missing settings subtree.
      fs.mkdirSync('content/annotations/openriak-kv', {recursive: true});
      assert.throws(() => annotateSettings({}, {}), /Missing settings annotation directory/);
    `], {cwd: directory, stdio: 'pipe'});
  } finally {
    fs.rmSync(directory, {recursive: true, force: true});
  }
});
