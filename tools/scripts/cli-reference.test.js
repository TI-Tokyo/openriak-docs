'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { test } = require('node:test');
const { buildReference } = require('./cli-reference');
const { main: generate } = require('./generate-cli-pages');
const shell = (invocation, fields = {}) => ({ id: `shell:${invocation}`, invocation, path: invocation.split(' '),
  context: 'shell', kind: 'shell', availability: 'available', deprecated: false, help: '', arguments: [], options: [], ...fields });
const document = commands => ({ schema_version: 1, product: 'kv', version: '3.4.0', status: 'complete', warnings: [], commands });

test('command format flags retain their own choices separately from global writers', () => {
  const ref = buildReference(document([shell('riak admin node repair status', {
    options: [{ name: '--format', short: '-f', datatype: 'string', allowed_values: ['table', 'json'], default: 'table' }],
    global_options: [{ name: '--format', datatype: 'string', allowed_values: ['csv', 'human', 'json'], default: 'human' }],
  })]));
  const options = ref.pages[0].options;
  assert.equal(options.length, 2);
  assert.deepEqual(options.find(o => o.name === '-f').allowedValues, ['table', 'json']);
  assert.equal(options.find(o => o.name === '-f').defaultValue, 'table');
  assert.equal(options.find(o => o.name === '--format').short, '');
  assert.equal(options.find(o => o.name === '--format').defaultValue, 'human');
});

test('aliases and their descendants share pages without losing flag declarations', () => {
  const reference = buildReference(document([
    shell('riak admin repair-2i', { aliases: [{ invocation: 'riak admin repair_2i' }], options: [{ name: '--speed', datatype: 'integer' }] }),
    shell('riak admin repair_2i', { aliases: [{ invocation: 'riak admin repair-2i' }], options: [{ name: '--speed', description: 'Duty cycle' }] }),
    shell('riak admin repair-2i status', { kind: 'console_dispatch' }),
    shell('riak admin repair_2i status', { kind: 'console_dispatch' }),
    shell('riak remote'), shell('riak remsh'), shell('riak remote_console'),
  ]));
  assert.equal(reference.pages.length, 3);
  const repair = reference.pages.find(p => p.route === 'riak/admin/repair-2i');
  assert.equal(repair.options[0].datatype, 'integer');
  assert.equal(repair.options[0].description, 'Duty cycle');
  assert.equal(repair.children[0].route, 'riak/admin/repair-2i/status');
  assert.ok(repair.aliases.includes('riak admin repair_2i'));
});

test('wildcards and values remain syntax on their parent command', () => {
  const reference = buildReference(document([
    shell('riak admin cluster location *', { wildcard_path: true }),
    shell('riak admin handoff enable inbound'), shell('riak admin handoff enable outbound'), shell('riak admin handoff enable both'),
    shell('riak admin downgrade-objects true', { kind: 'console_dispatch' }),
    shell('riak admin downgrade-objects false', { kind: 'console_dispatch' }),
    shell('_ set', { kind: 'clique', arguments: 'unrestricted', help: 'Usage: _ set <variable>=<value>' }),
  ]));
  assert.equal(reference.pages.length, 4);
  assert.equal(reference.pages.find(p => p.route.endsWith('/enable')).forms.length, 3);
  const set = reference.pages.find(p => p.route === 'riak/admin/set');
  assert.equal(set.forms[0].unrestricted, true);
  assert.ok(set.forms[0].help[0].includes('riak-admin set'));
  assert.ok(reference.pages.every(p => !p.route.includes('*')));
});

test('Erlang arities combine, AAE selectors have pages, documented internal operations remain visible', () => {
  const operation = (arity, fields = {}) => ({ ...shell('unused'), id: `erlang:riak_client:aae_fold/${arity}`,
    context: 'erlang', kind: 'erlang_function', module: 'riak_client', function: 'aae_fold', arity,
    invocation: `riak_client:aae_fold/${arity}`, signatures: ['aae_fold(Query)'], ...fields });
  const reference = buildReference(document([
    operation(1), operation(2),
    operation(1, { id: 'erase1', kind: 'erlang_subcommand', selector: 'erase_keys' }),
    operation(2, { id: 'erase2', kind: 'erlang_subcommand', selector: 'erase_keys' }),
    operation(3, { id: 'compiler', function: 'for_dialyzer_only_ignore', visibility: 'internal', help: '@private' }),
    operation(1, { id: 'repair', module: 'riak_core_vnode_manager', function: 'kill_repairs', visibility: 'internal', help: '@private', examples: [{ expression: 'kill_repairs(reason).' }] }),
  ]));
  assert.equal(reference.pages.length, 3);
  assert.equal(reference.pages.find(p => p.title.endsWith('erase_keys')).forms.length, 2);
  assert.ok(reference.pages.find(p => p.title.includes('kill_repairs')).internal);
  assert.ok(!reference.recordTopics.compiler);
  assert.ok(reference.sections.some(s => s.route === 'erlang/riak-core-vnode-manager'));
});

