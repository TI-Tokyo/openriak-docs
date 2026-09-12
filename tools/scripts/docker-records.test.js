'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const records = require('./docker-records');
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'openriak-records-test-'));
try {
  const data = Buffer.from(JSON.stringify({ status: 'passed', digest: 'verified' }));
  const sha256 = crypto.createHash('sha256').update(data).digest('hex');
  fs.mkdirSync(path.join(root, 'history'));
  fs.writeFileSync(path.join(root, 'history', sha256 + '.json'), data);
  fs.writeFileSync(path.join(root, 'current.json'), JSON.stringify({ schema_version: 1,
    files: { 'report.json': { snapshot: `history/${sha256}.json`, sha256 } } }));
  assert.deepEqual(records.read(path.join(root, 'report.json')), { status: 'passed', digest: 'verified' });
  assert.equal(records.exists(path.join(root, 'missing.json')), false);
  fs.writeFileSync(path.join(root, 'history', sha256 + '.json'), '{}');
  assert.throws(() => records.read(path.join(root, 'report.json')), /checksum mismatch/);
  fs.writeFileSync(path.join(root, 'current.json'), JSON.stringify({ files: {
    'report.json': { snapshot: '../outside.json', sha256 } } }));
  assert.throws(() => records.read(path.join(root, 'report.json')), /Invalid Docker record pointer/);
} finally {
  fs.rmSync(root, { recursive: true, force: true });
}
