'use strict';
const {readMarkdownLayers, annotationFiles} = require('./cli-annotation-markdown');
const path = require('node:path');
const { validateTags, mergeTags } = require('./annotation-tags');
const crypto = require('node:crypto');
const { buildReference } = require('./cli-reference');
const { buildSyntax } = require('./cli-syntax');
const sorted = value => Array.isArray(value) ? value.map(sorted) : value && typeof value === 'object'
  ? Object.fromEntries(Object.keys(value).sort().map(k => [k, sorted(value[k])])) : value;
const fingerprint = command => crypto.createHash('sha256').update(JSON.stringify(sorted(Object.fromEntries(
  ['id', 'path', 'arguments', 'options', 'global_options', 'help', 'availability'].map(k => [k, command[k] ?? null]))))).digest('hex');
const reviewFingerprint = command => crypto.createHash('sha256').update(JSON.stringify(sorted({
  command: fingerprint(command),
  reference: command.reference ? {
    arguments: command.reference.arguments || [], results: command.reference.results || [], errors: command.reference.errors || [],
    examples: (command.reference.examples || []).map(e => ({ id: e.id, invocation: e.invocation, scenario: e.verification?.sha256 || null }))
  } : null
}))).digest('hex');
const defaultOverrideRoot = path.resolve(__dirname, '../../content/annotations/openriak-kv');
const arrayFields = ['arguments', 'shared_arguments', 'examples', 'results', 'errors', 'notes'];
const exampleFields = ['id', 'title', 'invocation', 'description', 'prerequisites', 'outcome', 'expected_output'];
const fields = {
  arguments: ['name', 'format', 'description', 'datatype', 'required', 'repeatable', 'allowed_values', 'default'], examples: exampleFields,
  results: ['id', 'description'], errors: ['id', 'condition', 'description', 'remedy']
};
fields.shared_arguments = fields.arguments;
function plain(value) { return value && typeof value === 'object' && !Array.isArray(value); }
function displayShellInvocation(text) {
  // Change only the launcher prefix, preserving argument quoting and meaningful
  // environment overrides (for example the cookie in an authentication example).
  const value = String.raw`(?:'[^']*'|"(?:\\.|[^"\\])*"|[^\s"'\\]+)`;
  const assignment = String.raw`[A-Za-z_][A-Za-z0-9_]*=${value}`;
  const prefix = new RegExp(String.raw`^([ \t]*)(?:env[ \t]+)?((?:${assignment}[ \t]+)*)/usr/lib(?:64)?/riak/bin/riak(?=[ \t]|$)`, 'gm');
  return text.replace(prefix, (_, indent, environment) => {
    const overrides = environment.match(new RegExp(assignment, 'g')) || [];
    const kept = overrides.filter(v => !/^VMARGS_PATH=(?:\/var\/lib\/riak\/vm\.args|'\/var\/lib\/riak\/vm\.args'|"\/var\/lib\/riak\/vm\.args")$/.test(v));
    return indent + (kept.length ? kept.join(' ') + ' ' : '') + 'riak';
  });
}
function displayExampleDescription(text) {
  return text.replace(/(^```(?:sh|bash|shell|console)\s*\n)([\s\S]*?)(^```[ \t]*$)/gm,
    (_, start, commands, end) => start + displayShellInvocation(commands) + end);
}
function validateEntry(entry, file) {
  const allowed = ['tags', 'versions', 'reviewed_against', 'summary', 'description', 'syntax', 'related_documentation', ...arrayFields, 'example_overrides', 'error_overrides', 'option_overrides'];
  if (!plain(entry) || Object.keys(entry).some(k => !allowed.includes(k))) throw new Error(`${file}: unknown annotation fields`);
  if (entry.tags) validateTags(entry.tags, file);
  if (entry.versions && (!Array.isArray(entry.versions) || entry.versions.some(v => !/^\d+\.\d+\.\d+$/.test(v)))) throw new Error(`${file}: invalid versions`);
  if (entry.reviewed_against && (!plain(entry.reviewed_against) || Object.entries(entry.reviewed_against).some(([v, h]) => !/^\d+\.\d+\.\d+$/.test(v) || !/^[a-f0-9]{64}$/.test(h)))) throw new Error(`${file}: invalid review fingerprints`);
  for (const field of ['summary', 'description', 'syntax', 'related_documentation']) if (field in entry && typeof entry[field] !== 'string') throw new Error(`${file}: ${field} must be text`);
  if ('option_overrides' in entry) {
    if (!plain(entry.option_overrides)) throw new Error(`${file}: option_overrides must map flag names to fields`);
    for (const patch of Object.values(entry.option_overrides)) {
      if (!plain(patch) || Object.keys(patch).some(k => !['description', 'datatype', 'required', 'repeatable', 'allowed_values', 'default', 'omit'].includes(k)) ||
          (['description', 'datatype'].some(k => k in patch && typeof patch[k] !== 'string')) ||
          (['required', 'repeatable', 'omit'].some(k => k in patch && typeof patch[k] !== 'boolean')) ||
          ('allowed_values' in patch && (!Array.isArray(patch.allowed_values) || patch.allowed_values.some(v => typeof v !== 'string'))) ||
          ('default' in patch && !['string', 'number', 'boolean'].includes(typeof patch.default))) throw new Error(`${file}: invalid option override`);
    }
  }
  for (const field of arrayFields) {
    if (!(field in entry)) continue;
    if (!Array.isArray(entry[field])) throw new Error(`${file}: ${field} must explicitly replace with an array`);
    const ids = new Set();
    for (const item of entry[field]) {
      if (field === 'notes') {
        if (typeof item !== 'string') throw new Error(`${file}: notes must be strings`);
        continue;
      }
      if (!plain(item) || Object.keys(item).some(k => !fields[field].includes(k)) || Object.entries(item).some(([k,v]) => ['required', 'repeatable'].includes(k) ? typeof v !== 'boolean' : k === 'allowed_values' ? !Array.isArray(v) || v.some(x => typeof x !== 'string') : typeof v !== 'string')) throw new Error(`${file}: invalid ${field} entry`);
      const id = item[['arguments', 'shared_arguments'].includes(field) ? 'name' : 'id'];
      if (!id || ids.has(id)) throw new Error(`${file}: missing or duplicate ${field} ID`);
      ids.add(id);
      const required = ['arguments', 'shared_arguments'].includes(field) ? ['format'] : field === 'examples' ? ['invocation', 'description'] : field === 'errors' ? ['condition', 'description', 'remedy'] : ['description'];
      if (required.some(k => !item[k])) throw new Error(`${file}: incomplete ${field} entry ${id}`);
      if (item.outcome && !['success', 'error'].includes(item.outcome)) throw new Error(`${file}: invalid outcome`);
    }
  }
  for (const [field, permitted] of [['example_overrides', exampleFields], ['error_overrides', fields.errors]]) {
    if (!(field in entry)) continue;
    if (!plain(entry[field])) throw new Error(`${file}: ${field} must map IDs to fields`);
    for (const patch of Object.values(entry[field])) {
      if (!plain(patch) || Object.keys(patch).some(k => !permitted.includes(k) || k === 'id') || Object.values(patch).some(v => typeof v !== 'string')) throw new Error(`${file}: invalid ${field}`);
      if (patch.outcome && !['success', 'error'].includes(patch.outcome)) throw new Error(`${file}: invalid outcome`);
    }
  }
}

