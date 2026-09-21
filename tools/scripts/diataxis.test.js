'use strict';
const assert = require('node:assert/strict');
const { test } = require('node:test');
const fs = require('node:fs');
const path = require('node:path');
const yaml = require('./vendor/js-yaml/js-yaml');
const root = path.resolve(__dirname, '../..');
const content = path.join(root, 'content/openriak-kv');
const plan = JSON.parse(fs.readFileSync(path.join(root, 'notes/reports/diataxis-page-map.json')));
const route = file => file.replace(/(?:\/)?_index\.md$|\.md$/g, '').replace(/\/$/, '');
const read = file => {
  const text = fs.readFileSync(file, 'utf8');
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  assert.ok(match, `Missing front matter: ${file}`);
  return { metadata: yaml.load(match[1]), body: text.slice(match[0].length) };
};
const files = dir => fs.readdirSync(dir, { withFileTypes: true }).flatMap(entry => entry.isDirectory() ? files(path.join(dir, entry.name)) : entry.name.endsWith('.md') ? [path.join(dir, entry.name)] : []);
for (const version of ['3.4.0', '3.4.1']) {
  const merged = new Map();
  for (const layer of ['3.4.0-new-release', ...(version === '3.4.1' ? ['3.4.1'] : [])]) {
    const base = path.join(content, layer);
    for (const file of files(base)) merged.set(route(path.relative(base, file)), { ...read(file), file });
  }
  test(`${version}: planned topics exist at unique paths and retain their Diataxis purpose`, () => {
    const paths = new Set();
    for (const [area, rows] of Object.entries(plan)) for (const row of rows) {
      const key = route(row.path);
      assert.ok(!paths.has(key), `Duplicate planned topic: ${key}`);
      paths.add(key);
      const page = merged.get(key);
      assert.ok(page, `Missing planned topic: ${key}`);
      assert.equal(page.metadata.diataxis, { foundations: 'explanation', 'how-to': 'how-to', tutorials: 'tutorial', reference: 'reference' }[area], page.file);
      assert.ok(page.body.trim().length > 0, `Empty topic: ${page.file}`);
      if (!row.path.endsWith('_index.md')) assert.ok(page.metadata.related?.length > 0, `Missing related reading: ${page.file}`);
    }
  });
  test(`${version}: related pages, workflow steps and version-relative links resolve`, () => {
    for (const [key, page] of merged) {
      if (!/^(foundations|how-to|tutorials|reference)(\/|$)/.test(key)) continue;
      const links = [...(page.metadata.related || []).map(link => typeof link === 'string' ? link : link.page), page.metadata.previous_page, page.metadata.next_page].filter(Boolean);
      for (const match of page.body.matchAll(/\{\{<\s*product-version-root\s*>\}\}([^\s)"<>]+)/g)) links.push(match[1]);
      for (const link of links) {
        const target = link.split('#')[0].replace(/\/$/, '');
        assert.ok(merged.has(target), `${page.file}: missing ${link}`);
      }
    }
  });
  test(`${version}: metadata references use known command topics and API definitions`, () => {
    const cli = JSON.parse(fs.readFileSync(path.join(root, `tools/generated/openriak-kv/data/cli-reference/${version}.json`)));
    const keys = new Set(cli.pages.map(page => page.key));
    const reference = JSON.parse(fs.readFileSync(path.join(content, `metadata/${version}/kv-reference.json`)));
    for (const [key, page] of merged) {
      if (!/^(foundations|how-to|tutorials|reference)(\/|$)/.test(key)) continue;
      for (const match of page.body.matchAll(/\{\{<\s*cli(?:-example|-command)?\s+[^>]*?key="([^"]+)"/g)) assert.ok(keys.has(match[1]), `${page.file}: unknown CLI key ${match[1]}`);
      for (const match of page.body.matchAll(/configuration-reference-table\s+reference="([^"]+)"/g)) assert.ok(reference.tables[match[1]], `${page.file}: missing table ${match[1]}`);
      for (const match of page.body.matchAll(/protocol-message\s+name="([^"]+)"/g)) assert.ok(reference.messages[match[1]], `${page.file}: missing protocol message ${match[1]}`);
    }
    const capabilities = reference.tables.backends.rows.find(row => row.name === 'Leveled').capabilities;
    assert.match(capabilities, /complex_query/);
    assert.doesNotMatch(capabilities, /define|app_helper|record/, 'Backend extraction must stop at the end of the capabilities declaration');
    assert.ok(reference.tables['node-metrics'].rows.length > 200);
  });
}
