(() => {
  'use strict';

  const SEMVER_PATTERN = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$/;

  const parseSemVer = (value) => {
    const match = SEMVER_PATTERN.exec(String(value || ''));
    if (!match) throw new Error(`Invalid Semantic Version: ${value}`);
    return { major: Number(match[1]), minor: Number(match[2]), patch: Number(match[3]), prerelease: match[4] || '' };
  };

  const comparePrerelease = (left, right) => {
    if (left === right) return 0;
    if (!left) return 1;
    if (!right) return -1;
    const a = left.split('.');
    const b = right.split('.');
    for (let index = 0; index < Math.max(a.length, b.length); index += 1) {
      if (a[index] === undefined) return -1;
      if (b[index] === undefined) return 1;
      if (a[index] === b[index]) continue;
      const aNumeric = /^\d+$/.test(a[index]);
      const bNumeric = /^\d+$/.test(b[index]);
      if (aNumeric && bNumeric) return Number(a[index]) - Number(b[index]);
      if (aNumeric) return -1;
      if (bNumeric) return 1;
      return a[index].localeCompare(b[index]);
    }
    return 0;
  };

  const compareSemVer = (left, right) => {
    const a = parseSemVer(left);
    const b = parseSemVer(right);
    return a.major - b.major || a.minor - b.minor || a.patch - b.patch || comparePrerelease(a.prerelease, b.prerelease);
  };

  const versionInBrand = (version, brand) =>
    (!brand.minVersion || compareSemVer(version, brand.minVersion) >= 0) &&
    (!brand.maxVersionExclusive || compareSemVer(version, brand.maxVersionExclusive) < 0);

  const resolveBrand = (version, brands) => {
    const matches = brands.filter((brand) => versionInBrand(version, brand));
    if (matches.length !== 1) throw new Error(`Version ${version} resolves to ${matches.length} brands`);
    return matches[0];
  };

  const resolveOs = (requestedId, sourceOs, targetVersion) => {
    const supported = targetVersion.operatingSystems || [];
    const exact = supported.find((os) => os.id === requestedId);
    if (exact) return exact;
    const family = sourceOs?.family;
    if (family) {
      const architecture = sourceOs?.architecture;
      const architectureMatch = architecture && supported.find((os) => os.family === family && os.architecture === architecture);
      if (architectureMatch) return architectureMatch;
      const familyDefault = supported.find((os) => os.family === family && os.defaultForFamily);
      if (familyDefault) return familyDefault;
      const familyMatch = supported.find((os) => os.family === family);
      if (familyMatch) return familyMatch;
    }
    return supported.find((os) => os.id === targetVersion.defaultOs) || supported[0] || null;
  };

  const resolveValue = (versionData, osId, key) => {
    const osValues = versionData.values?.[osId] || {};
    if (Object.prototype.hasOwnProperty.call(osValues, key)) return osValues[key];
    const commonValues = versionData.values?.common || {};
    if (Object.prototype.hasOwnProperty.call(commonValues, key)) return commonValues[key];
    throw new Error(`Missing documentation value ${versionData.product}/${versionData.version}/${osId}/${key}`);
  };

  const buildVersionCandidates = ({ currentUrl, productBase, currentVersion, targetVersion }) => {
    const url = new URL(currentUrl, 'https://docs.invalid');
    const base = new URL(productBase, url.origin);
    const marker = `${base.pathname}${currentVersion}/`;
    const markerIndex = url.pathname.indexOf(marker);
    let suffix = markerIndex >= 0 ? url.pathname.slice(markerIndex + marker.length) : '';
    suffix = suffix.replace(/^\/+|\/+$/g, '');
    const candidates = [];
    while (suffix) {
      candidates.push(new URL(`${targetVersion}/${suffix}/`, base).href);
      suffix = suffix.includes('/') ? suffix.slice(0, suffix.lastIndexOf('/')) : '';
    }
    candidates.push(new URL(`${targetVersion}/`, base).href);
    return [...new Set(candidates)];
  };

  const resolveAssetUrl = (asset, assetBase, origin) => new URL(asset, new URL(assetBase, origin)).href;

  const configurationDefaultForOs = (defaults, osId) => {
    const selected = defaults?.[osId];
    if (!selected) return { hasDefault: false, value: '', osSpecific: false };
    return {
      hasDefault: Boolean(selected.hasDefault),
      value: selected.value == null ? '' : String(selected.value),
      osSpecific: Boolean(selected.osSpecific)
    };
  };

  const writeClipboard = async (value) => {
    if (navigator.clipboard?.writeText && window.isSecureContext) {
      await navigator.clipboard.writeText(value);
      return;
    }
    const field = document.createElement('textarea');
    field.value = value;
    field.setAttribute('readonly', '');
    field.style.position = 'fixed';
    field.style.opacity = '0';
    document.body.append(field);
    field.select();
    try {
      if (!document.execCommand('copy')) throw new Error('Copy command was rejected');
    } finally {
      field.remove();
    }
  };

  const copyIconMarkup = `
    <span class="download-copy-icon" aria-hidden="true">
      <svg class="download-copy-glyph" viewBox="0 0 24 24" focusable="false">
        <rect x="9" y="9" width="11" height="11" rx="2"></rect>
        <path d="M15 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h3"></path>
      </svg>
      <svg class="download-copy-tick" viewBox="0 0 24 24" focusable="false">
        <path d="m6 12 4 4 8-9"></path>
      </svg>
    </span>`;
  const hashIconMarkup = `
    <svg class="download-hash-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M10 3 8 21M16 3l-2 18M4 9h16M3 15h16"></path>
    </svg>`;

  const copyValue = async (button) => {
    const originalLabel = button.dataset.copyLabel || button.getAttribute('aria-label') || 'Copy';
    try {
      await writeClipboard(button.dataset.copyValue);
      button.classList.remove('is-copy-failed');
      button.classList.add('is-copied');
      button.setAttribute('aria-label', `${originalLabel} copied`);
      button.title = `${originalLabel} copied`;
    } catch {
      button.classList.remove('is-copied');
      button.classList.add('is-copy-failed');
      button.setAttribute('aria-label', `${originalLabel} failed`);
      button.title = `${originalLabel} failed`;
    }
    window.clearTimeout(Number(button.dataset.copyResetTimer || 0));
    const timer = window.setTimeout(() => {
      button.classList.remove('is-copied', 'is-copy-failed');
      button.setAttribute('aria-label', originalLabel);
      button.title = originalLabel;
      delete button.dataset.copyResetTimer;
    }, 1500);
    button.dataset.copyResetTimer = String(timer);
  };

  const createCopyButton = (label, value) => {
    const button = document.createElement('button');
    button.className = 'download-copy';
    button.type = 'button';
    button.innerHTML = copyIconMarkup;
    button.dataset.copyLabel = label;
    button.dataset.copyValue = value;
    button.setAttribute('aria-label', label);
    button.title = label;
    button.setAttribute('aria-live', 'polite');
    return button;
  };

  const createDownloadChecksum = (download) => {
    if (!download.checksum?.value) return null;
    const actions = document.createElement('div');
    actions.className = 'download-actions';
    const toggle = document.createElement('button');
    toggle.className = 'download-checksum-toggle';
    toggle.type = 'button';
    toggle.innerHTML = hashIconMarkup;
    toggle.dataset.downloadChecksumToggle = '';
    toggle.setAttribute('aria-label', 'Show checksum');
    toggle.title = 'Show checksum';
    toggle.setAttribute('aria-expanded', 'false');
    const panel = document.createElement('div');
    panel.className = 'download-checksum-panel';
    panel.dataset.downloadChecksumPanel = '';
    panel.hidden = true;
    const checksumLine = document.createElement('p');
    checksumLine.className = 'download-checksum-value';
    const algorithm = document.createElement('strong');
    algorithm.textContent = download.checksum.algorithm === 'sha256'
      ? 'SHA-256'
      : download.checksum.algorithm.toUpperCase();
    const value = document.createElement('code');
    value.textContent = download.checksum.value;
    checksumLine.append(algorithm, value);
    const checksumActions = document.createElement('div');
    checksumActions.className = 'download-checksum-actions';
    checksumActions.append(createCopyButton('Copy checksum', download.checksum.value));
    panel.append(checksumLine, checksumActions);
    const copyUrl = createCopyButton('Copy URL', download.url);
    copyUrl.classList.add('download-copy-url');
    actions.append(toggle, copyUrl, panel);
    return actions;
  };

  const configurationSearchPattern = (value) => String(value)
    .split(/\s+/u)
    .map((part) => part.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
    .join('[\\s._-]+');

  const configurationSearchExpression = (value, mode = 'contains', flags = 'iu') => {
    const pattern = mode === 'regex' ? String(value) : configurationSearchPattern(value);
    const wordCharacter = '[^\\s._-]';
    if (mode === 'whole-word') return new RegExp(`(?<!${wordCharacter})${pattern}(?!${wordCharacter})`, flags);
    if (mode === 'word-prefix') return new RegExp(`(?<!${wordCharacter})${pattern}`, flags);
    if (mode === 'word-suffix') return new RegExp(`${pattern}(?!${wordCharacter})`, flags);
    return new RegExp(pattern, flags);
  };

  const api = { parseSemVer, compareSemVer, resolveBrand, resolveOs, resolveValue, buildVersionCandidates, resolveAssetUrl, configurationDefaultForOs, configurationSearchPattern, configurationSearchExpression };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.OpenRiakDocs = api;
  if (typeof document === 'undefined') return;

  const contextNode = document.getElementById('docs-context');
  if (!contextNode) return;
  const context = JSON.parse(contextNode.textContent);
  const versions = [...context.versions].sort((a, b) => compareSemVer(b.version, a.version));
  const currentVersion = versions.find((item) => item.version === context.currentVersion) || versions[0];
  const storageKey = `openriak-docs-os:${context.product.id}`;
  let selectedOs;

  const osById = (versionData, id) => versionData.operatingSystems.find((os) => os.id === id);
  const initialOs = () => {
    const params = new URLSearchParams(window.location.search);
    const explicit = params.get('os');
    if (explicit && osById(currentVersion, explicit)) return osById(currentVersion, explicit);
    const remembered = window.localStorage.getItem(storageKey);
    if (remembered && osById(currentVersion, remembered)) return osById(currentVersion, remembered);
    return osById(currentVersion, currentVersion.defaultOs) || currentVersion.operatingSystems[0];
  };

  const applyValues = () => {
    document.querySelectorAll('[data-doc-value]').forEach((node) => {
      const optional = node.dataset.docOptional === 'true';
      let value;
      try {
        value = resolveValue(currentVersion, selectedOs.id, node.dataset.docValue);
      } catch (error) {
        if (!optional) throw error;
        value = '';
      }
      node.hidden = optional && !value;
      if (!value) return;
      if (node.dataset.docBind === 'href') node.href = value;
      else node.textContent = value;
    });
  };

  const applyConfigurationReferences = () => {
    document.querySelectorAll('[data-configuration-reference]').forEach((reference) => {
      if (!reference.configurationDefaults) {
        const data = reference.querySelector('[data-configuration-reference-defaults]');
        reference.configurationDefaults = data ? JSON.parse(data.textContent) : {};
      }
      reference.querySelectorAll('[data-configuration-key]').forEach((row) => {
        const defaults = reference.configurationDefaults[row.dataset.configurationKey] || {};
        const selectedDefault = configurationDefaultForOs(defaults, selectedOs.id);
        const value = row.querySelector('[data-configuration-default-value]');
        const empty = row.querySelector('[data-configuration-default-empty]');
        const copy = row.querySelector('[data-configuration-default-copy]');
        const osSpecific = row.querySelector('[data-configuration-os-specific]');
        const osIcon = row.querySelector('[data-configuration-os-icon]');
        if (value) {
          value.hidden = !selectedDefault.hasDefault;
          value.textContent = selectedDefault.value;
        }
        if (empty) empty.hidden = selectedDefault.hasDefault;
        if (copy) {
          copy.hidden = !selectedDefault.hasDefault;
          copy.dataset.copyValue = selectedDefault.value;
        }
        if (osSpecific) osSpecific.hidden = !selectedDefault.osSpecific;
        if (osIcon) {
          osIcon.src = osAssetUrl(selectedOs.logo);
          osIcon.alt = selectedOs.displayName;
          osIcon.title = selectedOs.displayName;
        }
      });
      reference.refreshConfigurationTable?.();
    });
  };

  const setupConfigurationReferenceTables = () => {
    const searchModeStorageKey = 'openriak-docs-configuration-search-mode';
    const searchModes = new Set(['contains', 'whole-word', 'word-prefix', 'word-suffix', 'regex']);
    const storedSearchMode = window.localStorage.getItem(searchModeStorageKey);
    const rememberedSearchMode = searchModes.has(storedSearchMode) ? storedSearchMode : 'contains';
    const searchableTextNodes = (row) => {
      const nodes = [];
      const walker = document.createTreeWalker(row, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        const parent = node.parentElement;
        const excluded = parent?.closest('button, script, style, [hidden], .sr-only');
        if (!node.nodeValue || !parent || (excluded && excluded !== row)) continue;
        nodes.push(node);
      }
      return nodes;
    };
    const clearHighlights = (reference) => {
      reference.querySelectorAll('mark[data-configuration-search-highlight]').forEach((mark) => {
        const parent = mark.parentNode;
        mark.replaceWith(document.createTextNode(mark.textContent));
        parent?.normalize();
      });
    };
    const highlightMatches = (row, query, mode) => {
      searchableTextNodes(row).forEach((node) => {
        const text = node.nodeValue;
        const expression = configurationSearchExpression(query, mode, 'giu');
        let start = 0;
        let match = expression.exec(text);
        if (!match) return;
        const fragment = document.createDocumentFragment();
        while (match) {
          if (!match[0].length) return;
          fragment.append(document.createTextNode(text.slice(start, match.index)));
          const mark = document.createElement('mark');
          mark.dataset.configurationSearchHighlight = '';
          mark.textContent = match[0];
          fragment.append(mark);
          start = expression.lastIndex;
          match = expression.exec(text);
        }
        fragment.append(document.createTextNode(text.slice(start)));
        node.replaceWith(fragment);
      });
    };
    document.querySelectorAll('[data-configuration-reference]').forEach((reference) => {
      const input = reference.querySelector('[data-configuration-search]');
      const modeSelect = reference.querySelector('[data-configuration-search-mode]');
      const result = reference.querySelector('[data-configuration-results]');
      const sortButton = reference.querySelector('[data-configuration-sort]');
      const sortHeading = reference.querySelector('[data-configuration-sort-heading]');
      const body = reference.querySelector('.configuration-reference-table tbody');
      if (!input || !modeSelect || !result || !sortButton || !sortHeading || !body) return;
      modeSelect.value = rememberedSearchMode;
      const rows = () => [...body.querySelectorAll('[data-configuration-key]')];
      const refresh = () => {
        clearHighlights(reference);
        const mode = modeSelect.value;
        const query = mode === 'regex' ? input.value : input.value.trim();
        let queryExpression = null;
        try {
          queryExpression = query ? configurationSearchExpression(query, mode) : null;
          input.removeAttribute('aria-invalid');
          result.removeAttribute('data-configuration-search-error');
        } catch (error) {
          input.setAttribute('aria-invalid', 'true');
          result.dataset.configurationSearchError = '';
          result.value = 'Invalid regular expression';
          result.textContent = result.value;
          rows().forEach((row) => { row.hidden = false; });
          return;
        }
        let visible = 0;
        rows().forEach((row) => {
          const nodes = searchableTextNodes(row);
          const matches = !queryExpression || nodes.some((node) => queryExpression.test(node.nodeValue));
          row.hidden = !matches;
          if (!matches) return;
          visible += 1;
          if (query) highlightMatches(row, query, mode);
        });
        const total = rows().length;
        result.value = query ? `${visible} of ${total} rows` : `${total} rows`;
        result.textContent = result.value;
      };
      reference.refreshConfigurationTable = refresh;
      input.addEventListener('input', refresh);
      modeSelect.addEventListener('change', () => {
        if (!searchModes.has(modeSelect.value)) return;
        window.localStorage.setItem(searchModeStorageKey, modeSelect.value);
        document.querySelectorAll('[data-configuration-search-mode]').forEach((select) => {
          select.value = modeSelect.value;
          select.closest('[data-configuration-reference]')?.refreshConfigurationTable?.();
        });
      });
      sortButton.addEventListener('click', () => {
        const direction = sortButton.dataset.sortDirection === 'ascending' ? 'descending' : 'ascending';
        const multiplier = direction === 'ascending' ? 1 : -1;
        rows()
          .sort((left, right) => multiplier * left.dataset.configurationKey.localeCompare(right.dataset.configurationKey, undefined, { numeric: true, sensitivity: 'base' }))
          .forEach((row) => body.append(row));
        sortButton.dataset.sortDirection = direction;
        sortHeading.setAttribute('aria-sort', direction);
        const nextDirection = direction === 'ascending' ? 'descending' : 'ascending';
        sortButton.setAttribute('aria-label', `Sort config name ${nextDirection}`);
        sortButton.title = `Sort config name ${nextDirection}`;
        refresh();
      });
      refresh();
    });
  };

  const renderDownloads = () => {
    document.querySelectorAll('[data-download-os-select]').forEach((button) => {
      const isSelected = button.dataset.downloadOsSelect === selectedOs.id;
      button.setAttribute('aria-pressed', String(isSelected));
      button.classList.toggle('is-active', isSelected);
    });
    document.querySelectorAll('[data-selected-download-os]').forEach((label) => {
      label.textContent = osLabel(selectedOs);
    });
    document.querySelectorAll('[data-selected-download-logo]').forEach((logo) => {
      logo.src = osAssetUrl(selectedOs.logo);
    });
    document.querySelectorAll('[data-doc-downloads]').forEach((list) => {
      list.replaceChildren();
      const sourceGroups = [...document.querySelectorAll('[data-all-downloads] .download-package-group')]
        .filter((group) => group.dataset.downloadOsId === selectedOs.id);
      if (!sourceGroups.length) return;
      const sourceTable = sourceGroups[0].closest('table');
      const wrap = document.createElement('div');
      wrap.className = 'downloads-table-wrap';
      const table = document.createElement('table');
      table.className = 'downloads-table';
      const heading = sourceTable?.querySelector('thead');
      if (heading) table.append(heading.cloneNode(true));
      sourceGroups.forEach((sourceGroup) => {
        const group = sourceGroup.cloneNode(true);
        group.classList.remove('is-checksum-expanded');
        const checksumRow = group.querySelector('[data-download-checksum-row]');
        if (checksumRow) checksumRow.hidden = true;
        const toggle = group.querySelector('[data-download-checksum-toggle]');
        if (toggle) {
          toggle.setAttribute('aria-expanded', 'false');
          toggle.setAttribute('aria-label', 'Show checksum');
          toggle.title = 'Show checksum';
        }
        table.append(group);
      });
      wrap.append(table);
      list.append(wrap);
    });
  };

  const setupDownloadControls = () => {
    document.addEventListener('click', (event) => {
      const toggle = event.target.closest?.('[data-download-checksum-toggle]');
      if (toggle) {
        const packageRow = toggle.closest('.download-package-row');
        const checksumRow = packageRow?.nextElementSibling?.matches('[data-download-checksum-row]')
          ? packageRow.nextElementSibling
          : null;
        const panel = checksumRow || toggle.closest('.download-actions')?.querySelector('[data-download-checksum-panel]');
        if (panel) {
          panel.hidden = !panel.hidden;
          toggle.setAttribute('aria-expanded', String(!panel.hidden));
          toggle.setAttribute('aria-label', panel.hidden ? 'Show checksum' : 'Hide checksum');
          toggle.title = panel.hidden ? 'Show checksum' : 'Hide checksum';
          checksumRow?.closest('.download-package-group')?.classList.toggle('is-checksum-expanded', !panel.hidden);
        }
        return;
      }
      const button = event.target.closest?.('[data-copy-value]');
      if (button) copyValue(button);
    });
    document.querySelectorAll('[data-download-os-select]').forEach((button) => {
      button.addEventListener('click', () => {
        const os = osById(currentVersion, button.dataset.downloadOsSelect);
        if (os) setOs(os);
      });
    });
    const allDownloads = document.querySelector('[data-all-downloads]');
    document.querySelectorAll('[data-all-downloads-link]').forEach((link) => {
      link.addEventListener('click', () => { if (allDownloads) allDownloads.open = true; });
    });
    if (window.location.hash === '#all-downloads' && allDownloads) allDownloads.open = true;
  };

  const osDetails = (os) => {
    const details = [];
    if (os.codename) details.push(os.codename);
    if (os.architecture && !String(os.codename || '').toLowerCase().includes(os.architecture.toLowerCase())) details.push(os.architecture);
    return details;
  };

  const osLabel = (os) => `${os.name} ${os.version}${osDetails(os).length ? ` — ${osDetails(os).join(' · ')}` : ''}`;
  const osAssetUrl = (logo) => resolveAssetUrl(logo, context.assetBase, window.location.origin);
  let closeOsPicker = () => {};

  const renderOsPicker = () => {
    const root = document.querySelector('[data-os-control]');
    const trigger = root?.querySelector('[data-os-trigger]');
    const panel = root?.querySelector('[data-os-picker]');
    const logo = root?.querySelector('[data-os-logo]');
    const label = root?.querySelector('[data-os-label]');
    if (!root || !trigger || !panel || !logo || !label || !selectedOs) return;
    label.textContent = osLabel(selectedOs);
    logo.src = osAssetUrl(selectedOs.logo);
    panel.replaceChildren();
    const families = new Map();
    currentVersion.operatingSystems.forEach((os) => {
      if (!families.has(os.family)) families.set(os.family, []);
      families.get(os.family).push(os);
    });
    families.forEach((items, family) => {
      const section = document.createElement('section');
      section.className = 'os-family';
      const heading = document.createElement('h2');
      heading.textContent = items[0].name || family;
      section.append(heading);
      items.sort((a, b) => compareOsVersions(b.version, a.version)).forEach((os) => {
        const option = document.createElement('button');
        option.type = 'button';
        option.className = 'os-option';
        option.dataset.osId = os.id;
        option.setAttribute('role', 'option');
        option.setAttribute('aria-selected', String(os.id === selectedOs.id));
        if (os.id === selectedOs.id) option.classList.add('is-active');
        const optionLogo = document.createElement('img');
        optionLogo.className = 'os-option-logo';
        optionLogo.src = osAssetUrl(os.logo);
        optionLogo.alt = '';
        const copy = document.createElement('span');
        copy.className = 'os-option-copy';
        const name = document.createElement('strong');
        name.textContent = `${os.name} ${os.version}`;
        const details = document.createElement('span');
        details.textContent = osDetails(os).join(' · ');
        copy.append(name);
        if (details.textContent) copy.append(details);
        option.append(optionLogo, copy);
        option.addEventListener('click', () => {
          setOs(os);
          closeOsPicker(true);
        });
        section.append(option);
      });
      panel.append(section);
    });
  };

  const setupOsPicker = () => {
    const root = document.querySelector('[data-os-control]');
    const trigger = root?.querySelector('[data-os-trigger]');
    const panel = root?.querySelector('[data-os-picker]');
    if (!root || !trigger || !panel) return;
    closeOsPicker = (restoreFocus = false) => {
      panel.hidden = true;
      trigger.setAttribute('aria-expanded', 'false');
      if (restoreFocus) trigger.focus();
    };
    const open = () => {
      panel.hidden = false;
      trigger.setAttribute('aria-expanded', 'true');
    };
    trigger.addEventListener('click', () => panel.hidden ? open() : closeOsPicker());
    trigger.addEventListener('keydown', (event) => {
      if (!['ArrowDown', 'Enter', ' '].includes(event.key)) return;
      event.preventDefault();
      open();
      panel.querySelector('.os-option.is-active, .os-option')?.focus();
    });
    panel.addEventListener('keydown', (event) => {
      const options = [...panel.querySelectorAll('.os-option')];
      const current = options.indexOf(document.activeElement);
      let next = current;
      if (event.key === 'ArrowDown') next = Math.min(current + 1, options.length - 1);
      else if (event.key === 'ArrowUp') next = Math.max(current - 1, 0);
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = options.length - 1;
      else return;
      event.preventDefault();
      options[next]?.focus();
    });
    document.addEventListener('click', (event) => { if (!root.contains(event.target)) closeOsPicker(); });
    document.addEventListener('keydown', (event) => { if (event.key === 'Escape' && !panel.hidden) closeOsPicker(true); });
  };

  const compareOsVersions = (left, right) => {
    const a = String(left).split(/[.-]/).map((part) => Number.parseInt(part, 10) || 0);
    const b = String(right).split(/[.-]/).map((part) => Number.parseInt(part, 10) || 0);
    for (let i = 0; i < Math.max(a.length, b.length); i += 1) {
      if ((a[i] || 0) !== (b[i] || 0)) return (a[i] || 0) - (b[i] || 0);
    }
    return 0;
  };

  const setOs = (os) => {
    selectedOs = os;
    window.localStorage.setItem(storageKey, os.id);
    document.documentElement.dataset.selectedOs = os.id;
    const url = new URL(window.location.href);
    if (url.searchParams.has('os')) {
      url.searchParams.delete('os');
      window.history.replaceState(window.history.state, '', url);
    }
    renderOsPicker();
    applyValues();
    applyConfigurationReferences();
    renderDownloads();
  };

  const pageExists = async (url) => {
    try {
      let response = await fetch(url, { method: 'HEAD', credentials: 'same-origin' });
      if (response.status === 405) response = await fetch(url, { credentials: 'same-origin' });
      return response.ok;
    } catch {
      return false;
    }
  };

  const switchVersion = async (target) => {
    const targetOs = selectedOs
      ? resolveOs(selectedOs.id, selectedOs, target)
      : resolveOs('', null, target);
    const candidates = buildVersionCandidates({
      currentUrl: window.location.href,
      productBase: context.productBase,
      currentVersion: currentVersion.version,
      targetVersion: target.version
    });
    if (targetOs) window.localStorage.setItem(storageKey, targetOs.id);
    for (const candidate of candidates) {
      if (await pageExists(candidate)) {
        window.location.assign(candidate);
        return;
      }
    }
    window.location.assign(new URL(`${target.version}/`, new URL(context.productBase, window.location.origin)).href);
  };

  const setupVersionWarning = () => {
    const link = document.querySelector('[data-version-warning-target]');
    if (!link) return;
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const target = versions.find((version) => version.version === link.dataset.versionWarningTarget);
      if (target) switchVersion(target);
    });
  };

  const renderVersionPicker = () => {
    const root = document.querySelector('[data-version-picker]');
    const trigger = root?.querySelector('.picker-trigger');
    const panel = root?.querySelector('[data-version-panel]');
    if (!root || !trigger || !panel) return;
    const brands = [...context.product.brands].sort((a, b) => (a.displayOrder || 0) - (b.displayOrder || 0));
    brands.forEach((brand) => {
      const matching = versions.filter((version) => versionInBrand(version.version, brand));
      const section = document.createElement('section');
      section.className = 'version-brand';
      section.dataset.brand = brand.name;
      const heading = document.createElement('h2');
      heading.innerHTML = `<img src="${resolveAssetUrl(brand.logo, context.assetBase, window.location.origin)}" alt=""> <span>${brand.name}</span>`;
      section.append(heading);
      if (!matching.length) {
        const comingSoon = document.createElement('p');
        comingSoon.className = 'version-coming-soon';
        comingSoon.textContent = 'Coming soon';
        section.append(comingSoon);
        panel.append(section);
        return;
      }
      const rows = new Map();
      matching.forEach((version) => {
        const parsed = parseSemVer(version.version);
        const series = `${parsed.major}.${parsed.minor}`;
        if (!rows.has(series)) rows.set(series, []);
        rows.get(series).push(version);
      });
      [...rows.entries()].sort((a, b) => compareSemVer(`${b[0]}.0`, `${a[0]}.0`)).forEach(([series, releases]) => {
        const row = document.createElement('div');
        row.className = 'version-row';
        row.innerHTML = `<span class="version-series">${series}</span><div class="version-releases"></div>`;
        const releaseWrap = row.lastElementChild;
        releases.sort((a, b) => compareSemVer(b.version, a.version)).forEach((release, index) => {
          const button = document.createElement('button');
          button.type = 'button';
          button.textContent = release.version;
          button.className = 'version-option';
          if (index === 0) button.classList.add('is-newest');
          if (release.version === currentVersion.version) {
            button.classList.add('is-active');
            button.setAttribute('aria-current', 'page');
          }
          if (index >= 3) {
            button.classList.add('is-overflow');
            button.hidden = true;
          }
          button.addEventListener('click', () => release.version === currentVersion.version ? close() : switchVersion(release));
          releaseWrap.append(button);
        });
        if (releases.length > 3) {
          const more = document.createElement('button');
          more.type = 'button';
          more.className = 'version-more';
          more.setAttribute('aria-expanded', 'false');
          more.setAttribute('aria-label', `Show more ${series} versions`);
          more.textContent = '›';
          more.addEventListener('click', () => {
            const expanded = more.getAttribute('aria-expanded') === 'true';
            more.setAttribute('aria-expanded', String(!expanded));
            more.setAttribute('aria-label', `${expanded ? 'Show more' : 'Show fewer'} ${series} versions`);
            more.textContent = expanded ? '›' : '‹';
            releaseWrap.querySelectorAll('.is-overflow').forEach((item) => { item.hidden = expanded; });
          });
          releaseWrap.append(more);
        }
        section.append(row);
      });
      panel.append(section);
    });
    const close = () => { panel.hidden = true; trigger.setAttribute('aria-expanded', 'false'); };
    trigger.addEventListener('click', () => {
      panel.hidden = !panel.hidden;
      trigger.setAttribute('aria-expanded', String(!panel.hidden));
    });
    document.addEventListener('click', (event) => { if (!root.contains(event.target)) close(); });
    document.addEventListener('keydown', (event) => { if (event.key === 'Escape' && !panel.hidden) { close(); trigger.focus(); } });
  };

  const setupSearch = () => {
    const root = document.querySelector('[data-search]');
    if (root?.dataset.sharedSearchReady === 'true') return;
    const input = document.querySelector('[data-search-input]');
    const results = document.querySelector('[data-search-results]');
    const status = root?.querySelector('[data-search-status]');
    if (!root || !input || !results) return;
    let indexPromise;
    let cachedQuery = '';
    const hideResults = () => { results.hidden = true; };
    const highlightedUrl = (value, query) => {
      const url = new URL(value, window.location.href);
      url.searchParams.set('highlight', query);
      return url.href;
    };
    const score = (page, query) => {
      const title = (page.title || '').toLowerCase();
      const description = (page.description || '').toLowerCase();
      const content = (page.content || '').toLowerCase();
      return (title.includes(query) ? 1000 : 0)
        + (description.includes(query) ? 100 : 0)
        + (content.includes(query) ? Math.min(content.split(query).length - 1, 50) : 0);
    };
    const showCachedResults = () => {
      const query = input.value.trim().toLowerCase();
      if (query.length >= 2 && query === cachedQuery && results.childNodes.length) results.hidden = false;
    };
    const loadIndex = () => {
      if (!indexPromise) {
        const indexUrl = new URL(`${currentVersion.version}/index.json`, new URL(context.productBase, window.location.origin));
        indexPromise = fetch(indexUrl).then((response) => {
          if (!response.ok) throw new Error(`Search index returned ${response.status}`);
          return response.json();
        });
      }
      return indexPromise;
    };
    input.addEventListener('keydown', (event) => {
      if (event.key !== 'Escape') return;
      event.preventDefault();
      event.stopPropagation();
      input.value = '';
      cachedQuery = '';
      hideResults();
      results.replaceChildren();
      results.setAttribute('aria-busy', 'false');
      if (status) status.textContent = '';
    });
    input.addEventListener('click', showCachedResults);
    document.addEventListener('click', (event) => { if (!root.contains(event.target)) hideResults(); });
    input.addEventListener('input', async () => {
      const query = input.value.trim().toLowerCase();
      cachedQuery = '';
      hideResults();
      if (query.length < 2) {
        results.replaceChildren();
        results.setAttribute('aria-busy', 'false');
        if (status) status.textContent = '';
        return;
      }
      results.setAttribute('aria-busy', 'true');
      if (status) status.textContent = 'Searching…';
      try {
        const pages = await loadIndex();
        if (input.value.trim().toLowerCase() !== query) return;
        const matches = pages
          .map((page) => ({ page, score: score(page, query) }))
          .filter((match) => match.score > 0)
          .sort((left, right) => right.score - left.score)
          .slice(0, 8)
          .map((match) => match.page);
        results.replaceChildren();
        matches.forEach((page) => {
          const link = document.createElement('a');
          link.href = highlightedUrl(page.url, query);
          link.innerHTML = `<strong>${page.title}</strong><span>${page.description || ''}</span>`;
          results.append(link);
        });
        if (!matches.length) results.textContent = 'No results in this version.';
        cachedQuery = query;
        results.hidden = false;
        results.setAttribute('aria-busy', 'false');
        if (status) status.textContent = matches.length
          ? `${matches.length} search result${matches.length === 1 ? '' : 's'} found.`
          : 'No results in this version.';
      } catch (error) {
        if (input.value.trim().toLowerCase() !== query) return;
        results.textContent = 'Search is temporarily unavailable.';
        cachedQuery = query;
        results.hidden = false;
        results.setAttribute('aria-busy', 'false');
        if (status) status.textContent = 'Search is temporarily unavailable.';
        console.error(error);
      }
    });
  };

  setupOsPicker();
  setupConfigurationReferenceTables();
  selectedOs = initialOs();
  renderVersionPicker();
  setupVersionWarning();
  if (selectedOs) setOs(selectedOs);
  setupDownloadControls();
  setupSearch();
})();

