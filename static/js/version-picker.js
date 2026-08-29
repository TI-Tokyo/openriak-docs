(() => {
  'use strict';

  const versionParts = (version) => String(version || '').split('.').map((part) => Number.parseInt(part, 10) || 0);

  const compareVersions = (left, right) => {
    const leftParts = versionParts(left);
    const rightParts = versionParts(right);
    const length = Math.max(leftParts.length, rightParts.length);
    for (let index = 0; index < length; index += 1) {
      const difference = (leftParts[index] || 0) - (rightParts[index] || 0);
      if (difference) return difference;
    }
    return 0;
  };

  const productForVersion = (version) => compareVersions(version, '3.4.0') >= 0 ? 'OpenRiak KV' : 'Riak KV';

  const buildVersionCandidates = ({ currentPath, currentVersion, targetLanding, breadcrumbPaths = [], origin }) => {
    const marker = `/kv/${currentVersion}/`;
    const sourcePaths = [currentPath, ...breadcrumbPaths.slice().reverse()];
    const candidates = [];
    sourcePaths.forEach((sourcePath) => {
      const markerIndex = sourcePath.indexOf(marker);
      if (markerIndex < 0) return;
      const suffix = sourcePath.slice(markerIndex + marker.length);
      const candidate = new URL(suffix, new URL(targetLanding, origin)).href;
      if (!candidates.includes(candidate)) candidates.push(candidate);
    });
    const landing = new URL(targetLanding, origin).href;
    if (!candidates.includes(landing)) candidates.push(landing);
    return candidates;
  };

  const api = { compareVersions, productForVersion, buildVersionCandidates };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.OpenRiakVersionPicker = api;
  if (typeof document === 'undefined') return;

  const picker = document.querySelector('[data-version-picker]');
  if (!picker) return;

  const trigger = picker.querySelector('.version-picker__trigger');
  const panel = picker.querySelector('[data-version-panel]');
  const status = picker.querySelector('[data-version-status]');
  const currentVersion = picker.dataset.currentVersion;

  const positionPanel = () => {
    if (panel.hidden) return;
    const triggerBounds = trigger.getBoundingClientRect();
    const gutter = 12;
    const width = Math.min(610, window.innerWidth - (gutter * 2));
    const left = Math.max(gutter, Math.min(triggerBounds.left, window.innerWidth - width - gutter));
    panel.style.left = `${left}px`;
    panel.style.top = `${triggerBounds.bottom + 6}px`;
    panel.style.width = `${width}px`;
  };

  const setPanelOpen = (open) => {
    panel.hidden = !open;
    trigger.setAttribute('aria-expanded', String(open));
    picker.classList.toggle('is-open', open);
    if (open) positionPanel();
  };

  picker.querySelectorAll('[data-version-row]').forEach((row) => {
    const releases = row.querySelector('.version-series__releases');
    const options = [...row.querySelectorAll('[data-version-option]')]
      .sort((left, right) => compareVersions(right.dataset.version, left.dataset.version));
    const more = row.querySelector('[data-version-more]');
    options.forEach((option, index) => {
      option.classList.toggle('is-row-latest', index === 0);
      option.classList.toggle('version-option--overflow', index >= 3);
      option.hidden = index >= 3;
      releases.insertBefore(option, more);
    });
    if (!more) return;
    more.addEventListener('click', () => {
      const expanded = more.getAttribute('aria-expanded') !== 'true';
      more.setAttribute('aria-expanded', String(expanded));
      more.querySelector('[aria-hidden]')?.replaceChildren(document.createTextNode(expanded ? '‹' : '›'));
      const label = more.querySelector('.sr-only');
      if (label) label.textContent = `${expanded ? 'Show fewer' : 'Show more'} ${row.querySelector('.version-series__label').textContent.trim()} versions`;
      options.slice(3).forEach((option) => { option.hidden = !expanded; });
      positionPanel();
    });
  });

  picker.querySelectorAll('[data-version-product]').forEach((product) => {
    const rows = [...product.querySelectorAll('[data-version-row]')]
      .sort((left, right) => compareVersions(
        right.querySelector('.version-series__label').textContent.trim(),
        left.querySelector('.version-series__label').textContent.trim()
      ));
    rows.forEach((row) => product.append(row));
  });

  const pageExists = async (url) => {
    try {
      let response = await fetch(url, { method: 'HEAD', credentials: 'same-origin' });
      if (response.status === 405) response = await fetch(url, { credentials: 'same-origin' });
      return response.ok;
    } catch {
      return false;
    }
  };

  const switchVersion = async (option) => {
    const targetVersion = option.dataset.version;
    const targetLanding = option.dataset.versionUrl;
    if (!targetLanding || targetVersion === currentVersion) {
      setPanelOpen(false);
      return;
    }

    picker.classList.add('is-loading');
    status.textContent = `Finding this page in ${productForVersion(targetVersion)} ${targetVersion}…`;
    const breadcrumbPaths = [...document.querySelectorAll('.breadcrumbs a')]
      .map((link) => new URL(link.href, window.location.href).pathname);
    const candidates = buildVersionCandidates({
      currentPath: window.location.pathname,
      currentVersion,
      targetLanding,
      breadcrumbPaths,
      origin: window.location.origin
    });

    for (let index = 0; index < candidates.length; index += 1) {
      if (await pageExists(candidates[index])) {
        const exactPage = index === 0;
        const destination = new URL(candidates[index]);
        if (exactPage) {
          destination.search = window.location.search;
          destination.hash = window.location.hash;
        }
        window.location.assign(destination.href);
        return;
      }
    }

    window.location.assign(new URL(targetLanding, window.location.origin).href);
  };

  trigger.addEventListener('click', () => setPanelOpen(panel.hidden));
  picker.querySelectorAll('[data-version-option]:not(:disabled)').forEach((option) => {
    option.addEventListener('click', () => switchVersion(option));
  });
  document.addEventListener('click', (event) => {
    if (!picker.contains(event.target)) setPanelOpen(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !panel.hidden) {
      setPanelOpen(false);
      trigger.focus();
    }
  });
  window.addEventListener('resize', positionPanel);
})();
