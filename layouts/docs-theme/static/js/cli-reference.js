(() => {
  'use strict';
  document.querySelectorAll('[data-cli-index]').forEach(index => {
    const input = index.querySelector('[data-cli-search]');
    const rows = [...index.querySelectorAll('[data-cli-row]')];
    const apply = () => {
      const words = input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      let visible = 0;
      rows.forEach(row => {
        row.hidden = !words.every(word => row.dataset.cliSearchText.includes(word));
        if (!row.hidden) visible++;
      });
      index.querySelectorAll('[data-cli-group]').forEach(group => {
        group.hidden = [...group.querySelectorAll('[data-cli-row]')].every(row => row.hidden);
      });
      index.querySelector('[data-cli-count]').textContent = `${visible} of ${rows.length} command topics`;
      index.querySelector('[data-cli-empty]').hidden = visible !== 0;
    };
    input.addEventListener('input', apply);
    apply();
  });
})();
