(() => {
  'use strict';
  const skipLink = document.querySelector('.skip-link');
  document.addEventListener('keydown', (event) => {
    if (!['Home', 'End'].includes(event.key) || !(event.ctrlKey || event.metaKey) || event.altKey || event.shiftKey) return;
    const target = event.target;
    if (target instanceof HTMLElement
      && (target.matches('input, textarea') || target.isContentEditable)) return;
    // Scroll the document, even when a nested scroll area or the skip link has focus.
    event.preventDefault();
    if (document.activeElement === skipLink) skipLink.blur();
    const top = event.key === 'Home' ? 0 : document.scrollingElement.scrollHeight;
    window.scrollTo({ top, left: window.scrollX, behavior: 'instant' });
  });

  const siteSection = document.querySelector('[data-site-section-picker]');
  const siteSectionTrigger = siteSection?.querySelector('.site-section-trigger');
  const siteSectionPanel = siteSection?.querySelector('[data-site-section-panel]');
  const closeSiteSections = () => {
    if (!siteSectionPanel || !siteSectionTrigger) return;
    siteSectionPanel.hidden = true;
    siteSectionTrigger.setAttribute('aria-expanded', 'false');
  };
  siteSectionTrigger?.addEventListener('click', () => {
    siteSectionPanel.hidden = !siteSectionPanel.hidden;
    siteSectionTrigger.setAttribute('aria-expanded', String(!siteSectionPanel.hidden));
  });
  document.addEventListener('click', (event) => { if (siteSection && !siteSection.contains(event.target)) closeSiteSections(); });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeSiteSections(); });
  document.addEventListener('openriak:modal-open', closeSiteSections);

  const navToggle = document.querySelector('[data-nav-toggle]');
  const scrim = document.querySelector('[data-nav-scrim]');
  const sidebar = document.querySelector('#docs-sidebar');
  const sidebarScope = sidebar?.querySelector('[data-index-url]')?.dataset.indexUrl;
  const sidebarPositionKey = sidebarScope ? `openriak-sidebar-position:${sidebarScope}` : null;
  let sidebarPosition = { top: 0, branches: {} };
  let revealCurrentPage = false;
  let sidebarTreeReady = false;
  const { product, version } = document.body.dataset;
  if (product && version) {
    try {
      const key = `openriak-sidebar-version:${product}`;
      const previousVersion = window.sessionStorage.getItem(key);
      revealCurrentPage = Boolean(previousVersion && previousVersion !== version);
      window.sessionStorage.setItem(key, version);
    } catch (_) {}
  }
  try {
    const saved = sidebarPositionKey ? JSON.parse(window.sessionStorage.getItem(sidebarPositionKey) || 'null') : null;
    if (saved && Number.isFinite(saved.top) && saved.top >= 0
      && saved.branches && typeof saved.branches === 'object' && !Array.isArray(saved.branches)) {
      sidebarPosition = saved;
    }
  } catch (_) {}
  const sidebarIsCollapsed = () => window.matchMedia('(min-width: 761px)').matches
    && document.documentElement.classList.contains('sidebar-collapsed');
  const saveSidebarPosition = () => {
    if (!sidebar || !sidebarPositionKey || sidebarIsCollapsed()) return;
    sidebarPosition.top = sidebar.scrollTop;
    try { window.sessionStorage.setItem(sidebarPositionKey, JSON.stringify(sidebarPosition)); } catch (_) {}
  };
  const restoreSidebarPosition = () => {
    if (!sidebar || sidebarIsCollapsed()) return;
    sidebar.scrollTop = sidebarPosition.top;
    if (!sidebarTreeReady || !revealCurrentPage) return;
    const current = sidebar.querySelector('.sidebar-page-tree [aria-current="page"]');
    if (current) {
      const bounds = sidebar.getBoundingClientRect();
      const item = current.getBoundingClientRect();
      const top = bounds.top + sidebar.clientTop;
      const bottom = top + sidebar.clientHeight;
      // Adjust only the menu, leaving the document and its anchor unchanged.
      if (item.top < top) sidebar.scrollTop += item.top - top;
      else if (item.bottom > bottom) sidebar.scrollTop += item.bottom - bottom;
    }
    revealCurrentPage = false;
    saveSidebarPosition();
  };
  const mobileSidebar = window.matchMedia('(max-width: 760px)');
  const focusableSelector = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
  let restoreNavInert = () => {};
  let restoreSidebarRole = null;
  const visibleFocusable = (root) => [...(root?.querySelectorAll(focusableSelector) || [])]
    .filter((element) => !element.hidden && element.getClientRects().length > 0);
  const makeInert = (elements) => {
    const changed = [...new Set(elements)].filter((element) => element instanceof HTMLElement && !element.inert);
    changed.forEach((element) => { element.inert = true; });
    return () => changed.forEach((element) => { element.inert = false; });
  };
  const navBackground = () => {
    if (!sidebar) return [];
    const header = document.querySelector('.global-header');
    const shell = sidebar.parentElement;
    return [
      ...[...(document.body.children || [])].filter((element) => element !== header && element !== shell && element.tagName !== 'SCRIPT'),
      ...[...(header?.children || [])].filter((element) => element !== navToggle),
      ...[...(shell?.children || [])].filter((element) => element !== sidebar && element !== scrim),
    ];
  };
  const setNav = (open, returnFocus = false) => {
    open = Boolean(open && mobileSidebar.matches && sidebar);
    const wasOpen = document.body.classList.contains('nav-open');
    document.body.classList.toggle('nav-open', open);
    navToggle?.setAttribute('aria-expanded', String(open));
    if (scrim) scrim.hidden = !open;
    if (open && !wasOpen) {
      document.dispatchEvent(new CustomEvent('openriak:modal-open', { detail: { source: 'navigation' } }));
      restoreSidebarRole = {
        role: sidebar.getAttribute('role'),
        modal: sidebar.getAttribute('aria-modal'),
        tabindex: sidebar.getAttribute('tabindex'),
      };
      sidebar.setAttribute('role', 'dialog');
      sidebar.setAttribute('aria-modal', 'true');
      sidebar.setAttribute('tabindex', '-1');
      restoreNavInert = makeInert(navBackground());
      window.requestAnimationFrame(() => {
        const bounds = sidebar.getBoundingClientRect();
        const target = visibleFocusable(sidebar).find(element => {
          const rect = element.getBoundingClientRect();
          return rect.top >= bounds.top && rect.bottom <= bounds.bottom;
        });
        (target || sidebar).focus({ preventScroll: true });
      });
    } else if (!open && wasOpen) {
      restoreNavInert();
      restoreNavInert = () => {};
      if (restoreSidebarRole) {
        ['role', 'aria-modal', 'tabindex'].forEach((attribute) => {
          const value = restoreSidebarRole[attribute === 'aria-modal' ? 'modal' : attribute];
          if (value === null) sidebar.removeAttribute(attribute);
          else sidebar.setAttribute(attribute, value);
        });
        restoreSidebarRole = null;
      }
      if (returnFocus) navToggle?.focus();
    }
  };
  navToggle?.addEventListener('click', () => {
    const wasOpen = document.body.classList.contains('nav-open');
    setNav(!wasOpen, wasOpen);
  });
  scrim?.addEventListener('click', () => setNav(false, true));
  document.addEventListener('openriak:modal-open', (event) => {
    if (event.detail?.source !== 'navigation') setNav(false);
  });
  document.addEventListener('focusin', (event) => {
    if (!document.body.classList.contains('nav-open') || sidebar.contains(event.target)) return;
    (visibleFocusable(sidebar)[0] || sidebar).focus();
  });
  document.addEventListener('keydown', (event) => {
    if (!document.body.classList.contains('nav-open')) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      setNav(false, true);
      return;
    }
    if (event.key !== 'Tab') return;
    const focusable = visibleFocusable(sidebar);
    if (!focusable.length) {
      event.preventDefault();
      sidebar.focus();
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
  mobileSidebar.addEventListener('change', () => setNav(false));

  const sidebarCollapse = sidebar?.querySelector('[data-sidebar-collapse]');
  const sidebarRail = sidebar?.querySelector('[data-sidebar-rail]');
  const sidebarExpanded = sidebar?.querySelector('[data-sidebar-expanded]');
  const sidebarExpand = sidebar?.querySelector('[data-sidebar-expand]');
  const desktopSidebar = window.matchMedia('(min-width: 761px)');
  const sidebarStorageKey = 'openriak-docs-sidebar-collapsed';
  const readSidebarPreference = () => {
    try { return window.localStorage.getItem(sidebarStorageKey) === 'true'; } catch (_) { return false; }
  };
  const closeSidebarFlyouts = () => {
    sidebar?.querySelectorAll('.picker-panel, .search-results').forEach((panel) => { panel.hidden = true; });
    sidebar?.querySelectorAll('.picker-trigger[aria-expanded="true"]').forEach((trigger) => trigger.setAttribute('aria-expanded', 'false'));
  };
  const setSidebarCollapsed = (collapsed, persist = true) => {
    const active = Boolean(collapsed && desktopSidebar.matches);
    if (active && persist) saveSidebarPosition();
    document.documentElement.classList.toggle('sidebar-collapsed', active);
    sidebarCollapse?.setAttribute('aria-expanded', String(!active));
    sidebarRail?.setAttribute('aria-hidden', String(!active));
    sidebarExpanded?.setAttribute('aria-hidden', String(active));
    if (active) closeSidebarFlyouts();
    else restoreSidebarPosition();
    if (persist) {
      try { window.localStorage.setItem(sidebarStorageKey, String(Boolean(collapsed))); } catch (_) {}
    }
  };
  const expandFor = (selector, action = 'click') => {
    setSidebarCollapsed(false);
    window.requestAnimationFrame(() => {
      const target = sidebar?.querySelector(selector);
      if (!target) return;
      if (action === 'click') target.click();
      else {
        target.focus();
        target.scrollIntoView({ block: 'nearest' });
      }
    });
  };
  setSidebarCollapsed(readSidebarPreference(), false);
  sidebarCollapse?.addEventListener('click', () => {
    setSidebarCollapsed(true);
    sidebarExpand?.focus();
  });
  sidebarExpand?.addEventListener('click', () => {
    setSidebarCollapsed(false);
    sidebarCollapse?.focus({ preventScroll: true });
  });
  sidebar?.querySelector('[data-sidebar-version]')?.addEventListener('click', () => expandFor('[data-version-picker] .picker-trigger'));
  sidebar?.querySelector('[data-sidebar-os]')?.addEventListener('click', () => expandFor('[data-os-trigger]'));
  sidebar?.querySelector('[data-sidebar-search-button]')?.addEventListener('click', () => expandFor('[data-search-input]', 'focus'));
  sidebar?.querySelector('[data-sidebar-tree]')?.addEventListener('click', () => expandFor('.sidebar-page-tree', 'focus'));
  desktopSidebar.addEventListener('change', () => setSidebarCollapsed(readSidebarPreference(), false));
  document.addEventListener('keydown', (event) => {
    const target = event.target;
    const isTyping = target instanceof HTMLElement
      && (target.matches('input, textarea, select') || target.isContentEditable);
    const slashShortcut = event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey;
    const commandShortcut = event.key.toLowerCase() === 'k'
      && (event.ctrlKey || event.metaKey) && !event.altKey && !event.shiftKey;
    const searchInput = sidebar?.querySelector('[data-search-input]');
    if (isTyping || !searchInput || (!slashShortcut && !commandShortcut)) return;
    event.preventDefault();
    if (mobileSidebar.matches) setNav(true);
    else setSidebarCollapsed(false);
    window.requestAnimationFrame(() => {
      searchInput.focus();
      searchInput.select();
      searchInput.scrollIntoView({ block: 'nearest' });
    });
  });

  document.querySelectorAll('[data-nav-tree-toggle]').forEach((toggle) => {
    const children = document.getElementById(toggle.getAttribute('aria-controls'));
    if (!children) return;
    const setExpanded = (expanded) => {
      toggle.setAttribute('aria-expanded', String(expanded));
      const label = toggle.closest('.nav-tree-row')?.querySelector('a')?.textContent || 'section';
      toggle.setAttribute('aria-label', `${expanded ? 'Collapse' : 'Expand'} ${label}`);
      children.hidden = !expanded;
      sidebarPosition.branches[children.id] = expanded;
    };
    // Keep previous branches open, and reveal the current page's ancestors.
    setExpanded(toggle.getAttribute('aria-expanded') === 'true'
      || sidebarPosition.branches[children.id] === true);
    toggle.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      const expanded = toggle.getAttribute('aria-expanded') !== 'true';
      setExpanded(expanded);
      saveSidebarPosition();
    });
  });
  sidebarTreeReady = true;
  restoreSidebarPosition();
  sidebar?.addEventListener('scroll', saveSidebarPosition, { passive: true });
  // Capture the latest offset even if navigation occurs before a scroll event.
  sidebar?.addEventListener('click', saveSidebarPosition, { capture: true });
  window.addEventListener('pagehide', saveSidebarPosition);
  window.addEventListener('pageshow', restoreSidebarPosition);
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') saveSidebarPosition();
  });
})();
