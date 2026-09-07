'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const { multiarchDockerImages } = require('./docker-multiarch-metadata.js');
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'openriak-multiarch-metadata-'));
try {
  const version = '3.4.1';
  const tag = '3.4.1-alpine-3.21-otp26';
  const cache = path.join(temporary, 'cache');
  const published = path.join(temporary, 'static');
  const directory = path.join(cache, version, tag);
  fs.mkdirSync(directory, { recursive: true });
  const report = {
    schema_version: 4, product: 'openriak-kv', version, status: 'passed',
    image: `openriak/openriak-kv:${tag}`, tags: [`openriak/openriak-kv:${tag}`, 'openriak/openriak-kv:latest'],
    platforms: ['linux/amd64', 'linux/arm64'], targets: [
      { os_id: 'alpine-3.21-x86_64', architecture: 'x86_64' },
      { os_id: 'alpine-3.21-aarch64', architecture: 'aarch64' }
    ],
    os_name: 'Alpine Linux 3.21', os_release: '3.21', otp: '26', node: 'test-node',
    finished_at: '2026-09-06T00:00:00Z', cluster_nodes: 5,
    artifacts: {}, base_images: {}, platform_results: {}
  };
  for (const [key, filename] of Object.entries({ dockerfile: 'Dockerfile', compose_single: 'compose.single.yaml', compose_cluster: 'compose.cluster.yaml', environment_example: 'example.env' })) {
    const content = `test ${filename}\n`;
    const url = `downloads/docker/${version}/${tag}/${filename}`;
    const destination = path.join(published, url);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.writeFileSync(destination, content);
    fs.writeFileSync(path.join(directory, filename), content);
    report.artifacts[key] = { filename, url, sha256: crypto.createHash('sha256').update(content).digest('hex') };
  }
  for (const platform of report.platforms) {
    const proof = `platforms/${platform.replaceAll('/', '-')}/runs/example/report.json`;
    const file = path.join(directory, proof);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, JSON.stringify({
      schema_version: 4, status: 'passed', image: report.image,
      target: { docker_platform: platform }, artifacts: report.artifacts,
      tests: { admin_test: { status: 'passed' }, preserved_cookie: { status: 'passed' },
        cluster: { status: 'passed', coordinator_cookie_adoption: 'passed' },
        cluster_admin_test: Object.fromEntries([1, 2, 3, 4, 5].map((node) => [node, { status: 'passed' }])) }
    }));
    report.platform_results[platform] = { status: 'passed', report: proof };
    report.base_images[platform] = { pinned: 'alpine:3.21@sha256:' + 'a'.repeat(64) };
  }
  const save = () => fs.writeFileSync(path.join(directory, 'report.json'), JSON.stringify(report));
  const read = () => multiarchDockerImages(version, cache, published);
  save();
  assert.equal(read().length, 1);
  assert.deepEqual(read()[0].osIds, ['alpine-3.21-x86_64', 'alpine-3.21-aarch64']);
  assert.equal(read()[0].architecture, 'amd64, arm64');
  assert.deepEqual(read()[0].tags, report.tags);
  // Explicitly branded docs caches retain their namespace; default caches remain compatible.
  const originalImage = report.image;
  const originalTags = report.tags;
  report.identity = { namespace: 'tiotjp' };
  report.image = `tiotjp/openriak-kv:${tag}`;
  report.tags = originalTags.map((value) => value.replace('openriak/', 'tiotjp/'));
  for (const result of Object.values(report.platform_results)) {
    const file = path.join(directory, result.report);
    const proof = JSON.parse(fs.readFileSync(file, 'utf8'));
    proof.image = report.image;
    fs.writeFileSync(file, JSON.stringify(proof));
  }
  save();
  assert.equal(read()[0].image, report.image);
  assert.deepEqual(read()[0].tags, report.tags);
  report.identity.namespace = '../invalid'; save();
  assert.throws(read, /Invalid multi-platform Docker report/);
  delete report.identity;
  report.image = originalImage;
  report.tags = originalTags;
  for (const result of Object.values(report.platform_results)) {
    const file = path.join(directory, result.report);
    const proof = JSON.parse(fs.readFileSync(file, 'utf8'));
    proof.image = originalImage;
    fs.writeFileSync(file, JSON.stringify(proof));
  }
  report.status = 'failed'; save();
  assert.deepEqual(read(), []);
  report.status = 'passed';
  report.platform_results['linux/arm64'].status = 'failed'; save();
  assert.throws(read, /Invalid multi-platform Docker report/);
  report.platform_results['linux/arm64'].status = 'passed'; save();
  const armProof = path.join(directory, report.platform_results['linux/arm64'].report);
  const originalProof = fs.readFileSync(armProof, 'utf8');
  const invalidProof = JSON.parse(originalProof);
  delete invalidProof.tests.cluster_admin_test['5'];
  fs.writeFileSync(armProof, JSON.stringify(invalidProof));
  assert.throws(read, /Invalid multi-platform Docker report/);
  fs.writeFileSync(armProof, originalProof);
  fs.writeFileSync(path.join(published, report.artifacts.dockerfile.url), 'tampered');
  assert.throws(read, /Invalid multi-platform Docker report/);
  console.log('Multi-platform metadata publication tests passed.');
} finally {
  fs.rmSync(temporary, { recursive: true, force: true });
}
