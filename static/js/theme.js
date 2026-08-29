(() => {
  'use strict';

  const storageKey = 'openriak-docs-theme';
  const root = document.documentElement;
  const selector = document.querySelector('[data-theme-select]');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  const validPreferences = new Set(['system', 'light', 'dark']);

  const storedPreference = () => {
    try {
      const value = localStorage.getItem(storageKey);
      return validPreferences.has(value) ? value : 'system';
    } catch {
      return 'system';
    }
  };

  const applyTheme = (preference, persist = false) => {
    const selected = validPreferences.has(preference) ? preference : 'system';
    const resolved = selected === 'system' ? (systemTheme.matches ? 'dark' : 'light') : selected;
    root.dataset.themePreference = selected;
    root.dataset.theme = resolved;
    if (selector) selector.value = selected;
    if (persist) {
      try {
        if (selected === 'system') localStorage.removeItem(storageKey);
        else localStorage.setItem(storageKey, selected);
      } catch {}
    }
  };

  applyTheme(root.dataset.themePreference || storedPreference());

  selector?.addEventListener('change', () => applyTheme(selector.value, true));
  systemTheme.addEventListener('change', () => {
    if (root.dataset.themePreference === 'system') applyTheme('system');
  });
  window.addEventListener('storage', (event) => {
    if (event.key === storageKey) applyTheme(storedPreference());
  });
})();
