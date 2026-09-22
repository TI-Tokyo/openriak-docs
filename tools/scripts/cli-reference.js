'use strict';

// Convert runtime inventory records into documentation topics. Keep all source
// forms on their topic; aliases and argument values must not multiply pages.
const unique = values => [...new Set(values.filter(Boolean))];
const slug = value => value.replace(/_/g, '-').replace(/[^a-zA-Z0-9.-]+/g, '-').toLowerCase();
const compare = (a, b) => a.localeCompare(b, 'en');
const shellKey = path => `shell:${path.join(' ')}`;

function normalizedPath(command) {
  const path = [...command.path];
  if (path[0] === '_' && ['set', 'show', 'describe'].includes(path[1])) path.splice(0, 1, 'riak', 'admin');
  if (path[0] === 'riak-admin') path.splice(0, 1, 'riak', 'admin');
  if (path[0] === 'riak' && ['remote', 'remsh'].includes(path[1])) path[1] = 'remote_console';
  return path;
}

function category(path, context) {
  if (context === 'erlang') return 'Erlang shell';
  if (path[0] !== 'riak') return 'Bundled helpers';
  if (path[1] === 'repl') return 'Replication';
  if (path[1] !== 'admin') return 'Node and release commands';
  return ({ cluster: 'Cluster', security: 'Security', handoff: 'Handoff',
    'bucket-type': 'Bucket types', stat: 'Statistics', tictacaae: 'TicTac AAE' })[path[2]] || 'Administration';
}