function readLayers(directory, version) {
  const layers = readMarkdownLayers(directory, version);
  for (const layer of layers) for (const entry of Object.values(layer.commands)) validateEntry(entry, layer.name);
  return layers;
}
function buildAnnotatedReference(document, { overrideRoot = defaultOverrideRoot } = {}) {
  const reference = buildReference(document);
  const scenarioReports = new Map((document.coverage?.scenarios?.scenarios || []).map(s => [s.id, s]));
  const byId = new Map(document.commands.map(c => [c.id, c]));
  const report = { version: document.version, commands: [], issues: [], overridden: [] };
  const layers = readLayers(overrideRoot, document.version);
  for (const layer of layers) for (const [id, entry] of Object.entries(layer.commands)) {
    if (entry.versions && !entry.versions.includes(document.version)) continue;
    const section = reference.sections.find(s => s.route.startsWith('erlang/') && id === `erlang:${s.title}`);
    if (section) {
      section.reference = {...section.reference, ...structuredClone(entry)};
      delete layer.commands[id];
      continue;
    }
    if (!byId.has(id) && reference.pages.some(p => p.key === id)) {
      const target = reference.pages.find(p => p.key === id).ids[0];
      delete layer.commands[id]; layer.commands[target] = entry;
    } else if (!byId.has(id)) throw new Error(`${layer.name}: override targets missing command ${id} in ${document.version}`);
  }
  const merged = new Map();
  for (const command of document.commands) {
    const auto = command.reference || {};
    const content = structuredClone(auto);
    content.examples ??= (command.usage_examples || []).map((e, i) => ({ id: `usage-${i + 1}`, ...e }));
    for (const field of arrayFields) content[field] ||= [];
    // Observed output is immutable evidence, separate from editable explanations.
    const evidence = content.examples.map(e => ({ ...e, command_id: command.id }));
    content.examples = content.examples.map(e => Object.fromEntries(Object.entries(e).filter(([k]) => exampleFields.includes(k))));
    const overrides = [];
    let argumentsDefined = Object.hasOwn(auto, 'arguments');
    for (const layer of layers) {
      const entry = layer.commands[command.id];
      if (!entry || entry.versions && !entry.versions.includes(document.version)) continue;
      const expected = entry.reviewed_against?.[document.version];
      if (expected !== reviewFingerprint(command)) report.issues.push({ command: command.id, file: layer.name, status: expected ? 'stale' : 'unreviewed', fingerprint: reviewFingerprint(command) });
      if (entry.tags) content.tags = {...content.tags, ...entry.tags};
      for (const field of ['summary', 'description', 'syntax', 'related_documentation', ...arrayFields]) if (field in entry) content[field] = structuredClone(entry[field]);
      for (const [id, patch] of Object.entries(entry.example_overrides || {})) {
        const example = content.examples.find(e => e.id === id);
        if (!example) {
          if (!patch.invocation || !patch.description) throw new Error(`${layer.name}: unknown example ${id} on ${command.id}; new examples need invocation and description`);
          content.examples.push({id, ...patch});
        } else Object.assign(example, patch);
      }
      for (const [id, patch] of Object.entries(entry.error_overrides || {})) {
        const error = content.errors.find(e => e.id === id);
        if (error) Object.assign(error, patch);
        else {
          if (!patch.condition || !patch.description || !patch.remedy) throw new Error(`${layer.name}: new error ${id} needs condition, description and remedy`);
          content.errors.push({id, ...patch});
        }
      }
      for (const [name, patch] of Object.entries(entry.option_overrides || {})) {
        const page = reference.pages.find(p => p.ids.includes(command.id));
        const option = page?.options.find(o => o.name === name);
        if (!option) throw new Error(`${layer.name}: unknown option ${name} on ${command.id}`);
        for (const field of ['description', 'datatype', 'required', 'repeatable', 'omit']) if (field in patch) option[field] = patch[field];
        if ('allowed_values' in patch) option.allowedValues = structuredClone(patch.allowed_values);
        if ('default' in patch) option.defaultValue = patch.default;
      }
      if ('arguments' in entry) argumentsDefined = true;
      overrides.push(layer.name);
      report.overridden.push({ command: command.id, file: layer.name });
    }
    for (const example of content.examples) {
      if (command.context === 'shell') {
        example.display_invocation = displayShellInvocation(example.invocation);
        example.display_description = displayExampleDescription(example.description);
      }
      const observed = evidence.find(e => e.id === example.id && e.invocation === example.invocation);
      if (observed?.verification) {
        if (observed.verification.command_fingerprint === fingerprint(command) && observed.verification.image_id === document.runtime?.id) {
          example.observed = {...observed};
          const report = scenarioReports.get(observed.verification.scenario);
          if (report && report.sha256 === observed.verification.sha256 && report.image_id === observed.verification.image_id) {
            example.observed.test_steps = (report.steps || []).filter(step =>
              ['setup', `case_setup:${observed.verification.case}`, `case:${observed.verification.case}`, `verify:${observed.verification.case}`].includes(step.phase));
          }
        }
        else report.issues.push({ command: command.id, example: example.id, status: 'stale_evidence' });
      }
    }
    merged.set(command.id, { content, evidence, overrides, argumentsDefined });
  }
  const uniqueBy = (items, key) => [...new Map(items.map(i => [i[key], i])).values()];
  for (const page of reference.pages) {
    const sources = page.ids.map(id => merged.get(id));
    const content = {
      tags: mergeTags(sources.map(s => s.content.tags)),
      summary: sources.map(s => s.content.summary).filter(Boolean).join('\n\n'),
      description: sources.map(s => s.content.description).filter(Boolean).join('\n\n'),
      syntax: sources.map(s => s.content.syntax).filter(Boolean).join('\n\n'),
      related_documentation: sources.map(s => s.content.related_documentation).filter(Boolean).join('\n\n'),
      arguments: uniqueBy(sources.flatMap(s => s.content.arguments), 'name'),
      shared_arguments: uniqueBy(sources.flatMap(s => s.content.shared_arguments), 'name'),
      argumentsDefined: sources.some(s => s.argumentsDefined),
      examples: uniqueBy(sources.flatMap(s => s.content.examples), 'id'),
      results: uniqueBy(sources.flatMap(s => s.content.results), 'id'),
      errors: uniqueBy(sources.flatMap(s => s.content.errors), 'id'),
      notes: [...new Set(sources.flatMap(s => s.content.notes))],
      evidence: sources.flatMap(s => s.evidence),
      overrides: [...new Set(sources.flatMap(s => s.overrides))]
    };
    for (const example of content.examples) example.title ||= example.id.replace(/^[^:]+:/, '').replace(/-/g, ' ');
    page.reference = content;
    const rawArguments = content.argumentsDefined ? content.arguments : page.forms.flatMap(f => f.arguments);
    page.options = page.options.filter(o => !o.omit);
    page.parameters = [...uniqueBy(rawArguments.map(a => ({...a, name: a.name || a.key || `Argument ${a.position}`,
      kind: 'Argument', description: a.description || a.format || '', allowedValues: a.allowed_values,
      ...(Object.hasOwn(a, 'default') ? {defaultValue: a.default} : {})})), 'name'),
      ...page.options.map(o => ({...o, kind: 'Option'}))];
    const missing = ['examples', 'results', 'errors'].filter(k => !content[k].length);
    report.commands.push({ key: page.key, route: page.route, missing,
      tested_examples: content.examples.filter(e => e.observed).length,
      overridden: Boolean(content.overrides.length) });
  }
  // Keep each call's requiredness and type, but describe shared meanings once
  // at the nearest annotated ancestor. Syntax still has all parameter names.
  for (const page of reference.pages.filter(p => p.context === 'erlang')) {
    const ancestors = [...reference.pages, ...reference.sections]
      .filter(p => page.route.startsWith(p.route + '/') && p.reference?.shared_arguments?.length)
      .sort((a,b) => b.route.length - a.route.length);
    for (const parameter of page.parameters) {
      const parent = ancestors.find(p => p.reference.shared_arguments.some(a => a.name === parameter.name));
      if (parent) parameter.shared = {route: parent.route, title: parent.title,
        anchor: 'argument-' + parameter.name.toLowerCase()};
    }
  }
  // Shared errors are documented once on the ancestors that define them.
  for (const page of reference.pages) {
    page.reference.sharedErrors = reference.pages.filter(parent => (page.route.startsWith(parent.route + '/') || (page.context === 'erlang' && parent.key === 'shell:riak attach')) && parent.reference.errors.length)
      .map(parent => ({route: parent.route, title: parent.title}));
    const coverage = report.commands.find(c => c.key === page.key);
    if (page.reference.sharedErrors.length) coverage.missing = coverage.missing.filter(k => k !== 'errors');
  }
  report.total = report.commands.length;
  report.complete = report.commands.filter(c => !c.missing.length).length;
  reference.annotationCoverage = report;
  return buildSyntax(reference, document);
}
module.exports = { buildAnnotatedReference, fingerprint, reviewFingerprint, readLayers, validateEntry, defaultOverrideRoot, annotationFiles };
