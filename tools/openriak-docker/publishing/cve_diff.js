'use strict';
const fs = require('node:fs');
const path = require('node:path');
const records = require('../../scripts/docker-records');
const { summarize } = require('../../scripts/docker-cve-metadata');
const { readAssessments, imageKey } = require('../../scripts/docker-cve-assessments');
function files(root) {
  if (!fs.statSync(root).isDirectory()) return [root];
  return fs.readdirSync(root, {withFileTypes: true}).flatMap(entry => {
    const name = path.join(root, entry.name);
    return entry.isDirectory() ? files(name) : entry.isFile() && entry.name === 'cve-report.json' ? [name] : entry.name === 'current.json' && records.exists(path.join(root, 'cve-report.json')) ? [path.join(root, 'cve-report.json')] : [];
  });
}
function comparable(item) {
  const {hubUrl, detailsUrl, ...meaningful} = item;
  return JSON.stringify(meaningful);
}
function snapshot(root) {
  const images = new Map();
  for (const file of files(root)) {
    const report = records.read(file);
    if (report.product !== 'openriak-kv' || !report.source?.approval) throw new Error(`Invalid CVE report: ${file}`);
    const image = imageKey(report.source.image);
    if ((images.get(image)?.date || '') > (report.finished_at || report.started_at || '')) continue;
    const data = summarize(report, report.source.approval, readAssessments(report.source.version), file);
    images.set(image, {date:report.finished_at || report.started_at || '', digest:report.source.archive.digest, data});
  }
  for (const [image, value] of images) if (value.data.state !== 'complete') throw new Error(`Incomplete verified scan: ${image}`);
  if (!images.size) throw new Error(`No CVE reports found: ${root}`);
  return images;
}
try {
  const before = snapshot(process.argv[2]), after = snapshot(process.argv[3]);
  const result = [];
  for (const image of [...new Set([...before.keys(), ...after.keys()])].sort()) {
    if (!before.has(image) || !after.has(image)) throw new Error(`Both snapshots must contain ${image}`);
    const old = before.get(image), current = after.get(image);
    const previous = new Map(old.data.items.map(item => [item.id, item]));
    const next = new Map(current.data.items.map(item => [item.id, item]));
    const row = {image, beforeDigest:old.digest, afterDigest:current.digest, new:[], resolved:[], changed:[], unchanged:[]};
    for (const [id,item] of next) {
      if (!previous.has(id)) row.new.push(item);
      else if (comparable(previous.get(id)) !== comparable(item)) row.changed.push({id,before:previous.get(id),after:item});
      else row.unchanged.push(item);
    }
    for (const [id,item] of previous) if (!next.has(id)) row.resolved.push(item);
    result.push(row);
  }
  process.stdout.write(JSON.stringify(result));
} catch (error) { console.error(error.message); process.exitCode = 1; }
