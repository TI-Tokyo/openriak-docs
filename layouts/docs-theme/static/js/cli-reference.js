(() => {
  'use strict';
  document.querySelectorAll('[data-cli-index]').forEach(index => {
    const input = index.querySelector('[data-cli-search]');
    const rows = [...index.querySelectorAll('[data-cli-row]')];
    const filters = [...index.querySelectorAll('[data-cli-tag-filter]')];
    const tags = new Map(rows.map(row => [row, JSON.parse(row.dataset.cliTags || '{}')]));
    const apply = () => {
      const words = input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      let visible = 0;
      rows.forEach(row => {
        const rowTags = tags.get(row);
        const text = row.dataset.cliSearchText + ' ' + Object.entries(rowTags).flatMap(([category, values]) => values.map(value => `${category}: ${value}`)).join(' ');
        row.hidden = !words.every(word => text.includes(word)) || !filters.every(filter => !filter.value || (rowTags[filter.dataset.cliTagFilter] || []).includes(filter.value));
        if (!row.hidden) visible++;
      });
      index.querySelectorAll('[data-cli-group]').forEach(group => {
        group.hidden = [...group.querySelectorAll('[data-cli-row]')].every(row => row.hidden);
      });
      index.querySelector('[data-cli-count]').textContent = `${visible} of ${rows.length} command topics`;
      index.querySelector('[data-cli-empty]').hidden = visible !== 0;
    };
    input.addEventListener('input', apply);
    filters.forEach(filter => filter.addEventListener('change', apply));
    index.querySelector('[data-cli-reset]')?.addEventListener('click', () => {
      input.value = '';
      filters.forEach(filter => { filter.value = ''; });
      apply();
    });
    apply();
  });
})();
