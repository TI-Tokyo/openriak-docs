'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { isDeepStrictEqual } = require('node:util');
const { sections, pairs, annotationFiles } = require('./cli-annotation-markdown');
const { parseTags, mergeTags } = require('./annotation-tags');
const defaultSettingsRoot = path.resolve(__dirname, '../../content/annotations/openriak-kv/settings');
const sorted = value => Array.isArray(value) ? value.map(sorted) : value && typeof value === 'object'
  ? Object.fromEntries(Object.keys(value).sort().map(key => [key, sorted(value[key])])) : value;
// Source line movements do not change a setting's contract.
const settingFingerprint = setting => crypto.createHash('sha256').update(JSON.stringify(sorted({ ...setting,
  definitions: (setting.definitions || []).map(({line, ...definition}) => definition)
}))).digest('hex');
const list = (body, file) => body ? body.split('\n').map(line => {
  if (!/^[-*] .+/.test(line)) throw new Error(`${file}: expected a bullet list`);
  return line.slice(2).replace(/^`([^`]+)`$/, '$1');
}) : [];
function parseSetting(text, file) {
  const result = {}, used = new Set();
  const groups = sections(text, 1, file);
  if (groups[0].body) throw new Error(`${file}: start with a # section heading`);
  for (const {title, body} of groups.slice(1)) {
    const key = title.toLowerCase();
    if (used.has(key)) throw new Error(`${file}: duplicate section ${title}`);
    used.add(key);
    if (['description', 'notes', 'examples', 'related documentation'].includes(key)) result[key.replace(/ /g, '_')] = body;
    else if (key === 'application name') result.internalName = body;
    else if (key === 'areas') result.areas = list(body, file);
    else if (key === 'tags') result.tags = parseTags(body, file);
    else if (key === 'reviewed against') {
      result.reviewed_against = pairs(body, file);
      if (Object.entries(result.reviewed_against).some(([v,h]) => !/^\d+\.\d+\.\d+$/.test(v) || !/^[a-f0-9]{64}$/.test(h))) throw new Error(`${file}: invalid review fingerprint`);
    } else if (['datatype', 'allowed values', 'units', 'constraints'].includes(key)) {
      result.datatype ||= {};
      result.datatype[{'datatype':'label', 'allowed values':'options', units:'units', constraints:'constraints'}[key]] = key === 'datatype' ? body : list(body, file);
    } else throw new Error(`${file}: unknown or immutable setting field ${title}`);
  }
  return result;
}
function annotateSettings(reference, document, {overrideRoot = defaultSettingsRoot} = {}) {
  reference = structuredClone(reference);
  const byName = new Map(reference.settings.map(setting => [setting.name, setting]));
  const report = { version: reference.version, total: reference.settings.length, complete: 0, issues: [], corrections: [] };
  for (const setting of reference.settings) {
    setting.source = structuredClone(document.settings[setting.name]);
    setting.tags = mergeTags([]);
    setting.overrides = [];
    setting.anchor = 'setting-' + Buffer.from(setting.name).toString('hex');
  }
  for (const file of annotationFiles(overrideRoot, reference.version)) {
    const name = path.relative(overrideRoot, path.dirname(file));
    const setting = byName.get(name);
    if (!setting) throw new Error(`${file}: annotation targets missing setting ${name} in ${reference.version}`);
    const entry = parseSetting(fs.readFileSync(file, 'utf8'), file);
    const expected = entry.reviewed_against?.[reference.version];
    const fingerprint = settingFingerprint(setting.source);
    if (expected !== fingerprint) report.issues.push({setting: name, file: path.relative(overrideRoot, file), status: expected ? 'stale' : 'unreviewed', fingerprint});
    const {reviewed_against, datatype, tags, ...fields} = entry;
    Object.assign(setting, fields);
    if (datatype) for (const [field, value] of Object.entries(datatype)) {
      if (!isDeepStrictEqual(setting.datatype[field], value)) report.corrections.push({setting: name, field: `datatype.${field}`, before: setting.datatype[field], after: value, file: path.relative(overrideRoot, file)});
      setting.datatype[field] = value;
    }
    if (tags) setting.tags = {...setting.tags, ...tags};
    setting.overrides.push(path.relative(overrideRoot, file));
  }
  for (const setting of reference.settings) {
    if (setting.description && setting.overrides.length && ['feature','repository','concept'].every(category => setting.tags[category].length)) report.complete++;
    else report.issues.push({setting: setting.name, status: 'incomplete'});
    // Source identity is useful for filtering, but is not evidence of a functional relationship.
    setting.related = reference.settings.filter(other => other !== setting).map(other => {
      const features = setting.tags.feature.filter(tag => other.tags.feature.includes(tag));
      const concepts = setting.tags.concept.filter(tag => other.tags.concept.includes(tag));
      return {name: other.name, anchor: other.anchor, score: features.length * 3 + concepts.length, features, concepts};
    }).filter(other => other.features.length && other.concepts.length)
      .sort((a,b) => b.score - a.score || a.name.localeCompare(b.name)).slice(0, 8);
  }
  reference.annotationCoverage = report;
  return reference;
}
module.exports = { annotateSettings, parseSetting, settingFingerprint, defaultSettingsRoot };