function buildReference(document) {
  if (document.schema_version !== 1 || document.product !== 'kv' || document.status !== 'complete'
      || document.warnings?.length || !document.commands?.length) {
    throw new Error('CLI reference requires complete KV CLI metadata without discovery warnings');
  }
  const records = document.commands.filter(c => c.examples?.length || (c.visibility !== 'internal' && !/@private\b/.test(c.help || '')));
  const paths = new Map(records.filter(c => c.context === 'shell').map(c => [shellKey(normalizedPath(c)), normalizedPath(c)]));
  const aliases = new Map();
  // Union only aliases explicitly declared by the dispatcher; spelling alone is
  // insufficient evidence that two real operations have the same meaning.
  for (const command of records.filter(c => c.context === 'shell')) {
    const candidates = [normalizedPath(command), ...(command.aliases || []).map(a => normalizedPath({ path: a.invocation.split(' ') }))]
      .filter(p => paths.has(shellKey(p))).sort((a, b) =>
        (a.join(' ').match(/_/g) || []).length - (b.join(' ').match(/_/g) || []).length || compare(a.join(' '), b.join(' ')));
    for (const candidate of candidates) aliases.set(shellKey(candidate), candidates[0]);
  }
  // Descendants inherit their parent's explicitly established spelling.
  function canonicalPath(path) {
    for (let length = path.length; length > 0; length--) {
      const canonical = aliases.get(shellKey(path.slice(0, length)));
      if (canonical && canonical.join(' ') !== path.slice(0, length).join(' ')) return [...canonical, ...path.slice(length)];
    }
    return path;
  }
  const topics = new Map();
  const recordTopics = {};
  for (const command of records) {
    let path, key, route, title;
    if (command.context === 'erlang') {
      key = `erlang:${command.module}:${command.function}${command.selector ? ':' + command.selector : ''}`;
      path = ['erlang', slug(command.module), slug(command.function), ...(command.selector ? [slug(command.selector)] : [])];
      title = `${command.module}:${command.function}${command.selector ? ' — ' + command.selector : ''}`;
      route = path.join('/');
    } else {
      path = canonicalPath(normalizedPath(command));
      if (command.availability === 'help_only') {
        const corrected = path.map(p => p.replace(/_/g, '-'));
        if (!paths.has(shellKey(corrected))) continue;
        path = corrected;
      }
      const statHelp = path.slice(0, 4).join(' ') === 'riak admin stat help';
      if (statHelp) path.splice(3, 1);
      path = path.filter(p => p !== '*');
      if (path.slice(0, 3).join(' ') === 'riak admin handoff' && ['inbound', 'outbound', 'both'].includes(path.at(-1))) path.pop();
      if (command.kind === 'console_dispatch' && ['true', 'false', 'root', 'always', 'never'].includes(path.at(-1))) path.pop();
      key = shellKey(path);
      title = path.join(' ');
      route = path[0] === 'riak' ? path.map(slug).join('/') : ['helpers', ...path.map(slug)].join('/');
    }
    recordTopics[command.id] = key;
    if (!topics.has(key)) topics.set(key, { key, path, route, title, context: command.context,
      category: category(path, command.context), records: [] });
    topics.get(key).records.push(command);
  }
  const pages = [...topics.values()].sort((a, b) => compare(a.route, b.route));
  const routeKeys = new Set();
  for (const page of pages) {
    if (routeKeys.has(page.route)) throw new Error(`CLI route collision: ${page.route}`);
    routeKeys.add(page.route);
    const items = page.records;
    page.linkTitle = page.context === 'erlang' ? items[0].selector || items[0].function : page.path.at(-1);
    page.ids = items.map(c => c.id);
    page.summary = page.context === 'erlang' ? `Call ${page.title} from the Erlang shell.` : `Run ${page.title} on an OpenRiak KV node.`;
    page.description = unique(items.map(c => c.description || c.summary)).join('\n\n');
    const statuses = unique(items.map(c => c.availability || 'available'));
    page.availability = statuses.includes('available') ? 'available' : statuses.includes('unavailable') ? 'unavailable' : statuses[0];
    page.deprecated = items.some(c => c.deprecated);
    page.helper = page.category === 'Bundled helpers';
    page.internal = items.some(c => c.visibility === 'internal' || /@private\b/.test(c.help || ''));
    page.notice = unique(items.map(c => c.unavailable_reason)).join(' ');
    page.aliases = [];
    page.helpInvocations = [];
    for (const item of items) {
      for (const alias of item.aliases || []) {
        if (alias.invocation !== page.title) page.aliases.push(alias.invocation);
      }
      if (item.context === 'shell' && item.path.includes('help') && !page.path.includes('help')) page.helpInvocations.push(item.invocation);
      else if (item.context === 'shell' && canonicalPath(normalizedPath(item)).join(' ') === page.title
          && item.invocation !== page.title && !page.helper) page.aliases.push(item.invocation);
    }
    // Argument-bearing forms are syntax, not aliases of the bare command.
    page.aliases = unique(page.aliases).filter(a => !a.includes('*') && a.split(' ').length <= page.path.length).sort(compare);
    page.helpInvocations = unique(page.helpInvocations).sort(compare);
    page.forms = items.map(item => ({
      label: item.context === 'erlang' ? `${item.module}:${item.function}/${item.arity}${item.selector ? ' — ' + item.selector : ''}` : item.invocation.replace(/^_ /, 'riak admin '),
      syntax: item.context === 'erlang'
        ? item.selector ? [item.invocation] : (item.signatures || []).map(s => `${item.module}:${s}.`)
        : unique(((item.usage || []).length ? item.usage : [item.invocation])
          .map(text => text.replace(/^\s*usage\b\s*:?\s*/i, '').replace(/^_ /, 'riak admin ').replace(/^riak-admin\b/, 'riak admin'))),
      template: item.context === 'erlang' || item.wildcard_path || Boolean(item.invocation_is_template),
      help: unique([item.help, ...(item.help_sources || []).map(h => h.text)]).map(t => t.replace(/Usage: _ /g, 'Usage: riak-admin ')),
      specifications: item.specifications || [],
      arguments: item.arguments === 'unrestricted' ? [] : item.arguments || [],
      unrestricted: item.arguments === 'unrestricted',
      argumentFormat: item.argument_format || '',
      options: [...(item.options || []), ...(item.global_options || [])],
    }));
    const seenForms = new Set();
    page.forms = page.forms.filter(form => {
      const key = JSON.stringify([form.syntax, form.help, form.specifications, form.arguments, form.options]);
      if (seenForms.has(key)) return false;
      seenForms.add(key); return true;
    });
    // Merge declarations of the same flag without dropping richer Clique/getopt
    // types when a second source only mentions its spelling in a usage string.
    const options = new Map();
    for (const item of items) {
      for (const option of [...(item.options || []), ...(item.global_options || [])]) {
        if (!option.name) continue;
        let name = option.name.startsWith('-') ? option.name : '--' + option.name;
        let short = option.short ? (option.short.startsWith('-') ? option.short : '-' + option.short) : '';
        // Clique consumes global long flags before parsing command flags. A
        // command's colliding short spelling still selects its local option.
        if ((item.options || []).includes(option) && short &&
            (item.global_options || []).some(global => global.name === name)) {
          name = short; short = '';
        }
        const row = options.get(name) || { name, short: '', datatype: '', value: '', description: '', hidden: false, appliesTo: [] };
        row.short ||= short;
        row.datatype ||= option.datatype || '';
        row.value ||= option.value_name || '';
        row.description ||= option.description || '';
        if (option.allowed_values) row.allowedValues = option.allowed_values;
        if (Object.hasOwn(option, 'default')) row.defaultValue = option.default;
        for (const flag of ['required', 'repeatable']) if (Object.hasOwn(option, flag)) row[flag] = option[flag];
        if ((item.global_options || []).includes(option)) {
          row.required = false;
          row.repeatable = false;
          if (name === '--help') row.datatype ||= 'flag (no value)';
        }
        row.hidden ||= Boolean(option.hidden);
        row.appliesTo.push(item.invocation);
        options.set(name, row);
      }
    }
    for (const option of options.values()) {
      if (option.short && options.has(option.short)) {
        const short = options.get(option.short);
        option.description ||= short.description;
        option.value ||= short.value;
        options.delete(option.short);
      }
      option.appliesTo = unique(option.appliesTo);
    }
    page.options = [...options.values()].sort((a, b) => compare(a.name, b.name));
    page.prerequisites = unique(items.flatMap(c => c.prerequisites || []));
    const examples = [...new Map(items.flatMap(c => c.usage_examples || []).map(e => [JSON.stringify(e), e])).values()];
    if (examples.length) page.examples = examples;
    page.types = unique(items.flatMap(c => c.argument_types || []));
    page.variants = [...new Map(items.flatMap(c => c.variants || []).map(v => [JSON.stringify(v), v])).values()];
    page.provenance = [...new Map(items.flatMap(c => c.provenance || []).map(p => [JSON.stringify(p), p])).values()];
    page.children = pages.filter(p => p.route.startsWith(page.route + '/') && !p.route.slice(page.route.length + 1).includes('/'))
      .map(p => ({ title: p.title, route: p.route, deprecated: p.records?.some(c => c.deprecated) ?? p.deprecated }));
    delete page.records;
  }
  const sections = [{ route: 'erlang', title: 'Erlang shell operations' }, { route: 'helpers', title: 'Bundled helpers' }];
  for (const page of pages) {
    const parts = page.route.split('/');
    for (let length = 1; length < parts.length; length++) {
      const route = parts.slice(0, length).join('/');
      if (!routeKeys.has(route) && !sections.some(s => s.route === route)) sections.push({ route,
        title: parts[0] === 'erlang' && length === 2 ? page.key.split(':')[1] : parts[length - 1] });
    }
  }
  return { schemaVersion: 1, version: document.version, source: document.source, runtime: document.runtime,
    inputCount: document.commands.length, excludedCount: document.commands.length - Object.keys(recordTopics).length,
    pages, sections, recordTopics };
}

module.exports = { buildReference };
