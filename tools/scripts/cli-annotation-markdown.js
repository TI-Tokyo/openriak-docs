'use strict';
const fs = require('node:fs');
const path = require('node:path');

// Only headings outside fenced code delimit structured annotation sections.
function sections(text, level, file) {
  const result = []; let current = {title: '', lines: []}, fence;
  for (const line of text.replace(/\r\n/g, '\n').split('\n')) {
    const marker = line.match(/^ {0,3}(`{3,}|~{3,})/);
    if (marker) {
      if (!fence) fence = marker[1];
      else if (marker[1][0] === fence[0] && marker[1].length >= fence.length && /^ {0,3}(`+|~+)\s*$/.test(line)) fence = null;
      current.lines.push(line); continue;
    }
    const heading = !fence && line.match(new RegExp(`^#{${level}} (.+?)\\s*$`));
    if (heading) { result.push(current); current = {title: heading[1], lines: []}; }
    else current.lines.push(line);
  }
  if (fence) throw new Error(`${file}: unclosed code fence`);
  result.push(current);
  return result.map(s => ({title: s.title, body: s.lines.join('\n').trim()}));
}
function pairs(text, file) {
  const result = {};
  for (const line of text.split('\n').filter(l => l.trim())) {
    const match = line.match(/^([\w.-]+):\s*(.*?)\s*$/);
    if (!match || Object.hasOwn(result, match[1])) throw new Error(`${file}: expected a unique key: value field: ${line}`);
    result[match[1]] = match[2];
  }
  return result;
}
const unquote = text => text.replace(/^`([^`]+)`$/, '$1');
const unfence = text => text.replace(/^(`{3,}|~{3,})[^\n]*\n([\s\S]*?)\n\1$/, '$2');
const key = text => text.toLowerCase().replace(/[ -]/g, '_');
function rows(body, file) {
  const entries = sections(body, 2, file);
  if (entries[0].body) throw new Error(`${file}: table entries need ## name headings`);
  const rows = {};
  for (const entry of entries.slice(1)) {
    const name = unquote(entry.title);
    if (Object.hasOwn(rows, name)) throw new Error(`${file}: duplicate entry ${name}`);
    const fields = sections(entry.body, 3, file);
    const row = pairs(fields[0].body, file);
    for (const field of fields.slice(1)) {
      const id = key(field.title);
      if (Object.hasOwn(row, id)) throw new Error(`${file}: duplicate field ${id}`);
      if (id === 'valid_values') {
        const lines = field.body.split('\n').filter(Boolean);
        if (lines.some(l => !/^[-*] .+/.test(l))) throw new Error(`${file}: valid values must be a bullet list`);
        row.allowed_values = lines.map(l => unquote(l.slice(2)));
      } else row[id] = ['invocation', 'expected_output'].includes(id) ? unfence(field.body) : field.body;
    }
    for (const flag of ['required', 'repeatable', 'omit']) if (flag in row) {
      if (!['true', 'false'].includes(row[flag])) throw new Error(`${file}: ${flag} must be true or false`);
      row[flag] = row[flag] === 'true';
    }
    rows[name] = row;
  }
  return rows;
}
function parseMarkdown(text, file = 'annotation') {
  const entry = {}, used = new Set();
  const groups = sections(text, 1, file);
  if (groups[0].body) throw new Error(`${file}: start with a # section heading`);
  for (const {title, body} of groups.slice(1)) {
    const name = key(title);
    if (used.has(name)) throw new Error(`${file}: duplicate section ${title}`);
    used.add(name);
    if (['summary', 'description', 'syntax', 'related_documentation'].includes(name)) entry[name] = body;
    else if (name === 'notes') entry.notes = body ? [body] : [];
    else if (name === 'reviewed_against') entry.reviewed_against = pairs(body, file);
    else if (name === 'metadata') {
      const data = pairs(body, file);
      if (Object.keys(data).some(k => !['command', 'versions'].includes(k))) throw new Error(`${file}: unknown metadata field`);
      if (data.command) entry.command = data.command;
      if (data.versions) entry.versions = data.versions.split(',').map(s => s.trim());
    } else if (['arguments', 'shared_arguments', 'options', 'examples', 'errors', 'results'].includes(name)) {
      const items = rows(body, file);
      if (name === 'options') entry.option_overrides = items;
      else if (['arguments', 'shared_arguments'].includes(name)) entry[name] = Object.entries(items).map(([name, row]) => ({name, ...row, format: row.description || row.format || ''}));
      else if (name === 'results') entry.results = Object.entries(items).map(([id, row]) => ({id, ...row}));
      else if (!Object.keys(items).length) entry[name] = [];
      else entry[name === 'examples' ? 'example_overrides' : 'error_overrides'] = items;
    } else throw new Error(`${file}: unknown section ${title}`);
  }
  return entry;
}
function annotationFiles(directory, version) {
  if (!fs.existsSync(directory)) return [];
  return fs.readdirSync(directory, {withFileTypes: true}).flatMap(e => {
    const file = path.join(directory, e.name);
    return e.isDirectory() ? annotationFiles(file, version) : ['common.md', `${version}.md`].includes(e.name) ? [file] : [];
  }).sort((a, b) => Number(path.basename(a) !== 'common.md') - Number(path.basename(b) !== 'common.md') || a.localeCompare(b));
}
function readMarkdownLayers(directory, version) {
  return annotationFiles(directory, version).map(file => {
    const relative = path.relative(directory, file).split(path.sep);
    const parts = relative.slice(0, -1);
    const inferred = parts[0] === 'cli' ? `shell:${parts.slice(1).join(' ')}`
      : parts[0] === 'riak-attach' ? `erlang:${parts.slice(1).join(':')}` : '';
    if (!inferred || parts.length < 2) throw new Error(`${file}: use cli/COMMAND or riak-attach/MODULE/FUNCTION directories`);
    const entry = parseMarkdown(fs.readFileSync(file, 'utf8'), file);
    const id = entry.command || inferred;
    const canonical = id.startsWith('erlang:') ? id.replace(/\/\d+(?=:|$)/, '') : id.replace(/(?: \*)+$/, '');
    if (id !== inferred && canonical !== inferred) throw new Error(`${file}: command does not match its directory`);
    delete entry.command;
    return {name: relative.join('/'), commands: {[id]: entry}};
  });
}
module.exports = {parseMarkdown, readMarkdownLayers, annotationFiles};
