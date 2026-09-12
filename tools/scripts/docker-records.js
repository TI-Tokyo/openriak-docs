'use strict';

// Durable records use immutable snapshots and a small per-directory index.
// Plain report files remain supported for standalone outputs and test fixtures.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../../records/openriak-docker/images');
const artifactRoot = path.resolve(__dirname, '../../artifacts/openriak-docker/images');
const resolve = (file, { verify = true } = {}) => {
  if (fs.existsSync(file)) return file;
  const pointer = path.join(path.dirname(file), 'current.json');
  if (!fs.existsSync(pointer)) return null;
  const ref = JSON.parse(fs.readFileSync(pointer, 'utf8')).files?.[path.basename(file)];
  if (!ref) return null;
  if (!/^[0-9a-f]{64}$/.test(ref.sha256) || ref.snapshot !== `history/${ref.sha256}.json`) {
    throw new Error(`Invalid Docker record pointer: ${pointer}`);
  }
  const snapshot = path.join(path.dirname(file), ref.snapshot);
  if (!fs.realpathSync(snapshot).startsWith(fs.realpathSync(path.dirname(file)) + path.sep)) {
    throw new Error(`Docker record escapes its directory: ${snapshot}`);
  }
  if (verify) {
    const bytes = fs.readFileSync(snapshot);
    if (crypto.createHash('sha256').update(bytes).digest('hex') !== ref.sha256) {
      throw new Error(`Docker record checksum mismatch: ${snapshot}`);
    }
  }
  return snapshot;
};
const exists = file => Boolean(resolve(file, { verify: false }));
const read = file => {
  const resolved = resolve(file);
  if (!resolved) throw new Error(`Missing Docker record: ${file}`);
  return JSON.parse(fs.readFileSync(resolved, 'utf8'));
};
const artifact = (file, recordsRoot) => path.resolve(recordsRoot) === root
  ? path.join(artifactRoot, path.relative(root, file)) : file;

module.exports = { root, artifactRoot, resolve, exists, read, artifact };
