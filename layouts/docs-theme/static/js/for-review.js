(() => {
  'use strict';
  const root = document.querySelector('[data-for-review]');
  if (!root) return;
  const controls = [...root.querySelectorAll('[data-review-filter]')];
  const rows = [...root.querySelectorAll('[data-review-values]')].map(element => ({
    element, values: JSON.parse(element.dataset.reviewValues)
  }));
  const groups = [...root.querySelectorAll('[data-review-group]')].map(element => ({
    element, rows: [...element.querySelectorAll('[data-review-values]')]
  }));
  const storageKey = `openriak-docs-review-filters:${root.dataset.reviewProduct}`;

  controls.forEach(control => {
    const values = new Set();
    rows.forEach(row => {
      const items = row.values[control.dataset.reviewFilter];
      (items.length ? items : [null]).forEach(value => values.add(value));
    });
    [...values].sort((a, b) => (a === null ? 1 : b === null ? -1 : a.localeCompare(b))).forEach(value => {
      const option = document.createElement('option');
      // Encode values to distinguish All, an empty value, and missing metadata.
      option.value = JSON.stringify(value);
      option.textContent = value === null ? 'Not set' : value === '' ? '(empty)' : value;
      control.append(option);
    });
  });

  const apply = () => {
    const filters = controls.filter(control => control.value !== '').map(control => ({
      key: control.dataset.reviewFilter, value: JSON.parse(control.value)
    }));
    let visible = 0;
    rows.forEach(row => {
      const matches = filters.every(filter => filter.value === null
        ? row.values[filter.key].length === 0
        : row.values[filter.key].includes(filter.value));
      row.element.hidden = !matches;
      if (matches) visible += 1;
    });
    groups.forEach(group => { group.element.hidden = group.rows.every(row => row.hidden); });
    root.querySelector('[data-review-count]').textContent = `${visible} of ${rows.length} pages`;
    root.querySelector('[data-review-empty]').hidden = visible !== 0;
  };
  const restore = () => {
    let saved = {};
    try {
      const value = JSON.parse(localStorage.getItem(storageKey) || '{}');
      if (value && typeof value === 'object' && !Array.isArray(value)) saved = value;
    } catch { /* Use All when storage is unavailable or invalid. */ }
    controls.forEach(control => {
      const value = saved[control.dataset.reviewFilter];
      control.value = [...control.options].some(option => option.value === value) ? value : '';
    });
    apply();
  };
  const save = () => {
    const values = Object.fromEntries(controls.filter(control => control.value !== '')
      .map(control => [control.dataset.reviewFilter, control.value]));
    try { localStorage.setItem(storageKey, JSON.stringify(values)); } catch { /* Filtering still works without storage. */ }
    apply();
  };
  controls.forEach(control => control.addEventListener('change', save));
  root.querySelector('[data-review-reset]').addEventListener('click', () => {
    controls.forEach(control => { control.value = ''; });
    save();
  });
  window.addEventListener('pageshow', event => { if (event.persisted) restore(); });
  window.addEventListener('storage', event => {
    if (event.key === storageKey || event.key === null) restore();
  });
  restore();
  root.querySelector('[data-review-filters]').hidden = false;
})();
