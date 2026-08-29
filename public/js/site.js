(() => {
  'use strict';

  const body = document.body;
  const toggle = document.querySelector('.nav-toggle');
  const closeButton = document.querySelector('[data-sidebar-close]');

  const setNavigation = (open) => {
    body.classList.toggle('nav-open', open);
    toggle?.setAttribute('aria-expanded', String(open));
  };

  toggle?.addEventListener('click', () => setNavigation(!body.classList.contains('nav-open')));
  closeButton?.addEventListener('click', () => setNavigation(false));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') setNavigation(false);
  });

  document.querySelector('[data-version-select]')?.addEventListener('change', (event) => {
    window.location.assign(event.target.value);
  });

  document.querySelectorAll('.doc-body pre').forEach((pre) => {
    const button = document.createElement('button');
    button.className = 'copy-code';
    button.type = 'button';
    button.textContent = 'Copy';
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(pre.innerText.replace(/^Copy\s*/, ''));
        button.textContent = 'Copied';
        window.setTimeout(() => { button.textContent = 'Copy'; }, 1500);
      } catch {
        button.textContent = 'Select and copy';
      }
    });
    pre.append(button);
  });

  const searchForm = document.querySelector('[data-search]');
  const searchInput = searchForm?.querySelector('[data-search-input]');
  const searchResults = searchForm?.querySelector('[data-search-results]');
  let searchIndex;

  const normalize = (value) => String(value || '').toLocaleLowerCase();
  const loadSearchIndex = async () => {
    if (searchIndex) return searchIndex;
    const response = await fetch(searchForm.dataset.indexUrl, { credentials: 'same-origin' });
    if (!response.ok) throw new Error(`Search index request failed: ${response.status}`);
    searchIndex = await response.json();
    return searchIndex;
  };

  const renderSearchResults = (items, query) => {
    searchResults.replaceChildren();
    if (!items.length) {
      const empty = document.createElement('p');
      empty.className = 'search-results__empty';
      empty.textContent = `No results for “${query}”.`;
      searchResults.append(empty);
    } else {
      items.forEach((item) => {
        const link = document.createElement('a');
        const title = document.createElement('strong');
        const detail = document.createElement('span');
        link.href = item.url;
        title.textContent = item.title;
        detail.textContent = [item.diataxis, item.version].filter(Boolean).join(' · ');
        link.append(title, detail);
        searchResults.append(link);
      });
    }
    searchResults.hidden = false;
  };

  let searchTimer;
  searchInput?.addEventListener('input', () => {
    window.clearTimeout(searchTimer);
    const query = searchInput.value.trim();
    if (query.length < 2) {
      searchResults.hidden = true;
      return;
    }
    searchTimer = window.setTimeout(async () => {
      try {
        const terms = normalize(query).split(/\s+/).filter(Boolean);
        const version = searchForm.dataset.version;
        const index = await loadSearchIndex();
        const matches = index
          .filter((item) => !version || item.version === version)
          .map((item) => {
            const title = normalize(item.title);
            const haystack = `${title} ${normalize(item.description)} ${normalize(item.content)}`;
            if (!terms.every((term) => haystack.includes(term))) return null;
            const score = terms.reduce((total, term) => total + (title.includes(term) ? 10 : 1), 0);
            return { item, score };
          })
          .filter(Boolean)
          .sort((a, b) => b.score - a.score || a.item.title.localeCompare(b.item.title))
          .slice(0, 12)
          .map(({ item }) => item);
        renderSearchResults(matches, query);
      } catch {
        renderSearchResults([], query);
      }
    }, 180);
  });

  document.addEventListener('click', (event) => {
    if (searchForm && !searchForm.contains(event.target)) searchResults.hidden = true;
  });

  // Modern, dependency-free port of the capacity calculator used by the old site.
  const calculator = document.querySelector('.calculator');
  if (calculator) {
    const defaults = {
      n_total_keys: 183915891,
      n_bucket_size: 10,
      n_key_size: 36,
      n_record_size: 36,
      n_ram: 16,
      n_nval: 3
    };
    const info = document.querySelector('#node_info');
    const recommendation = document.querySelector('#recommend');
    const descriptions = {
      n_total_keys: 'How many keys will be stored in your cluster?',
      n_bucket_size: 'How long will the average bucket name be in bytes?',
      n_key_size: 'How long will the average key be in bytes?',
      n_record_size: 'How much data will be stored on average per bucket and key pair?',
      n_ram: 'How much physical RAM on each server will be dedicated to the storage engine?',
      n_nval: 'How many replicas of each item will the cluster retain?'
    };
    const value = (id) => Math.abs(Number.parseFloat(document.querySelector(`#${id}`)?.value || '0')) || 0;
    const formatBytes = (bytes) => {
      if (!Number.isFinite(bytes) || bytes <= 0) return '0 bytes';
      const units = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB'];
      const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
      const amount = bytes / (1024 ** index);
      return `${index === 0 ? amount.toFixed(0) : amount.toFixed(1)} ${units[index]}`;
    };
    const abbreviate = (number) => new Intl.NumberFormat('en', { notation: 'compact', maximumFractionDigits: 1 }).format(number);

    const update = () => {
      const entries = value('n_total_keys');
      const bucket = value('n_bucket_size');
      const key = value('n_key_size');
      const record = value('n_record_size');
      const ram = value('n_ram') * (1024 ** 3);
      const nVal = value('n_nval');
      const values = { n_total_keys: entries, n_bucket_size: bucket, n_key_size: key, n_record_size: record, n_ram: value('n_ram'), n_nval: nVal };

      Object.entries(values).forEach(([id, number]) => {
        const error = document.querySelector(`#${id}_error`);
        if (error) error.textContent = Number.isInteger(number) && number >= 0 ? '' : 'Must be a non-negative integer';
      });
      if (!recommendation) return;
      if (![entries, bucket, key, record, ram, nVal].every((number) => number > 0)) {
        recommendation.textContent = 'Enter a positive value in every field to calculate an estimate.';
        return;
      }

      const pointerBytes = 8;
      const nullBucketKeyPairBytes = 44.5 + 13 + pointerBytes;
      const keyDirectory = (key + bucket + nullBucketKeyPairBytes) * entries * nVal;
      const nodes = Math.max(nVal + 2, Math.ceil(keyDirectory / ram));
      const storage = (14 + (13 + bucket + key) + (91 + bucket + key + record) + (18 + (13 + bucket + key))) * entries * nVal;
      recommendation.innerHTML = `<p>For approximately ${abbreviate(entries)} bucket/key pairs with N=${nVal}, the historical Bitcask model estimates at least:</p><ul><li><strong>${nodes} nodes</strong></li><li><strong>${formatBytes(keyDirectory / nodes)}</strong> RAM per node (${formatBytes(keyDirectory)} total)</li><li><strong>${formatBytes(storage / nodes)}</strong> storage per node (${formatBytes(storage)} total)</li></ul><p><small>This is a planning estimate, not a capacity guarantee; validate it with representative data and load tests.</small></p>`;
    };

    Object.entries(defaults).forEach(([id, defaultValue]) => {
      const input = document.querySelector(`#${id}`);
      if (!input) return;
      if (!input.value) input.value = String(defaultValue);
      input.addEventListener('input', update);
      input.addEventListener('focus', () => { if (info) info.textContent = descriptions[id]; });
    });
    update();
  }
})();

