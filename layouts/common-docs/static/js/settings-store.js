(() => {
  'use strict';
  const prefix = 'openriak-docs-';
  const defaults = JSON.parse(document.getElementById('example-defaults')?.textContent || '{}');
  const exampleKey = `${prefix}examples-v1`;
  const object = value => value && typeof value === 'object' && !Array.isArray(value);
  const text = value => typeof value === 'string' && value.length <= 10000 && !/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(value);
  const map = (value, check) => object(value) && Object.entries(value).every(([key, item]) => !['__proto__', 'constructor', 'prototype'].includes(key) && check(item));
  const exampleFields = {
    cluster: ['name', 'backend'], node: ['name', 'host', 'cluster'],
    backend: ['name', 'type', 'settings'], listener: ['name', 'bind', 'host', 'port'],
    sink: ['name', 'host', 'port', 'cluster'], domain: ['name'], user: ['name']
  };
  const validExamples = value => object(value) && Object.entries(value).every(([key, item]) => {
    if (key === 'clusterPattern' || key === 'nodePattern') return text(item) && item.length <= 200;
    if (key === 'clusterSize') return Number.isInteger(item) && item > 0 && item <= 10000;
    if (key === 'ringSize') return Number.isInteger(item) && item >= 8 && item <= 1048576 && (item & (item - 1)) === 0;
    return Object.hasOwn(exampleFields, key) && Array.isArray(item) && item.length <= 100 && item.every(record =>
      object(record) && Object.entries(record).every(([field, entry]) => exampleFields[key].includes(field) &&
        (field === 'port' ? Number.isInteger(entry) && entry > 0 && entry <= 65535 : text(entry))));
  });
  const fixed = {
    [`${prefix}theme`]: ['appearance', 'system', ['system', 'dark', 'light']],
    [`${prefix}content-width`]: ['appearance', '75', ['50', '75', '90', '98']],
    [`${prefix}font-size`]: ['appearance', '100', ['100', '110', '125', '150', '200', '250']],
    [`${prefix}sidebar-collapsed`]: ['appearance', 'false', ['true', 'false']],
    [`${prefix}code-language`]: ['code', '', value => /^[\w+#.-]{0,50}$/.test(value)],
    'openriak-code-output-expanded': ['code', 'false', ['true', 'false']],
    [`${prefix}code-options-v1`]: ['code', '{}', value => map(value, options => map(options, v => typeof v === 'boolean') && Object.keys(options).every(k => ['lineNumbers', 'wrap', 'shellWrap', 'outputExpanded'].includes(k))), true],
    [`${prefix}configuration-search-mode`]: ['tables', 'contains', ['contains', 'whole-word', 'word-prefix', 'word-suffix', 'regex']],
    [exampleKey]: ['examples', JSON.stringify(defaults), validExamples, true]
  };
  function spec(key) {
    if (Object.hasOwn(fixed, key)) return fixed[key];
    if (/^openriak-docs-version:[\w-]+$/.test(key)) return ['platform', 'latest', value => value === 'latest' || /^\d+\.\d+\.\d+(?:-[\w.-]+)?$/.test(value)];
    if (/^openriak-docs-os:[\w-]+$/.test(key)) return ['platform', '', text];
    if (/^openriak-docs-architectures:[\w-]+$/.test(key)) return ['platform', '{}', value => map(value, text), true];
    if (/^openriak-docs-review-filters:[\w-]+$/.test(key)) return ['tables', '{}', value => map(value, item => text(item) || typeof item === 'boolean'), true];
    if (/^openriak-docs-table-filters:.{1,1000}$/.test(key)) return ['tables', '{}', value => map(value, text), true];
    return null;
  }
  function validate(key, raw) {
    const entry = spec(key);
    if (!entry || typeof raw !== 'string' || raw.length > 200000) throw new Error(`Unknown or invalid setting: ${key}`);
    let value = raw;
    if (entry[3]) { try { value = JSON.parse(raw); } catch { throw new Error(`Invalid JSON for ${key}`); } }
    if (!(Array.isArray(entry[2]) ? entry[2].includes(value) : entry[2](value))) throw new Error(`Invalid value for ${key}`);
    return raw;
  }
  function read(key) {
    try { const raw = localStorage.getItem(key); return raw === null ? spec(key)?.[1] : validate(key, raw); }
    catch { return spec(key)?.[1]; }
  }
  function json(key) { try { return JSON.parse(read(key)); } catch { return {}; } }
  function emit(key) { window.dispatchEvent(new StorageEvent('storage', { key, newValue: key ? localStorage.getItem(key) : null })); document.dispatchEvent(new CustomEvent('openriak:settings-changed', { detail: { key } })); }
  function write(key, value) { validate(key, value); localStorage.setItem(key, value); emit(key); }
  function keys() { let saved = []; try { saved = Object.keys(localStorage).filter(key => spec(key)); } catch {} return [...new Set([...Object.keys(fixed), ...saved])]; }
  function snapshot(groups) {
    return { format: 'openriak-docs-settings', version: 1, settings: Object.fromEntries(keys().filter(key => !groups || groups.includes(spec(key)[0])).map(key => [key, read(key)])) };
  }
  function parse(raw) {
    if (raw.length > 1000000) throw new Error('Settings files must be smaller than 1 MB.');
    const value = JSON.parse(raw);
    if (value?.format !== 'openriak-docs-settings' || value.version !== 1 || !object(value.settings)) throw new Error('Unsupported settings file or version.');
    Object.entries(value.settings).forEach(([key, entry]) => validate(key, entry));
    return value;
  }
  function apply(settings, remove = []) {
    // Validate before touching storage; roll back if writing fails (for example, quota).
    Object.entries(settings).forEach(([key, entry]) => validate(key, entry));
    const affected = [...new Set([...Object.keys(settings), ...remove])];
    const before = affected.map(key => [key, localStorage.getItem(key)]);
    try { remove.forEach(key => localStorage.removeItem(key)); Object.entries(settings).forEach(([key, value]) => localStorage.setItem(key, value)); }
    catch (error) { before.forEach(([key, value]) => { try { if (value === null) localStorage.removeItem(key); else localStorage.setItem(key, value); } catch {} }); throw error; }
    emit(null);
  }
  function examples() { return { ...structuredClone(defaults), ...json(exampleKey) }; }
  function resolve(group, index = 1, field = 'name', fallback = '') {
    const values = examples();
    if (group === 'clusterSize' || group === 'ringSize') return String(values[group]);
    if (!Object.hasOwn(exampleFields, group) || !Number.isInteger(index) || index < 1) return fallback;
    const value = values[group]?.[index - 1]?.[field];
    if (value !== undefined && value !== '') return String(value);
    if (field === 'name' && ['cluster', 'node'].includes(group)) {
      let n = index, letter = '';
      while (n > 0) { n--; letter = String.fromCharCode(65 + n % 26) + letter; n = Math.floor(n / 26); }
      return values[`${group}Pattern`].replaceAll('{index}', String(index)).replaceAll('{letter}', letter);
    }
    return fallback;
  }
  function substitute(source) {
    return source.replace(/<span data-example="([\w]+)" data-example-index="(\d+)" data-example-field="([\w]+)">([^<]*)<\/span>/g, (_, group, index, field, fallback) => {
      const node = document.createElement('textarea'); node.innerHTML = fallback;
      return resolve(group, Number(index), field, node.value);
    });
  }
  function renderExamples() {
    document.querySelectorAll('[data-example]').forEach(node => {
      node.dataset.exampleFallback ??= node.textContent;
      node.textContent = resolve(node.dataset.example, Number(node.dataset.exampleIndex), node.dataset.exampleField, node.dataset.exampleFallback);
    });
  }
  window.OpenRiakSettings = { prefix, fixed, spec, read, json, write, keys, snapshot, parse, apply, examples, resolve, substitute, exampleKey, exampleFields, defaults };
  const rememberDocumentation = () => {
    const { product, productName, version, pageTitle } = document.body.dataset;
    if (!product || !productName || !version || !pageTitle) return;
    try {
      sessionStorage.setItem(`${prefix}settings-return`, location.href);
      sessionStorage.setItem(`${prefix}settings-return-context`, JSON.stringify({
        url: location.href, project: productName, version, title: pageTitle
      }));
    } catch { /* Settings remain usable if session storage is unavailable. */ }
  };
  // Remember documentation independently of how Settings is opened. Other site
  // pages and Settings navigation must never overwrite this destination.
  rememberDocumentation();
  window.addEventListener('pageshow', rememberDocumentation);
  window.addEventListener('hashchange', rememberDocumentation);
  document.querySelectorAll('[data-settings-link]').forEach(link => link.addEventListener('click', rememberDocumentation));
  renderExamples();
  window.addEventListener('storage', event => { if (event.key === exampleKey || event.key === null) renderExamples(); });
})();
