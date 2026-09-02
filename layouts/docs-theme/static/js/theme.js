(() => {
  'use strict';
  const key = 'openriak-docs-theme';
  const contentWidthKey = 'openriak-docs-content-width';
  const contentWidthDefault = '75';
  const contentWidths = ['50', '75', '90', '98'];
  const fontSizeKey = 'openriak-docs-font-size';
  const fontSizeDefault = '100';
  const fontSizes = ['100', '110', '125', '150', '200', '250'];
  const picker = document.querySelector('[data-theme-picker]');
  const trigger = picker?.querySelector('.theme-trigger');
  const panel = picker?.querySelector('[data-theme-panel]');
  const options = [...(picker?.querySelectorAll('[data-theme-value]') || [])];
  const contentWidthOptions = [...(picker?.querySelectorAll('[data-content-width-value]') || [])];
  const fontSizeOptions = [...(picker?.querySelectorAll('[data-font-size-value]') || [])];
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  const mobileAppearance = window.matchMedia('(max-width: 760px)');
  const focusableSelector = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
  let currentTheme = 'system';
  let currentContentWidth = contentWidthDefault;
  let currentFontSize = fontSizeDefault;
  let restoreAppearanceInert = () => {};
  const syncTriggerLabel = () => {
    if (!trigger) return;
    const themeLabel = { system: 'System theme', dark: 'Dark theme', light: 'Light theme' }[currentTheme] || 'System theme';
    trigger.setAttribute('aria-label', `Display preferences: ${themeLabel}, ${currentContentWidth}% width, ${currentFontSize}% text`);
  };
  const visibleFocusable = () => [...(panel?.querySelectorAll(focusableSelector) || [])]
    .filter((element) => !element.hidden && element.getClientRects().length > 0);
  const makeInert = (elements) => {
    const changed = [...new Set(elements)].filter((element) => element instanceof HTMLElement && !element.inert);
    changed.forEach((element) => { element.inert = true; });
    return () => changed.forEach((element) => { element.inert = false; });
  };
  const appearanceBackground = () => {
    const header = document.querySelector('.global-header');
    const controls = picker?.parentElement;
    return [
      ...[...(document.body.children || [])].filter((element) => element !== header && element.tagName !== 'SCRIPT'),
      ...[...(header?.children || [])].filter((element) => element !== controls),
      ...[...(controls?.children || [])].filter((element) => element !== picker),
    ];
  };
  const syncHeaderHeight = () => {
    const root = document.documentElement;
    const header = document.querySelector('.global-header');
    if (!header) return;
    root.style.removeProperty('--site-header-height');
    root.style.setProperty('--site-header-height', `${Math.ceil(header.getBoundingClientRect().height)}px`);
  };
  const stored = () => {
    try {
      const value = window.localStorage.getItem(key) || 'system';
      return ['system', 'dark', 'light'].includes(value) ? value : 'system';
    } catch { return 'system'; }
  };
  const apply = (value) => {
    currentTheme = ['system', 'dark', 'light'].includes(value) ? value : 'system';
    document.documentElement.dataset.theme = value === 'dark' || (value === 'system' && media.matches) ? 'dark' : 'light';
    const selected = options.find((option) => option.dataset.themeValue === value) || options[0];
    options.forEach((option) => {
      const active = option === selected;
      option.classList.toggle('is-active', active);
      option.setAttribute('aria-pressed', String(active));
    });
    syncTriggerLabel();
  };
  const storedContentWidth = () => {
    try {
      const value = window.localStorage.getItem(contentWidthKey) || contentWidthDefault;
      return contentWidths.includes(value) ? value : contentWidthDefault;
    } catch { return contentWidthDefault; }
  };
  const applyContentWidth = (value) => {
    const selectedValue = contentWidths.includes(value) ? value : contentWidthDefault;
    currentContentWidth = selectedValue;
    document.documentElement.dataset.contentWidth = selectedValue;
    contentWidthOptions.forEach((option) => {
      const active = option.dataset.contentWidthValue === selectedValue;
      option.classList.toggle('is-active', active);
      option.setAttribute('aria-pressed', String(active));
    });
    syncTriggerLabel();
  };
  const storedFontSize = () => {
    try {
      const value = window.localStorage.getItem(fontSizeKey) || fontSizeDefault;
      return fontSizes.includes(value) ? value : fontSizeDefault;
    } catch { return fontSizeDefault; }
  };
  const applyFontSize = (value) => {
    const selectedValue = fontSizes.includes(value) ? value : fontSizeDefault;
    currentFontSize = selectedValue;
    document.documentElement.dataset.fontSize = selectedValue;
    fontSizeOptions.forEach((option) => {
      const active = option.dataset.fontSizeValue === selectedValue;
      option.classList.toggle('is-active', active);
      option.setAttribute('aria-pressed', String(active));
    });
    syncTriggerLabel();
    window.requestAnimationFrame(syncHeaderHeight);
  };
  const close = (returnFocus = false) => {
    if (!panel || !trigger) return;
    const wasOpen = !panel.hidden;
    panel.hidden = true;
    panel.setAttribute('role', 'region');
    panel.removeAttribute('aria-modal');
    document.body.classList.remove('appearance-open');
    restoreAppearanceInert();
    restoreAppearanceInert = () => {};
    trigger.setAttribute('aria-expanded', 'false');
    if (returnFocus && wasOpen) trigger.focus();
  };
  const open = () => {
    if (!panel || !trigger) return;
    document.dispatchEvent(new CustomEvent('openriak:modal-open', { detail: { source: 'appearance' } }));
    panel.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
    if (mobileAppearance.matches) {
      panel.setAttribute('role', 'dialog');
      panel.setAttribute('aria-modal', 'true');
      document.body.classList.add('appearance-open');
      restoreAppearanceInert = makeInert(appearanceBackground());
    } else {
      panel.setAttribute('role', 'region');
      panel.removeAttribute('aria-modal');
    }
    const selected = panel.querySelector('[aria-pressed="true"]');
    window.requestAnimationFrame(() => (selected || visibleFocusable()[0] || panel).focus());
  };
  apply(stored());
  applyContentWidth(storedContentWidth());
  applyFontSize(storedFontSize());
  trigger?.addEventListener('click', () => {
    if (panel.hidden) open();
    else close(true);
  });
  options.forEach((option) => option.addEventListener('click', () => {
    const value = option.dataset.themeValue;
    try { window.localStorage.setItem(key, value); } catch {}
    apply(value);
    close(true);
  }));
  contentWidthOptions.forEach((option) => option.addEventListener('click', () => {
    const value = option.dataset.contentWidthValue;
    try { window.localStorage.setItem(contentWidthKey, value); } catch {}
    applyContentWidth(value);
    close(true);
  }));
  fontSizeOptions.forEach((option) => option.addEventListener('click', () => {
    const value = option.dataset.fontSizeValue;
    try { window.localStorage.setItem(fontSizeKey, value); } catch {}
    applyFontSize(value);
    close(true);
  }));
  document.addEventListener('click', (event) => { if (picker && !picker.contains(event.target)) close(); });
  document.addEventListener('openriak:modal-open', (event) => {
    if (event.detail?.source !== 'appearance') close();
  });
  document.addEventListener('focusin', (event) => {
    if (!panel || panel.hidden || picker.contains(event.target)) return;
    if (mobileAppearance.matches) (visibleFocusable()[0] || panel).focus();
    else close();
  });
  document.addEventListener('keydown', (event) => {
    if (!panel || panel.hidden) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      close(true);
      return;
    }
    if (event.key !== 'Tab' || !mobileAppearance.matches) return;
    const focusable = visibleFocusable();
    if (!focusable.length) {
      event.preventDefault();
      panel.focus();
      return;
    }
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
  mobileAppearance.addEventListener('change', () => close());
  window.addEventListener('resize', () => window.requestAnimationFrame(syncHeaderHeight));
  media.addEventListener?.('change', () => { if (stored() === 'system') apply('system'); });
})();
