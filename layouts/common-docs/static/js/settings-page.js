(() => {
  'use strict';
  const root = document.querySelector('[data-settings-page]');
  const S = window.OpenRiakSettings;
  if (!root || !S) return;
  const status = root.querySelector('[data-settings-status]');
  const sections = root.querySelector('[data-settings-sections]');
  const search = document.querySelector('[data-settings-search]');
  const results = document.querySelector('[data-settings-results]');
  let searchEntries = [];
  const pageGroup = root.dataset.settingsGroup || '';
  const base = root.dataset.settingsBase;
  const names = { appearance: 'Appearance', code: 'Code blocks', platform: 'OS and architecture', tables: 'Tables and filters', examples: 'Example values', transfer: 'Import, export, and reset' };
  const el = (tag, text, parent) => { const node = document.createElement(tag); if (text !== undefined) node.textContent = text; parent?.append(node); return node; };
  // Logo-only legends still name their settings group through accessible text.
  const settingLabel = node => (
    node.getAttribute('aria-label') ||
    node.querySelector(':scope > img[alt]')?.alt ||
    node.firstChild?.textContent || node.textContent
  ).trim();
  const message = value => { status.textContent = value; };
  const safe = fn => { try { fn(); } catch (error) { message(`Could not save: ${error.message}`); } };
  const save = (key, value) => { S.write(key, value); message('Saved in this browser.'); };
  const button = (parent, label, action) => { const node = el('button', label, parent); node.type = 'button'; node.addEventListener('click', () => safe(action)); return node; };
  function field(parent, label, value, choices, change, type = 'text') {
    const wrapper = el('label', undefined, parent);
    el('span', label, wrapper);
    const input = el(choices ? 'select' : type === 'textarea' ? 'textarea' : 'input', undefined, wrapper);
    input.setAttribute('aria-label', label);
    if (choices) choices.forEach(choice => { const [v, title] = Array.isArray(choice) ? choice : [choice, choice]; const option = el('option', title, input); option.value = v; });
    else if (type !== 'textarea') input.type = type;
    if (type === 'textarea') input.rows = 3;
    input.value = value ?? '';
    input.addEventListener('change', () => safe(() => { change(input.value); }));
    return input;
  }
  const selectSetting = (parent, label, suffix, choices) => field(parent, label, S.read(S.prefix + suffix), choices, value => save(S.prefix + suffix, value));
  function codeTable(parent) {
    const codeKey = `${S.prefix}code-options-v1`;
    const preferredKey = `${S.prefix}code-language`;
    const expandKey = 'openriak-code-output-expanded';
    const filterKey = `${S.prefix}table-filters:settings:code`;
    const state = { sort: 'type', direction: 'descending', ...S.json(filterKey) };
    const columns = [
      ['type', 'Type'], ['preferred', 'Preferred'], ['lineNumbers', 'Line Numbers'],
      ['wrap', 'Wrap'], ['shellWrap', 'Command Split'], ['outputExpanded', 'Expand']
    ];
    const maintainedTypes = JSON.parse(document.getElementById('settings-code-types').textContent);
    const savedOptions = S.json(codeKey);
    const preferred = S.read(preferredKey);
    const types = new Map(maintainedTypes.map(type => [type.id, type.title]));
    // Keep previously saved types editable, even if a maintainer retires them.
    [...Object.keys(savedOptions), preferred].filter(type => type && type !== 'global').forEach(type => {
      if (!types.has(type)) types.set(type, type);
    });
    el('p', 'Default inherits the DEFAULT row. Set All to Default clears every type override and the preferred type, keeping your DEFAULT values. Command Split applies to shell blocks.', parent);
    const wrapper = el('div', undefined, parent); wrapper.className = 'settings-table-scroll';
    wrapper.tabIndex = 0; wrapper.setAttribute('role', 'region'); wrapper.setAttribute('aria-label', 'Code block settings table');
    const table = el('table', undefined, wrapper); table.className = 'settings-code-table';
    el('caption', 'Code block preferences by type', table).className = 'sr-only';
    const head = el('thead', undefined, table);
    const headings = el('tr', undefined, head);
    const filters = el('tr', undefined, head);
    const body = el('tbody', undefined, table);
    const headers = new Map();
    const filterControls = new Map();
    const rows = [];
    const catalogControls = [];
    const count = el('p', undefined, parent); count.setAttribute('role', 'status');
    const choicesFor = key => key === 'outputExpanded' ? [['true', 'Yes'], ['false', 'No']] : [['true', 'On'], ['false', 'Off']];
    const saveState = () => S.write(filterKey, JSON.stringify(state));
    columns.forEach(([key, title]) => {
      const th = el('th', undefined, headings); th.scope = 'col'; headers.set(key, th);
      const sort = button(th, title, () => {
        state.direction = state.sort === key && state.direction === 'ascending' ? 'descending' : 'ascending';
        state.sort = key; saveState(); refresh();
      });
      sort.setAttribute('aria-label', `Sort by ${title}`);
      const cell = el('td', undefined, filters);
      const choices = key === 'type' ? null : [['', 'All'], ...(key === 'preferred' ? [['true', 'Yes'], ['false', 'No']] : [['default', 'Default'], ...choicesFor(key), ...(key === 'shellWrap' ? [['na', 'Not applicable']] : [])])];
      const input = field(cell, `Filter ${title}`, state[key] || '', choices, value => {
        state[key] = value; saveState(); refresh();
      }, key === 'type' ? 'search' : 'text');
      if (key === 'type') input.addEventListener('input', () => safe(() => { state[key] = input.value; saveState(); refresh(); }));
      filterControls.set(key, input);
      catalogControls.push({ name: key, label: `Code blocks: ${title}`, ...(choices ? { options: choices } : { type: 'text' }) });
    });
    el('th', 'Actions', headings).scope = 'col';
    const clearCell = el('td', undefined, filters);
    button(clearCell, 'Clear filters', () => {
      columns.forEach(([key]) => { state[key] = ''; filterControls.get(key).value = ''; });
      saveState(); refresh();
    });
    function addRow(type, title) {
      const row = el('tr', undefined, type === 'global' ? head : body); row.dataset.codeSettingsType = type;
      // Shared defaults stay below the column headings and above the filters.
      if (type === 'global') head.insertBefore(row, filters);
      const name = el('th', title, row); name.scope = 'row';
      const preferredCell = el('td', undefined, row);
      const item = { type, title, row, controls: {} };
      if (type !== 'global') {
        const label = el('label', `Preferred ${title}`, preferredCell);
        label.className = 'settings-preferred';
        const input = el('input', undefined, label); input.type = 'checkbox';
        input.setAttribute('aria-label', `Preferred ${title}`);
        input.addEventListener('change', () => safe(() => { save(preferredKey, input.checked ? type : ''); refresh(); }));
        item.preferred = input;
      }
      columns.slice(2).forEach(([key, label]) => {
        const cell = el('td', undefined, row);
        if (key === 'shellWrap' && type !== 'global' && !['bash', 'shell', 'sh'].includes(type)) {
          cell.textContent = '—'; cell.setAttribute('aria-label', `${label} not applicable to ${title}`);
          return;
        }
        item.controls[key] = field(cell, `${label} for ${title}`, '', [
          ...(type === 'global' ? [] : [['', 'Default']]), ...choicesFor(key)
        ], value => {
          if (type === 'global' && key === 'outputExpanded') save(expandKey, value);
          else {
            const current = S.json(codeKey); current[type] = { ...current[type] };
            if (value === '') delete current[type][key]; else current[type][key] = value === 'true';
            save(codeKey, JSON.stringify(current));
          }
          refresh();
        });
      });
      const action = el('td', undefined, row);
      button(action, type === 'global' ? 'Set All to Default' : 'Set to Default', () => {
        const current = S.json(codeKey);
        if (type === 'global') {
          S.apply({ [codeKey]: JSON.stringify(current.global ? { global: current.global } : {}), [preferredKey]: '' });
        } else {
          delete current[type];
          S.apply({ [codeKey]: JSON.stringify(current), ...(S.read(preferredKey) === type ? { [preferredKey]: '' } : {}) });
        }
        message(type === 'global' ? 'All types now use DEFAULT; preferred type cleared.' : `${title} now uses DEFAULT.`);
        refresh();
      });
      rows.push(item);
    }
    addRow('global', 'DEFAULT');
    [...types].sort((a, b) => a[1].localeCompare(b[1])).forEach(([type, title]) => addRow(type, title));
    function refresh() {
      const options = S.json(codeKey);
      const preferred = S.read(preferredKey);
      const globalExpand = S.read(expandKey) === 'true';
      rows.forEach(item => {
        item.values = { type: item.title, preferred: String(item.type !== 'global' && preferred === item.type) };
        if (item.preferred) item.preferred.checked = preferred === item.type;
        columns.slice(2).forEach(([key]) => {
          if (!item.controls[key]) { item.values[key] = 'na'; return; }
          const value = item.type === 'global' ? (key === 'outputExpanded' ? globalExpand : options.global?.[key] ?? false) : options[item.type]?.[key];
          item.controls[key].value = value === undefined ? '' : String(value);
          item.values[key] = value === undefined ? 'default' : String(value);
          const inherited = key === 'outputExpanded' ? globalExpand : options.global?.[key] ?? false;
          item.controls[key].title = value === undefined ? `Default: ${choicesFor(key).find(([v]) => v === String(inherited))[1]}` : '';
        });
        item.row.hidden = item.type !== 'global' && !columns.every(([key]) => !state[key] || (key === 'type'
          ? `${item.title} ${item.type}`.toLowerCase().includes(state[key].toLowerCase())
          : item.values[key] === state[key]));
      });
      const typeRows = rows.filter(item => item.type !== 'global');
      const column = columns.some(([key]) => key === state.sort) ? state.sort : 'type';
      const direction = state.direction === 'descending' ? -1 : 1;
      const sortValue = item => {
        if (column === 'type') return item.title;
        if (column === 'preferred') return item.values[column] === 'true' ? 'Yes' : 'No';
        if (item.values[column] === 'na') return 'Not applicable';
        return item.values[column] === 'default' ? 'Default' : choicesFor(column).find(([value]) => value === item.values[column])[1];
      };
      typeRows.sort((a, b) => direction * sortValue(a).localeCompare(sortValue(b), undefined, { numeric: true }) || a.title.localeCompare(b.title))
        .forEach(item => body.append(item.row));
      headers.forEach((header, key) => header.setAttribute('aria-sort', key === column ? (direction === 1 ? 'ascending' : 'descending') : 'none'));
      count.textContent = `${typeRows.filter(item => !item.row.hidden).length} of ${typeRows.length} types`;
    }
    refresh();
    if (pageGroup === 'code') {
      try {
        const key = `${S.prefix}filter-catalog`;
        const catalog = JSON.parse(localStorage.getItem(key) || '{}');
        catalog[filterKey] = { title: 'Code block settings', controls: catalogControls };
        localStorage.setItem(key, JSON.stringify(catalog));
      } catch {}
    }
  }
  function platformSettings(parent) {
    const D = window.OpenRiakDocs;
    const products = JSON.parse(document.getElementById('settings-platforms').textContent);
    products.forEach(product => {
      const group = el('fieldset', undefined, parent); group.dataset.settingsProduct = product.id;
      const legend = el('legend', undefined, group);
      const image = el('img', undefined, legend); image.src = product.logo; image.alt = product.name; image.className = 'settings-project-logo';
      const versions = [...product.versions].sort((a, b) => D.compareSemVer(b.version, a.version));
      const latest = versions.find(version => !D.parseSemVer(version.version).prerelease) || versions[0];
      const versionKey = `${S.prefix}version:${product.id}`;
      const osKey = `${S.prefix}os:${product.id}`;
      const archKey = `${S.prefix}architectures:${product.id}`;
      let version = versions.find(version => version.version === S.read(versionKey)) || latest;
      let selectedOs;
      const choices = [['latest', `Latest${latest ? ` (${latest.version})` : ''}`], ...versions.map(version => version.version)];
      const savedVersion = S.read(versionKey);
      if (savedVersion !== 'latest' && !versions.some(version => version.version === savedVersion)) choices.push([savedVersion, `${savedVersion} (unavailable; using latest)`]);
      const versionSelect = field(group, 'Default documentation version', savedVersion, choices, value => {
        const currentOsId = S.read(osKey);
        const previous = versions.flatMap(item => item.operatingSystems || []).find(os => os.id === currentOsId) || selectedOs;
        version = versions.find(version => version.version === value) || latest;
        const os = version && D.resolveOs(previous?.id, previous, version);
        const preferences = S.json(archKey);
        if (os) preferences[D.osReleaseKey(os)] = os.architecture;
        S.apply({ [versionKey]: value, ...(os ? { [osKey]: os.id, [archKey]: JSON.stringify(preferences) } : {}) });
        renderPlatform(); message(`Default documentation version saved for ${product.name}.`);
      });
      versionSelect.setAttribute('aria-label', `Default documentation version for ${product.name}`);
      const controls = el('div', undefined, group);
      const versionLink = el('a', 'Open documentation', group);
      function renderPlatform() {
        controls.replaceChildren();
        versionLink.href = `${product.base}${S.read(versionKey) === 'latest' ? 'latest' : version?.version || 'latest'}/`;
        const systems = version?.operatingSystems || [];
        if (!systems.length) {
          el('p', 'This documentation version does not provide an OS/architecture picker.', controls);
          return;
        }
        const preferences = S.json(archKey);
        const initial = systems.find(os => os.id === S.read(osKey)) || systems.find(os => os.id === version.defaultOs) || systems[0];
        selectedOs = D.resolveReleaseArchitecture(systems.filter(os => D.osReleaseKey(os) === D.osReleaseKey(initial)), preferences, initial.architecture, version.defaultOs);
        const osRow = el('div', undefined, controls); osRow.className = 'settings-platform-field';
        el('span', 'Operating system', osRow);
        const root = el('div', undefined, osRow); root.className = 'os-control'; root.dataset.osControl = '';
        const trigger = el('button', undefined, root); trigger.type = 'button'; trigger.className = 'picker-trigger os-picker-trigger'; trigger.dataset.osTrigger = '';
        trigger.setAttribute('aria-label', `Operating system for ${product.name}`); trigger.setAttribute('aria-expanded', 'false');
        const logo = el('img', undefined, trigger); logo.dataset.osLogo = ''; logo.alt = '';
        el('span', undefined, trigger).dataset.osLabel = '';
        el('span', '▾', trigger).setAttribute('aria-hidden', 'true');
        const panel = el('div', undefined, root); panel.dataset.osPicker = ''; panel.className = 'picker-panel os-panel'; panel.hidden = true;
        panel.id = `settings-os-${product.id}`; panel.setAttribute('role', 'listbox'); panel.setAttribute('aria-label', `Operating system for ${product.name}`); trigger.setAttribute('aria-controls', panel.id);
        const architecture = el('div', undefined, controls); architecture.dataset.downloadArchitecturePicker = ''; architecture.className = 'settings-platform-field';
        el('span', 'Architecture', architecture);
        const list = el('ul', undefined, architecture); list.dataset.downloadArchitectureOptions = ''; list.className = 'settings-architecture-options';
        list.setAttribute('aria-label', `Architecture for ${product.name}`);
        const close = D.setupOsControl(root);
        const remember = os => {
          const prefs = S.json(archKey); prefs[D.osReleaseKey(os)] = os.architecture;
          S.apply({ [osKey]: os.id, [archKey]: JSON.stringify(prefs) });
          selectedOs = os; refresh(); message(`OS and architecture saved for ${product.name}.`);
        };
        const refresh = () => {
          D.renderOsControl({ root, systems, selectedOs, assetBase: new URL('../', new URL(base, location.origin)).href, close,
            onSelect: os => remember(D.resolveReleaseArchitecture(systems.filter(item => D.osReleaseKey(item) === D.osReleaseKey(os)), S.json(archKey), selectedOs.architecture, version.defaultOs)) });
          D.renderArchitectureControl({ list, systems, selectedOs, onSelect: remember });
        };
        refresh();
      }
      renderPlatform();
    });
  }
  let currentExport = 'all';
  function render() {
    sections.replaceChildren();
    const panels = {};
    Object.entries(names).forEach(([id, name]) => {
      const panel = el('section', undefined, sections); panel.id = id;
      el('h2', name, panel); panels[id] = panel;
    });
    const { appearance, code, platform, tables, examples, transfer } = panels;
    selectSetting(appearance, 'Colour theme', 'theme', [['system', 'Device setting'], ['light', 'Light'], ['dark', 'Dark']]);
    selectSetting(appearance, 'Content width', 'content-width', ['50','75','90','98'].map(v => [v, `${v}%`]));
    selectSetting(appearance, 'Font size', 'font-size', ['100','110','125','150','200','250'].map(v => [v, `${v}%`]));
    selectSetting(appearance, 'Sidebar', 'sidebar-collapsed', [['false', 'Expanded'], ['true', 'Collapsed']]);
    const toggles = [['false', 'Off'], ['true', 'On']];
    codeTable(code);
    platformSettings(platform);
    selectSetting(tables, 'Configuration search mode', 'configuration-search-mode', ['contains','whole-word','word-prefix','word-suffix','regex']);
    el('p', 'Filters are scoped to their product or table. Visit a table to make its filter controls available here.', tables);
    let catalog = {}; try { catalog = JSON.parse(localStorage.getItem(`${S.prefix}filter-catalog`) || '{}'); } catch {}
    const filterKeys = [...new Set([...Object.keys(catalog), ...S.keys().filter(key => /(?:review|table)-filters:/.test(key))])];
    filterKeys.forEach(key => {
      if (!S.spec(key)) return;
      const group = el('fieldset', undefined, tables); el('legend', catalog[key]?.title || key.replace(S.prefix, ''), group);
      const values = S.json(key);
      const controls = catalog[key]?.controls || Object.keys(values).map(name => ({ name, label: name, type: typeof values[name] === 'boolean' ? 'boolean' : 'text' }));
      controls.forEach(control => field(group, control.label, String(values[control.name] ?? control.default ?? ''), control.type === 'boolean' ? toggles : control.options, value => {
        const next = S.json(key); next[control.name] = control.type === 'boolean' ? value === 'true' : value; save(key, JSON.stringify(next));
      }));
      button(group, 'Reset these filters', () => { S.apply({}, [key]); render(); message('Filters reset.'); });
    });
    el('p', 'These values personalize examples, not configuration-reference defaults. Use sample identities rather than passwords or credentials.', examples);
    const values = S.examples();
    function saveExamples() { save(S.exampleKey, JSON.stringify(values)); }
    field(examples, 'Cluster naming pattern', values.clusterPattern, null, value => { values.clusterPattern = value; saveExamples(); preview(); });
    field(examples, 'Node naming pattern', values.nodePattern, null, value => { values.nodePattern = value; saveExamples(); preview(); });
    el('p', 'Use {index} for 1, 2, 3 or {letter} for A, B, C. Explicit names below override the pattern.', examples);
    const previewNode = el('p', undefined, examples);
    function preview() { previewNode.textContent = `Preview: ${S.resolve('cluster', 1)}, ${S.resolve('cluster', 2)}; ${S.resolve('node', 1)}, ${S.resolve('node', 2)}`; }
    preview();
    field(examples, 'Preferred cluster size', values.clusterSize, null, value => { values.clusterSize = Number(value); saveExamples(); }, 'number');
    field(examples, 'Preferred ring size (power of two, at least 8)', values.ringSize, null, value => { values.ringSize = Number(value); saveExamples(); }, 'number');
    const labels = { cluster: 'Clusters', node: 'Nodes', backend: 'Backend profiles', listener: 'Listeners', sink: 'Replication sinks', domain: 'Domains', user: 'Users' };
    Object.entries(S.exampleFields).forEach(([name, fields]) => {
      const group = el('fieldset', undefined, examples); el('legend', labels[name], group);
      values[name].forEach((record, index) => {
        const row = el('div', undefined, group); row.className = 'settings-record';
        el('h3', `${labels[name]} · ${index + 1}`, row);
        fields.forEach(key => field(row, ({ host: 'IP address / FQDN', bind: 'Bind address', cluster: 'Cluster index', backend: 'Backend profile name', settings: 'Backend configuration', name: 'Name (blank uses pattern for clusters/nodes)' })[key] || key, record[key], null, value => {
          record[key] = key === 'port' ? Number(value) : value; saveExamples(); preview();
        }, key === 'port' ? 'number' : key === 'settings' ? 'textarea' : 'text'));
        button(row, 'Remove entry', () => {
          if (!confirm('Remove this entry? Later entries will move to the preceding index.')) return;
          values[name].splice(index, 1); saveExamples(); render();
        });
      });
      button(group, `Add ${name}`, () => { values[name].push(Object.fromEntries(fields.map(key => [key, key === 'port' ? 8087 : '']))); saveExamples(); render(); });
    });
    Object.entries(panels).filter(([id]) => id !== 'transfer' && id !== 'code').forEach(([id, panel]) => button(panel, `Reset ${names[id].toLowerCase()}`, () => {
      if (!confirm(`Reset all ${names[id].toLowerCase()} settings to defaults?`)) return;
      S.apply({}, S.keys().filter(key => S.spec(key)[0] === id)); render(); message(`${names[id]} reset.`);
    }));
    el('h3', 'Export', transfer);
    field(transfer, 'Export group', currentExport, [['all','All settings'], ...Object.entries(names).filter(([key]) => key !== 'transfer')], value => { currentExport = value; });
    button(transfer, 'Export settings', () => {
      const blob = new Blob([JSON.stringify(S.snapshot(currentExport === 'all' ? undefined : [currentExport]), null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob); const link = el('a'); link.href = url; link.download = 'openriak-docs-settings.json'; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
    el('h3', 'Import', transfer);
    el('p', 'Choose a settings file to validate and preview before applying it.', transfer);
    let pending;
    const fileLabel = el('label', undefined, transfer);
    el('span', 'Import settings file', fileLabel);
    const file = el('input', undefined, fileLabel); file.type = 'file'; file.accept = '.json,application/json';
    const mode = field(transfer, 'Import mode', 'merge', [['merge','Merge — keep settings absent from the file'], ['replace','Replace — reset settings absent from the file']], () => {});
    const previewImport = el('pre', 'Choose a file to preview changes.', transfer);
    const applyButton = button(transfer, 'Apply import', () => {
      if (!pending) return;
      if (mode.value === 'replace' && !confirm('Replace all preferences? Settings absent from this file will reset to defaults.')) return;
      S.apply(pending.settings, mode.value === 'replace' ? S.keys() : []); render(); message('Settings imported.');
    }); applyButton.disabled = true;
    file.addEventListener('change', async () => {
      pending = null; applyButton.disabled = true;
      try {
        const selected = file.files[0]; if (!selected) return;
        if (selected.size > 1000000) throw new Error('Settings files must be smaller than 1 MB.');
        pending = S.parse(await selected.text());
        previewImport.textContent = Object.entries(pending.settings).map(([key, value]) => `${key.replace(S.prefix, '')}: ${S.read(key) === value ? 'unchanged' : `${S.read(key)} → ${value}`}`).join('\n') || 'No settings in this file.';
        applyButton.disabled = false;
      } catch (error) { previewImport.textContent = error.message; }
    });
    el('h3', 'Reset', transfer);
    el('p', 'Restore all documentation preferences and example values to their original defaults.', transfer);
    button(transfer, 'Reset all settings', () => {
      if (!confirm('Reset all documentation preferences and example values?')) return;
      S.apply({}, S.keys()); render(); message('All settings reset.');
    });
    searchEntries = [];
    sections.querySelectorAll(':scope > section').forEach(section => {
      const labels = [...section.querySelectorAll('label, legend, .settings-platform-field')];
      labels.forEach((label, index) => {
        label.id = `${section.id}-setting-${index}`;
        const title = settingLabel(label);
        const headings = [];
        for (let parent = label.parentElement; parent && parent !== section; parent = parent.parentElement) {
          const legend = parent.matches('fieldset') ? parent.querySelector(':scope > legend') : null;
          if (legend && legend !== label) headings.unshift(settingLabel(legend));
        }
        const resultTitle = [names[section.id], ...headings, title].join(': ');
        searchEntries.push({ title, context: [names[section.id], ...headings].join(': '), text: `${resultTitle} ${label.textContent}`.toLowerCase(), href: `${base}${section.id}/#${label.id}` });
      });
      if (section.id !== pageGroup) section.remove();
      else section.querySelector('h2')?.remove();
    });
    alignLabels();
    filter();
  }
  function alignLabels() {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    let width = 0;
    sections.querySelectorAll('label > span:first-child, .settings-platform-field > span:first-child').forEach(label => {
      if (label.closest('table')) return;
      const style = getComputedStyle(label);
      context.font = `${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
      width = Math.max(width, context.measureText(`${label.textContent}:`).width);
    });
    root.style.setProperty('--settings-label-width', `${Math.ceil(width) + 2}px`);
  }
  window.addEventListener('resize', alignLabels);
  new MutationObserver(alignLabels).observe(document.documentElement, { attributes: true, attributeFilter: ['data-font-size'] });
  document.fonts?.ready.then(alignLabels);
  function filter() {
    const query = search.value.trim().toLowerCase();
    results.replaceChildren(); results.hidden = !query;
    if (!query) {
      document.querySelector('[data-settings-search-status]').textContent = '';
      return;
    }
    const matches = searchEntries.filter(entry => entry.text.includes(query)).slice(0, 30);
    matches.forEach(entry => {
      const link = el('a', undefined, results); link.href = entry.href;
      el('strong', entry.title, link);
      el('span', entry.context, link);
    });
    if (!matches.length) el('p', 'No matching settings.', results);
    document.querySelector('[data-settings-search-status]').textContent = `${matches.length} matching settings`;
  }
  search.addEventListener('input', filter);
  search.addEventListener('click', filter);
  search.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    event.preventDefault();
    event.stopPropagation();
    search.value = '';
    filter();
  });
  document.addEventListener('click', event => {
    if (!search.closest('.search-control').contains(event.target)) results.hidden = true;
  });
  function revealSetting() {
    let target;
    try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch { return; }
    if (!target) return;
    for (let ancestor = target.parentElement; ancestor; ancestor = ancestor.parentElement) {
      if (ancestor.tagName === 'DETAILS') ancestor.open = true;
    }
    target.scrollIntoView();
    target.querySelector('input, select, textarea, button')?.focus({ preventScroll: true });
  }
  window.addEventListener('hashchange', revealSetting);
  function updateDocumentationReturn() {
    const link = root.querySelector('[data-settings-return]');
    link.hidden = true;
    try {
      const context = JSON.parse(sessionStorage.getItem(`${S.prefix}settings-return-context`) || 'null');
      const saved = context?.url || sessionStorage.getItem(`${S.prefix}settings-return`);
      if (!saved) return;
      const destination = new URL(saved, location.href);
      const docsBase = new URL('../', new URL(base, location.origin)).pathname;
      // Also accept the URL-only record written by older versions of Settings.
      const relative = destination.pathname.startsWith(docsBase) ? destination.pathname.slice(docsBase.length) : '';
      if (destination.origin !== location.origin || !/^openriak-(kv|cs|ts)\/[^/]+\//.test(relative)) return;
      link.href = destination.href;
      const described = context && ['project', 'version', 'title'].every(key => typeof context[key] === 'string' && context[key]);
      link.textContent = described ? `Return to documentation (${context.project} ${context.version}: ${context.title})` : 'Return to documentation';
      link.hidden = false;
    } catch { /* Do not show a misleading link to the site root. */ }
  }
  updateDocumentationReturn();
  window.addEventListener('pageshow', updateDocumentationReturn);
  // Refresh controls for changes made in other tabs or through the header's display controls.
  window.addEventListener('storage', event => { if (event.isTrusted && (event.key === null || S.spec(event.key))) render(); });
  document.addEventListener('click', event => { if (event.target.closest('[data-theme-value], [data-content-width-value], [data-font-size-value]')) render(); });
  const clearButton = root.querySelector('[data-settings-clear]');
  const clearDialog = root.querySelector('[data-settings-clear-dialog]');
  if (clearButton && clearDialog) {
    clearButton.addEventListener('click', () => {
      document.dispatchEvent(new CustomEvent('openriak:modal-open', { detail: { source: 'settings-clear' } }));
      clearDialog.returnValue = '';
      clearDialog.showModal();
    });
    clearDialog.addEventListener('click', event => {
      if (event.target !== clearDialog) return;
      const bounds = clearDialog.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right ||
          event.clientY < bounds.top || event.clientY > bounds.bottom) clearDialog.close('cancel');
    });
    clearDialog.addEventListener('close', () => {
      if (clearDialog.returnValue === 'clear') safe(() => {
        S.apply({}, S.keys()); render(); message('All settings cleared. Defaults restored.');
      });
      clearButton.focus({ preventScroll: true });
    });
  }
  render();
  if (location.hash) requestAnimationFrame(revealSetting);
})();
