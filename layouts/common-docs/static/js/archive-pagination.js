(() => {
  'use strict';
  const defaultPageSize = '12';

  document.querySelectorAll('[data-archive-listing]').forEach((listing) => {
    const items = [...listing.querySelectorAll('[data-archive-item]')];
    const pageSizeSelect = listing.querySelector('[data-archive-page-size]');
    const summary = listing.querySelector('[data-archive-page-summary]');
    const pagination = listing.querySelector('[data-archive-pagination]');
    const itemLabel = listing.dataset.itemLabel || 'items';
    const allowedSizes = new Set([...(pageSizeSelect?.options || [])].map((option) => option.value));
    if (!allowedSizes.size) allowedSizes.add(defaultPageSize);

    const updateSortLinks = (pageSize) => {
      listing.querySelectorAll('.sort-option').forEach((link) => {
        const url = new URL(link.href, window.location.href);
        url.searchParams.delete('page');
        if (pageSize === defaultPageSize) url.searchParams.delete('items');
        else url.searchParams.set('items', pageSize);
        link.href = url;
      });
    };

    const pageLink = (pageNumber, label, current = false) => {
      const link = document.createElement('a');
      const url = new URL(window.location.href);
      if (pageNumber === 1) url.searchParams.delete('page');
      else url.searchParams.set('page', String(pageNumber));
      link.className = `page-btn${current ? ' current' : ''}`;
      link.href = url;
      link.dataset.archivePage = String(pageNumber);
      link.textContent = label;
      if (current) link.setAttribute('aria-current', 'page');
      return link;
    };

    const renderPagination = (page, totalPages) => {
      if (!pagination) return;
      pagination.replaceChildren();
      pagination.hidden = totalPages < 2;
      if (totalPages < 2) return;
      pagination.append(pageLink(Math.max(1, page - 1), '←'));
      const shown = new Set([1, totalPages, page - 1, page, page + 1].filter((value) => value >= 1 && value <= totalPages));
      let previous = 0;
      [...shown].sort((left, right) => left - right).forEach((pageNumber) => {
        if (pageNumber > previous + 1) {
          const gap = document.createElement('span');
          gap.className = 'page-gap';
          gap.setAttribute('aria-hidden', 'true');
          gap.textContent = '…';
          pagination.append(gap);
        }
        pagination.append(pageLink(pageNumber, String(pageNumber), pageNumber === page));
        previous = pageNumber;
      });
      pagination.append(pageLink(Math.min(totalPages, page + 1), '→'));
      pagination.firstElementChild?.setAttribute('aria-label', 'Previous page');
      pagination.lastElementChild?.setAttribute('aria-label', 'Next page');
    };

    const render = () => {
      const url = new URL(window.location.href);
      const requestedSize = url.searchParams.get('items') || defaultPageSize;
      const selectedSize = allowedSizes.has(requestedSize) ? requestedSize : defaultPageSize;
      const pageSize = selectedSize === 'all' ? Math.max(items.length, 1) : Number(selectedSize);
      const totalPages = Math.max(1, Math.ceil(items.length / pageSize));
      const requestedPage = Number(url.searchParams.get('page') || 1);
      const page = Math.min(totalPages, Math.max(1, Number.isInteger(requestedPage) ? requestedPage : 1));
      const first = (page - 1) * pageSize;
      const last = first + pageSize;
      items.forEach((item, index) => { item.hidden = index < first || index >= last; });
      if (pageSizeSelect) pageSizeSelect.value = selectedSize;
      if (summary) summary.textContent = `Page ${page} of ${totalPages} · ${items.length} ${itemLabel}`;
      updateSortLinks(selectedSize);
      renderPagination(page, totalPages);
    };

    pageSizeSelect?.addEventListener('change', () => {
      const url = new URL(window.location.href);
      if (pageSizeSelect.value === defaultPageSize) url.searchParams.delete('items');
      else url.searchParams.set('items', pageSizeSelect.value);
      url.searchParams.delete('page');
      window.history.pushState({}, '', url);
      render();
    });
    pagination?.addEventListener('click', (event) => {
      const link = event.target.closest('[data-archive-page]');
      if (!link) return;
      event.preventDefault();
      window.history.pushState({}, '', link.href);
      render();
      listing.scrollIntoView({ block: 'start', behavior: 'smooth' });
    });
    window.addEventListener('popstate', render);
    render();
  });
})();
