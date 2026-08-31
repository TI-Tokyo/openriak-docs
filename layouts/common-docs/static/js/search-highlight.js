(() => {
  'use strict';
  const root = document.querySelector('[data-search-highlight-root]');
  const parameters = new URL(window.location.href).searchParams;
  const terms = [...new Map(parameters.getAll('highlight')
    .map((term) => term.trim().slice(0, 200))
    .filter(Boolean)
    .map((term) => [term.toLowerCase(), term])).values()]
    .sort((left, right) => right.length - left.length)
    .slice(0, 8);
  if (!root || !terms.length) return;

  const escaped = terms.map((term) => term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  const pattern = new RegExp(`(${escaped.join('|')})`, 'gi');
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      if (!node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
      if (node.parentElement?.closest('script, style, noscript, textarea, mark, [data-no-search-highlight]')) return NodeFilter.FILTER_REJECT;
      pattern.lastIndex = 0;
      return pattern.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    },
  });
  const textNodes = [];
  while (textNodes.length < 500 && walker.nextNode()) textNodes.push(walker.currentNode);

  let highlighted = 0;
  textNodes.forEach((node) => {
    const parts = node.nodeValue.split(pattern);
    const replacement = document.createDocumentFragment();
    parts.forEach((part, index) => {
      if (index % 2 === 0) {
        if (part) replacement.append(document.createTextNode(part));
        return;
      }
      const mark = document.createElement('mark');
      mark.className = 'search-highlight';
      mark.textContent = part;
      replacement.append(mark);
      highlighted += 1;
    });
    node.replaceWith(replacement);
  });

  const first = root.querySelector('mark.search-highlight');
  if (!first) return;
  let disclosure = first.closest('details:not([open])');
  while (disclosure) {
    disclosure.open = true;
    disclosure = disclosure.parentElement?.closest('details:not([open])');
  }

  const clear = document.createElement('button');
  clear.type = 'button';
  clear.className = 'search-highlight-clear';
  clear.textContent = `Clear ${highlighted} search highlight${highlighted === 1 ? '' : 's'}`;
  clear.addEventListener('click', () => {
    root.querySelectorAll('mark.search-highlight').forEach((mark) => mark.replaceWith(document.createTextNode(mark.textContent)));
    root.normalize();
    clear.remove();
    const url = new URL(window.location.href);
    url.searchParams.delete('highlight');
    history.replaceState(history.state, '', url);
  });
  document.body.append(clear);
  requestAnimationFrame(() => first.scrollIntoView({ behavior: 'smooth', block: 'center' }));
})();
