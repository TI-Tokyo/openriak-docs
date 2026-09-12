'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const records = require('./docker-records');
const readJson = records.read;
const sha256 = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const filenames = {
  dockerfile: 'Dockerfile', compose_single: 'compose.single.yaml',
  compose_cluster: 'compose.cluster.yaml', environment_example: 'example.env'
};

// A group is advertised only after the exact shared files pass on every platform.
const multiarchDockerImages = (version, cacheRoot, staticRoot) => {
  const root = path.join(cacheRoot, version);
  if (!fs.existsSync(root)) return [];
  const images = [];
  const cves = require('./docker-cve-metadata').cveReader(version, cacheRoot);
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const directory = path.join(root, entry.name);
    const reportFile = path.join(directory, 'report.json');
    if (!records.exists(reportFile)) continue;
    const report = readJson(reportFile);
    if (report.status !== 'passed' || report.schema_version !== 4) continue;
    const fail = () => { throw new Error(`Invalid multi-platform Docker report: ${reportFile}`); };
    const namespace = report.identity?.namespace ?? 'openriak';
    if (!/^[a-z0-9]+(?:[._-][a-z0-9]+)*$/.test(namespace)) fail();
    if (report.product !== 'openriak-kv' || report.version !== version
        || report.image !== `${namespace}/openriak-kv:${entry.name}`
        || !Array.isArray(report.platforms) || !report.platforms.length
        || new Set(report.platforms).size !== report.platforms.length
        || !Array.isArray(report.targets) || report.targets.length !== report.platforms.length) fail();
    for (const [key, filename] of Object.entries(filenames)) {
      const artifact = report.artifacts?.[key];
      const expectedUrl = `downloads/docker/${version}/${entry.name}/${filename}`;
      if (artifact?.filename !== filename || artifact.url !== expectedUrl) fail();
      const cached = records.artifact(path.join(directory, filename), cacheRoot);
      const published = path.join(staticRoot, expectedUrl);
      if (!fs.existsSync(cached) || !fs.existsSync(published)
          || sha256(cached) !== artifact.sha256 || sha256(published) !== artifact.sha256) fail();
    }
    for (const platform of report.platforms) {
      const result = report.platform_results?.[platform];
      if (result?.status !== 'passed' || typeof result.report !== 'string') fail();
      const proofPath = path.resolve(directory, result.report);
      if (!proofPath.startsWith(directory + path.sep) || !records.exists(proofPath)) fail();
      const proof = readJson(proofPath);
      if (proof.status !== 'passed' || proof.schema_version !== 4 || proof.image !== report.image
          || proof.target?.docker_platform !== platform || proof.tests?.admin_test?.status !== 'passed'
          || proof.tests?.cluster?.status !== 'passed'
          || proof.tests?.preserved_cookie?.status !== 'passed'
          || proof.tests?.cluster?.coordinator_cookie_adoption !== 'passed'
          || Object.values(proof.tests?.cluster_admin_test || {}).length !== report.cluster_nodes
          || Object.values(proof.tests.cluster_admin_test).some((test) => test.status !== 'passed')) fail();
      for (const key of Object.keys(filenames)) {
        if (proof.artifacts?.[key]?.sha256 !== report.artifacts[key].sha256) fail();
      }
    }
    images.push({
      osId: report.targets[0].os_id, osIds: report.targets.map((target) => target.os_id),
      osName: report.os_name, osRelease: report.os_release, otp: report.otp,
      architecture: report.platforms.map((platform) => platform.replace('linux/', '')).join(', '),
      platforms: report.platforms, image: report.image, tags: report.tags,
      cves: cves(report),
      node: report.node, testedAt: report.finished_at, clusterNodes: report.cluster_nodes,
      baseImage: Object.values(report.base_images).map((base) => base.pinned).join(', '),
      dockerfile: report.artifacts.dockerfile, composeSingle: report.artifacts.compose_single,
      composeCluster: report.artifacts.compose_cluster, environmentExample: report.artifacts.environment_example
    });
  }
  return images;
};

module.exports = { multiarchDockerImages };
