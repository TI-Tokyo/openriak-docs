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

  const api = { parseSemVer, compareSemVer, resolveBrand, resolveOs, resolveValue, buildVersionCandidates, resolveAssetUrl };
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

  const withOs = (href, osId = selectedOs?.id) => {
    const url = new URL(href, window.location.href);
    if (osId) url.searchParams.set('os', osId);
    return url.href;
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
      const downloads = currentVersion.downloads?.[selectedOs.id] || [];
      list.replaceChildren();
      downloads.forEach((download) => {
        const item = document.createElement('li');
        const link = document.createElement('a');
        link.href = download.url;
        const parts = [`OTP ${download.otp}`, download.architecture];
        if (download.variant) parts.push(download.variant);
        parts.push(download.filename);
        link.textContent = parts.join(' · ');
        item.append(link);
        if (download.checksumUrl) {
          const checksum = document.createElement('a');
          checksum.href = download.checksumUrl;
          checksum.className = 'download-checksum';
          checksum.textContent = 'checksum';
          item.append(checksum);
        }
        list.append(item);
      });
    });
  };

  const setupDownloadControls = () => {
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

  const preserveOsOnInternalLinks = () => {
    document.querySelectorAll('main a[href], .docs-sidebar a[href], .breadcrumbs a[href]').forEach((link) => {
      const url = new URL(link.href, window.location.href);
      if (url.origin === window.location.origin && url.pathname.startsWith(context.productBase)) link.href = withOs(url.href);
    });
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
    const url = new URL(window.location.href);
    url.searchParams.set('os', os.id);
    window.history.replaceState({}, '', url);
    renderOsPicker();
    applyValues();
    renderDownloads();
    preserveOsOnInternalLinks();
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
    for (const candidate of candidates) {
      if (await pageExists(candidate)) {
        window.location.assign(withOs(candidate, targetOs?.id));
        return;
      }
    }
    window.location.assign(withOs(new URL(`${target.version}/`, new URL(context.productBase, window.location.origin)).href, targetOs?.id));
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
      if (!matching.length) return;
      const section = document.createElement('section');
      section.className = 'version-brand';
      const heading = document.createElement('h2');
      heading.innerHTML = `<img src="${resolveAssetUrl(brand.logo, context.assetBase, window.location.origin)}" alt=""> <span>${brand.name}</span>`;
      section.append(heading);
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
    if (!root || !input || !results) return;
    let indexPromise;
    let cachedQuery = '';
    const hideResults = () => { results.hidden = true; };
    const highlightedUrl = (value, query) => {
      const url = new URL(withOs(value), window.location.href);
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
    });
    input.addEventListener('click', showCachedResults);
    document.addEventListener('click', (event) => { if (!root.contains(event.target)) hideResults(); });
    input.addEventListener('input', async () => {
      const query = input.value.trim().toLowerCase();
      cachedQuery = '';
      hideResults();
      if (query.length < 2) { results.replaceChildren(); return; }
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
      } catch (error) {
        if (input.value.trim().toLowerCase() !== query) return;
        results.textContent = 'Search is temporarily unavailable.';
        cachedQuery = query;
        results.hidden = false;
        console.error(error);
      }
    });
  };

  setupOsPicker();
  selectedOs = initialOs();
  renderVersionPicker();
  setupVersionWarning();
  if (selectedOs) setOs(selectedOs);
  setupDownloadControls();
  setupSearch();
})();

