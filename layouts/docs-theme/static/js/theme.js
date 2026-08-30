(() => {
  'use strict';
  const key = 'openriak-docs-theme';
  const picker = document.querySelector('[data-theme-picker]');
  const trigger = picker?.querySelector('.theme-trigger');
  const panel = picker?.querySelector('[data-theme-panel]');
  const triggerIcon = picker?.querySelector('[data-theme-trigger-icon]');
  const triggerLabel = picker?.querySelector('[data-theme-trigger-label]');
  const options = [...(picker?.querySelectorAll('[data-theme-value]') || [])];
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  const stored = () => {
    try {
      const value = window.localStorage.getItem(key) || 'system';
      return ['system', 'dark', 'light'].includes(value) ? value : 'system';
    } catch { return 'system'; }
  };
  const apply = (value) => {
    document.documentElement.dataset.theme = value === 'dark' || (value === 'system' && media.matches) ? 'dark' : 'light';
    const selected = options.find((option) => option.dataset.themeValue === value) || options[0];
    options.forEach((option) => {
      const active = option === selected;
      option.classList.toggle('is-active', active);
      option.setAttribute('aria-selected', String(active));
    });
    if (selected && triggerIcon && triggerLabel) {
      triggerIcon.src = selected.dataset.themeIcon;
      triggerLabel.textContent = selected.querySelector('strong')?.textContent || 'Default';
    }
  };
  const close = (returnFocus = false) => {
    if (!panel || !trigger) return;
    const wasOpen = !panel.hidden;
    panel.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
    if (returnFocus && wasOpen) trigger.focus();
  };
  apply(stored());
  trigger?.addEventListener('click', () => {
    panel.hidden = !panel.hidden;
    trigger.setAttribute('aria-expanded', String(!panel.hidden));
  });
  options.forEach((option) => option.addEventListener('click', () => {
    const value = option.dataset.themeValue;
    try { window.localStorage.setItem(key, value); } catch {}
    apply(value);
    close(true);
  }));
  document.addEventListener('click', (event) => { if (picker && !picker.contains(event.target)) close(); });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') close(true); });
  media.addEventListener?.('change', () => { if (stored() === 'system') apply('system'); });
})();