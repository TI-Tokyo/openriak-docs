(() => {
  'use strict';
  const root = document.querySelector('[data-sidebar-search]');
  const input = root?.querySelector('[data-search-input]');
  const results = root?.querySelector('[data-search-results]');
  if (!root || !input || !results) return;
  root.dataset.sharedSearchReady = 'true';
  let indexPromise;
  let cachedQuery = '';
  const hide = () => { results.hidden = true; };
  const resultUrl = (value, query) => {
    const url = new URL(value, window.location.href);
    const os = new URL(window.location.href).searchParams.get('os');
    if (os && url.origin === window.location.origin) url.searchParams.set('os', os);
    url.searchParams.set('highlight', query);
    return url.href;
  };
  const loadIndex = () => {
    if (!indexPromise) indexPromise = fetch(new URL(root.dataset.indexUrl, window.location.href)).then((response) => {
      if (!response.ok) throw new Error(`Search index returned ${response.status}`);
      return response.json();
    });
    return indexPromise;
  };
  const score = (page, query) => {
    const title = (page.title || '').toLowerCase();
    const description = (page.description || '').toLowerCase();
    const content = (page.content || '').toLowerCase();
    return (title.includes(query) ? 1000 : 0)
      + (description.includes(query) ? 100 : 0)
      + (content.includes(query) ? Math.min(content.split(query).length - 1, 50) : 0);
  };
  const render = (pages, query) => {
    results.replaceChildren();
    pages.forEach((page) => {
      const link = document.createElement('a');
      const title = document.createElement('strong');
      const description = document.createElement('span');
      link.href = resultUrl(page.url, query);
      title.textContent = page.title;
      description.textContent = page.description || '';
      link.append(title, description);
      results.append(link);
    });
    if (!pages.length) results.textContent = root.dataset.emptyMessage || 'No results.';
    results.hidden = false;
  };
  input.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    event.preventDefault();
    event.stopPropagation();
    input.value = '';
    cachedQuery = '';
    results.replaceChildren();
    hide();
  });
  input.addEventListener('click', () => {
    if (input.value.trim().toLowerCase() === cachedQuery && results.childNodes.length) results.hidden = false;
  });
  document.addEventListener('click', (event) => { if (!root.contains(event.target)) hide(); });
  input.addEventListener('input', async () => {
    const query = input.value.trim().toLowerCase();
    cachedQuery = '';
    hide();
    if (query.length < 2) { results.replaceChildren(); return; }
    try {
      const pages = await loadIndex();
      if (input.value.trim().toLowerCase() !== query) return;
      render(pages
        .map((page) => ({ page, score: score(page, query) }))
        .filter((match) => match.score > 0)
        .sort((left, right) => right.score - left.score)
        .slice(0, 8)
        .map((match) => match.page), query);
      cachedQuery = query;
    } catch (error) {
      if (input.value.trim().toLowerCase() !== query) return;
      results.textContent = 'Search is temporarily unavailable.';
      results.hidden = false;
      console.error(error);
    }
  });
})();
