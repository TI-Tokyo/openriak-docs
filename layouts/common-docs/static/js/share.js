(() => {
  'use strict';
  const root = document.querySelector('[data-share-control]');
  const trigger = root?.querySelector('.share-trigger');
  const panel = root?.querySelector('[data-share-panel]');
  const copyButton = root?.querySelector('[data-share-copy]');
  const copyLabel = root?.querySelector('[data-share-copy-label]');
  const nativeButton = root?.querySelector('[data-share-native]');
  const status = root?.querySelector('[data-share-status]');
  if (!root || !trigger || !panel || !copyButton || !copyLabel || !status) return;

  const menuItems = () => [...panel.querySelectorAll('[role="menuitem"]')]
    .filter((item) => !item.hidden && item.getClientRects().length > 0);
  const shareDetails = () => {
    const url = new URL(window.location.href);
    url.searchParams.delete('highlight');
    url.searchParams.delete('os');
    const selectedOs = document.documentElement.dataset.selectedOs;
    if (selectedOs) url.searchParams.set('os', selectedOs);
    return { title: document.title, url: url.href };
  };
  const updateDestinations = () => {
    const details = shareDetails();
    const encodedUrl = encodeURIComponent(details.url);
    const encodedTitle = encodeURIComponent(details.title);
    const destinations = {
      email: `mailto:?subject=${encodedTitle}&body=${encodedUrl}`,
      x: `https://twitter.com/intent/tweet?text=${encodedTitle}&url=${encodedUrl}`,
      bluesky: `https://bsky.app/intent/compose?text=${encodeURIComponent(`${details.title} ${details.url}`)}`,
      reddit: `https://www.reddit.com/submit?url=${encodedUrl}&title=${encodedTitle}`,
      linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`,
    };
    root.querySelectorAll('[data-share-target]').forEach((link) => {
      link.href = destinations[link.dataset.shareTarget] || details.url;
    });
    return details;
  };
  const close = (returnFocus = false) => {
    const wasOpen = !panel.hidden;
    panel.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
    if (returnFocus && wasOpen) trigger.focus();
  };
  const open = () => {
    updateDestinations();
    panel.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
    window.requestAnimationFrame(() => menuItems()[0]?.focus());
  };
  const copyText = async (value) => {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(value);
      return;
    }
    const field = document.createElement('textarea');
    field.value = value;
    field.setAttribute('readonly', '');
    field.style.position = 'fixed';
    field.style.opacity = '0';
    document.body.append(field);
    field.select();
    const copied = document.execCommand('copy');
    field.remove();
    if (!copied) throw new Error('Copy command was rejected');
  };

  nativeButton.hidden = !navigator.share;
  trigger.addEventListener('click', () => {
    if (panel.hidden) open();
    else close(true);
  });
  trigger.addEventListener('keydown', (event) => {
    if (!['ArrowDown', 'Enter', ' '].includes(event.key) || !panel.hidden) return;
    event.preventDefault();
    open();
  });
  copyButton.addEventListener('click', async () => {
    const original = copyLabel.textContent;
    try {
      await copyText(shareDetails().url);
      copyLabel.textContent = 'Copied!';
      status.textContent = 'Link copied to clipboard.';
    } catch (error) {
      copyLabel.textContent = 'Copy failed';
      status.textContent = 'The link could not be copied.';
      console.error(error);
    }
    window.setTimeout(() => { copyLabel.textContent = original; }, 1600);
  });
  nativeButton.addEventListener('click', async () => {
    try {
      await navigator.share(shareDetails());
      close(true);
    } catch (error) {
      if (error?.name !== 'AbortError') console.error(error);
    }
  });
  panel.addEventListener('keydown', (event) => {
    const items = menuItems();
    const current = items.indexOf(document.activeElement);
    let next = current;
    if (event.key === 'ArrowDown') next = (current + 1) % items.length;
    else if (event.key === 'ArrowUp') next = (current - 1 + items.length) % items.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = items.length - 1;
    else if (event.key === 'Escape') {
      event.preventDefault();
      close(true);
      return;
    } else if (event.key === 'Tab') {
      close();
      return;
    } else return;
    event.preventDefault();
    items[next]?.focus();
  });
  document.addEventListener('click', (event) => { if (!root.contains(event.target)) close(); });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape' && !panel.hidden) close(true); });
})();
