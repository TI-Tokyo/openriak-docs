(() => {
  'use strict';
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

  const navToggle = document.querySelector('[data-nav-toggle]');
  const scrim = document.querySelector('[data-nav-scrim]');
  const setNav = (open) => {
    document.body.classList.toggle('nav-open', open);
    navToggle?.setAttribute('aria-expanded', String(open));
    if (scrim) scrim.hidden = !open;
  };
  navToggle?.addEventListener('click', () => setNav(!document.body.classList.contains('nav-open')));
  scrim?.addEventListener('click', () => setNav(false));

  const sidebar = document.querySelector('#docs-sidebar');
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
    document.documentElement.classList.toggle('sidebar-collapsed', active);
    sidebarCollapse?.setAttribute('aria-expanded', String(!active));
    sidebarRail?.setAttribute('aria-hidden', String(!active));
    sidebarExpanded?.setAttribute('aria-hidden', String(active));
    if (active) closeSidebarFlyouts();
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
    sidebarCollapse?.focus();
  });
  sidebar?.querySelector('[data-sidebar-version]')?.addEventListener('click', () => expandFor('[data-version-picker] .picker-trigger'));
  sidebar?.querySelector('[data-sidebar-os]')?.addEventListener('click', () => expandFor('[data-os-trigger]'));
  sidebar?.querySelector('[data-sidebar-search-button]')?.addEventListener('click', () => expandFor('[data-search-input]', 'focus'));
  sidebar?.querySelector('[data-sidebar-tree]')?.addEventListener('click', () => expandFor('.sidebar-page-tree', 'focus'));
  desktopSidebar.addEventListener('change', () => setSidebarCollapsed(readSidebarPreference(), false));

  document.querySelectorAll('[data-nav-tree-toggle]').forEach((toggle) => {
    const children = document.getElementById(toggle.getAttribute('aria-controls'));
    if (!children) return;
    toggle.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      const expanded = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(expanded));
      const label = toggle.closest('.nav-tree-row')?.querySelector('a')?.textContent || 'section';
      toggle.setAttribute('aria-label', `${expanded ? 'Collapse' : 'Expand'} ${label}`);
      children.hidden = !expanded;
    });
  });
})();
