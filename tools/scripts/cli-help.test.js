'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const test = require('node:test');

// Copy only the executable: help must work without the repository, Hugo,
// metadata, imported generators or any destination to mutate.
for (const name of ['generate-version-mounts.js', 'sync-product-metadata.js',
  'watch-page-provenance.js', 'watch-docker-metadata.js',
  'build.sh', 'build-project.sh', 'assemble-site.sh']) {
  test(`${name} documents its CLI and exits before work`, () => {
    const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'openriak-help-'));
    try {
      const script = path.join(directory, name);
      fs.copyFileSync(path.join(__dirname, name), script);
      const source = fs.readFileSync(script, 'utf8');
      for (const flag of ['-h', '--help']) {
        const result = spawnSync(name.endsWith('.js') ? process.execPath : '/bin/sh', [script, flag],
          { cwd: directory, encoding: 'utf8', timeout: 5000 });
        assert.equal(result.status, 0, result.stderr || String(result.error));
        assert.match(result.stdout, /Usage:/);
        assert.match(result.stdout, /--help/);
        for (const match of source.matchAll(/(?:argument|argumentsList\[index\]) === '(--[a-z-]+)'/g)) {
          assert.ok(result.stdout.includes(match[1]), `Missing ${match[1]}`);
        }
        assert.deepEqual(fs.readdirSync(directory), [name]);
      }
    } finally {
      fs.rmSync(directory, { recursive: true, force: true });
    }
  });
}
