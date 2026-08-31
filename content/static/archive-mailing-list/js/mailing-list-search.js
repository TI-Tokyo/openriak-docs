(() => {
  const normalize = (value) => String(value || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

  document.querySelectorAll('[data-mailing-list-search]').forEach((root) => {
    const input = root.querySelector('[data-mailing-list-search-input]');
    const status = root.querySelector('[data-mailing-list-search-status]');
    const results = root.querySelector('[data-mailing-list-search-results]');
    let indexPromise;
    let timer;

    const loadIndex = () => {
      if (!indexPromise) {
        status.textContent = 'Loading search index…';
        indexPromise = fetch(root.dataset.indexUrl)
          .then((response) => {
            if (!response.ok) throw new Error(`Search index returned ${response.status}`);
            return response.json();
          })
          .then((items) => items.map((item) => ({
            ...item,
            titleText: normalize(item.title),
            authorText: normalize(item.authors || item.author),
            contentText: normalize(item.content),
          })))
          .catch((error) => {
            indexPromise = undefined;
            status.textContent = 'Search is temporarily unavailable.';
            throw error;
          });
      }
      return indexPromise;
    };

    const render = (matches, query) => {
      results.replaceChildren();
      if (!matches.length) {
        results.hidden = true;
        status.textContent = `No conversations found for “${query}”.`;
        return;
      }
      const fragment = document.createDocumentFragment();
      matches.slice(0, 30).forEach(({ item }) => {
        const link = document.createElement('a');
        const url = new URL(item.url, new URL(root.dataset.indexUrl, window.location.href));
        query.trim().split(/\s+/).filter(Boolean).slice(0, 8).forEach((term) => url.searchParams.append('highlight', term));
        link.href = url;
        const title = document.createElement('strong');
        title.textContent = item.title;
        const meta = document.createElement('span');
        meta.textContent = `${item.author} · ${item.date}`;
        link.append(title, meta);
        fragment.append(link);
      });
      results.append(fragment);
      results.hidden = false;
      status.textContent = `${matches.length} conversation${matches.length === 1 ? '' : 's'} found${matches.length > 30 ? '; showing 30' : ''}.`;
    };

    const search = async () => {
      const query = input.value.trim();
      const terms = normalize(query).split(/\s+/).filter(Boolean);
      if (terms.join('').length < 2) {
        results.hidden = true;
        results.replaceChildren();
        status.textContent = '';
        return;
      }
      const items = await loadIndex();
      const matches = [];
      items.forEach((item) => {
        const allText = `${item.titleText} ${item.authorText} ${item.contentText}`;
        if (!terms.every((term) => allText.includes(term))) return;
        let score = 0;
        terms.forEach((term) => {
          if (item.titleText.includes(term)) score += 8;
          if (item.authorText.includes(term)) score += 4;
          if (item.contentText.includes(term)) score += 1;
        });
        matches.push({ item, score });
      });
      matches.sort((left, right) => right.score - left.score || right.item.date.localeCompare(left.item.date) || left.item.title.localeCompare(right.item.title));
      render(matches, query);
    };

    input.addEventListener('input', () => {
      clearTimeout(timer);
      timer = setTimeout(() => search().catch(() => {}), 140);
    });
    input.addEventListener('focus', () => {
      if (input.value.trim().length >= 2) search().catch(() => {});
    });
  });
})();
