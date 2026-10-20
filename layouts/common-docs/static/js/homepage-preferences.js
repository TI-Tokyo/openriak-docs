(() => {
  'use strict';
  const node = document.getElementById('homepage-projects');
  if (!node || !window.OpenRiakSettings) return;
  const products = JSON.parse(node.textContent);
  const refresh = () => products.forEach(product => {
    const link = document.querySelector(`[data-home-project="${product.id}"]`);
    if (!link) return;
    const preferred = window.OpenRiakSettings.read(`openriak-docs-version:${product.id}`);
    const version = product.versions.some(version => version.version === preferred) ? preferred : 'latest';
    link.href = `${product.base}${version}/`;
    const heading = document.querySelector(`[data-home-project-heading="${product.id}"]`);
    if (heading) heading.href = link.href;
    const latest = document.querySelector(`[data-home-project-latest="${product.id}"]`);
    if (latest) latest.hidden = version === 'latest';
    const latestVersion = product.versions.map(item => item.version).filter(version => !version.includes('-'))
      .sort((a, b) => b.localeCompare(a, undefined, { numeric: true }))[0] || product.versions[0]?.version;
    const latestLabel = `Open Latest (${latestVersion}) →`;
    if (latest) latest.textContent = latestLabel;
    link.querySelector('[data-home-project-action]').textContent = version === 'latest' ? latestLabel : `Open ${version} →`;
  });
  refresh();
  window.addEventListener('storage', refresh);
  window.addEventListener('pageshow', refresh);
})();
