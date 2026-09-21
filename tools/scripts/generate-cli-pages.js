#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

function main(args) {
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`Generate versioned Hugo CLI reference pages from deployed KV metadata.

Usage: node tools/scripts/generate-cli-pages.js --version VERSION [OPTIONS]

Options:
  --version VERSION  Exact KV release to generate (required).
  --repo PATH        Docs repository (default: this script's repository).
  --check            Verify generated pages match without writing anything.
  -h, --help         Show help without reading metadata or changing files.

The input is content/openriak-kv/metadata/VERSION/cli-commands.json.
Pages are written under the existing version directory's reference/commands/
(or VERSION-new-release/reference/commands/ for a new release). Existing
command overview URLs and their heading anchors are retained. Other authored
pages are preserved. Build-time data is prepared by sync-product-metadata.js.`);
    return;
  }
  let version, repo = path.resolve(__dirname, '../..'), check = false;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--version') version = args[++i];
    else if (args[i] === '--repo') repo = path.resolve(args[++i]);
    else if (args[i] === '--check') check = true;
    else throw new Error(`Unknown argument: ${args[i]}`);
  }
  if (!/^\d+\.\d+\.\d+$/.test(version || '')) throw new Error('--version must be major.minor.patch');
  const { buildReference } = require('./cli-reference');
  const document = JSON.parse(fs.readFileSync(path.join(repo, 'content/openriak-kv/metadata', version, 'cli-commands.json')));
  if (document.version !== version) throw new Error('Metadata version does not match the requested release');
  const reference = buildReference(document);
  const productRoot = path.join(repo, 'content/openriak-kv');
  const releaseRoot = path.join(productRoot, `${version}-new-release`);
  const patchRoot = path.join(productRoot, version);
  if (fs.existsSync(releaseRoot) && fs.existsSync(patchRoot)) throw new Error(`Ambiguous version directories for ${version}`);
  const root = path.join(fs.existsSync(patchRoot) ? patchRoot : releaseRoot, 'reference/commands');
  const expected = new Map();
  const marker = 'generated_by: "cli-reference"';
  const branchRoutes = new Set(reference.sections.map(s => s.route));
  for (const page of reference.pages) if (reference.pages.some(p => p.route.startsWith(page.route + '/'))) branchRoutes.add(page.route);
  const legacy = new Map();
  for (const [route, file] of [['', '_index.md'], ['riak', 'riak.md'], ['riak-admin', 'riak-admin.md']]) {
    const target = path.join(root, file);
    const branch = path.join(root, route, '_index.md');
    const existing = fs.existsSync(target) ? fs.readFileSync(target, 'utf8') : fs.existsSync(branch) ? fs.readFileSync(branch, 'utf8') : '';
    const saved = existing.match(/^cli_legacy_anchors: (.+)$/m);
    const headings = saved ? JSON.parse(saved[1]) : [...existing.matchAll(/^#{2,6}\s+(.+)$/gm)]
      .map(m => m[1].toLowerCase().replace(/[^\w -]/g, '').trim().replace(/\s+/g, '-'));
    legacy.set(route, [...new Set(headings)]);
  }
  function page(route, title, body, extra = {}) {
    const frontmatter = { title, description: route ? `Syntax, options and help for ${title}.` : 'All OpenRiak KV commands, with options, help and compatibility information.',
      layout: 'single', weight: 1, diataxis: 'reference', product: 'OpenRiak KV', product_version: version,
      draft: true, status: 'reference', technical_review: 'required', generated_by: 'cli-reference',
      cli_reference_version: version, ...extra };
    if (legacy.get(route)?.length) frontmatter.cli_legacy_anchors = legacy.get(route);
    const text = '---\n' + Object.entries(frontmatter).map(([k, v]) => `${k}: ${JSON.stringify(v)}`).join('\n') + '\n---\n\n' + body + '\n';
    const filename = !route ? '_index.md' : branchRoutes.has(route) ? `${route}/_index.md` : `${route}.md`;
    expected.set(filename, text);
  }
  page('', 'Command reference', '{{< cli-command-index >}}');
  for (const item of reference.pages) page(item.route, item.title, '{{< cli-command >}}', { cli_command_key: item.key });
  for (const section of reference.sections) {
    if (!reference.pages.some(p => p.route === section.route)) page(section.route, section.title, '{{< cli-command-index >}}', { cli_command_prefix: section.route });
  }
  // This historical URL remains a useful entry point and preserves old links.
  page('riak-admin', 'riak admin command reference', '{{< cli-command-index >}}', { cli_command_prefix: 'riak/admin' });
  const obsolete = [];
  function walk(directory) {
    if (!fs.existsSync(directory)) return;
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const filename = path.join(directory, entry.name);
      if (entry.isDirectory()) walk(filename);
      else if (entry.name.endsWith('.md') && fs.readFileSync(filename, 'utf8').includes(marker)
        && !expected.has(path.relative(root, filename).split(path.sep).join('/'))) obsolete.push(filename);
    }
  }
  walk(root);
  const oldRiak = path.join(root, 'riak.md');
  if (expected.has('riak/_index.md') && fs.existsSync(oldRiak) && !obsolete.includes(oldRiak)) obsolete.push(oldRiak);
  const changed = [...expected].filter(([file, text]) => !fs.existsSync(path.join(root, file)) || fs.readFileSync(path.join(root, file), 'utf8') !== text);
  // Refuse accidental overwrites outside the three overview pages being replaced.
  for (const [file] of changed) {
    const target = path.join(root, file);
    if (fs.existsSync(target) && !['_index.md', 'riak.md', 'riak-admin.md'].includes(file)
        && !fs.readFileSync(target, 'utf8').includes(marker)) throw new Error(`Refusing to replace authored page ${target}`);
  }
  if (check) {
    if (changed.length || obsolete.length) throw new Error(`CLI pages need regeneration (${changed.length} changed, ${obsolete.length} obsolete)`);
  } else {
    for (const [file, text] of changed) {
      const target = path.join(root, file);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, text);
    }
    for (const file of obsolete) fs.unlinkSync(file);
  }
  console.log(`${version}: ${reference.pages.length} command topics, ${expected.size} pages; ${check ? 'verified' : 'generated'}.`);
}

if (require.main === module) {
  try { main(process.argv.slice(2)); } catch (error) { console.error(error.message); process.exitCode = 1; }
}
module.exports = { main };