test('unavailable commands and deprecated commands retain their status', () => {
  const reference = buildReference(document([
    shell('riak start', { deprecated: true }),
    shell('riak admin search', { availability: 'unavailable', unavailable_reason: 'Missing handler' }),
    shell('riak admin remove', { availability: 'removed' }),
  ]));
  assert.equal(reference.pages.find(p => p.title === 'riak start').deprecated, true);
  assert.equal(reference.pages.find(p => p.title.endsWith('search')).notice, 'Missing handler');
  assert.equal(reference.pages.find(p => p.title.endsWith('remove')).availability, 'removed');
  assert.throws(() => buildReference({ ...document([]), status: 'partial' }), /complete KV/);
});

test('generation is repeatable, preserves authored pages and anchors, and check detects stale output', () => {
  const repo = fs.mkdtempSync(path.join(os.tmpdir(), 'cli-reference-pages-'));
  try {
    const metadata = path.join(repo, 'content/openriak-kv/metadata/3.4.0');
    fs.mkdirSync(metadata, { recursive: true });
    fs.writeFileSync(path.join(metadata, 'kv-cli-commands.json'), JSON.stringify(document([shell('riak'), shell('riak stop'), shell('riak admin'), shell('riak-admin')])));
    const root = path.join(repo, 'content/openriak-kv/3.4.0-new-release/reference/commands');
    fs.mkdirSync(root, { recursive: true });
    fs.writeFileSync(path.join(root, 'riak.md'), '# Legacy\n\n## stop\nLegacy body');
    fs.writeFileSync(path.join(root, 'riak-control.md'), 'Authored control guide');
    fs.writeFileSync(path.join(root, 'riak-admin.md'), '---\ngenerated_by: "cli-reference"\n---\nObsolete alias overview');
    generate(['--repo', repo, '--version', '3.4.0']);
    generate(['--repo', repo, '--version', '3.4.0', '--check']);
    assert.match(fs.readFileSync(path.join(root, 'riak/_index.md'), 'utf8'), /cli_legacy_anchors: \["stop"\]/);
    assert.ok(!fs.existsSync(path.join(root, 'riak.md')));
    assert.ok(!fs.existsSync(path.join(root, 'riak-admin.md')));
    assert.ok(fs.existsSync(path.join(root, 'riak/admin.md')));
    assert.equal(fs.readFileSync(path.join(root, 'riak-control.md'), 'utf8'), 'Authored control guide');
    fs.appendFileSync(path.join(root, 'riak/stop.md'), '\nEdited');
    assert.throws(() => generate(['--repo', repo, '--version', '3.4.0', '--check']), /regeneration/);

    const patchRoot = path.join(repo, 'content/openriak-kv/3.4.1');
    const patchMetadata = path.join(repo, 'content/openriak-kv/metadata/3.4.1');
    fs.mkdirSync(patchRoot);
    fs.mkdirSync(patchMetadata);
    fs.writeFileSync(path.join(patchMetadata, 'kv-cli-commands.json'), JSON.stringify({ ...document([shell('riak stop')]), version: '3.4.1' }));
    generate(['--repo', repo, '--version', '3.4.1']);
    assert.ok(fs.existsSync(path.join(patchRoot, 'reference/commands/riak/stop.md')));
    assert.ok(!fs.existsSync(path.join(repo, 'content/openriak-kv/3.4.1-new-release')));
  } finally { fs.rmSync(repo, { recursive: true, force: true }); }
});

test('deployed 3.4.0 inventory has one destination for every public or documented command', () => {
  const raw = JSON.parse(fs.readFileSync(path.join(__dirname, '../../content/openriak-kv/metadata/3.4.0/kv-cli-commands.json')));
  const result = buildReference(raw);
  for (const command of raw.commands) {
    if ((command.visibility === 'internal' || /@private\b/.test(command.help)) && !command.examples?.length) continue;
    assert.ok(result.recordTopics[command.id], command.id);
  }
  assert.equal(new Set(result.pages.map(p => p.route)).size, result.pages.length);
  assert.ok(!result.pages.some(p => p.title.includes('for_dialyzer')));
  assert.ok(result.pages.some(p => p.key === 'shell:riak admin set' && p.options.some(o => o.name === '--node')));
});
