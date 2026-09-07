(() => {
  'use strict';
  const requests = new Map();
  const load = (source) => {
    const url = new URL(source, document.baseURI);
    if (url.origin !== window.location.origin) return Promise.reject(new Error('Metadata must be same-origin'));
    const key = url.href;
    if (!requests.has(key)) {
      const request = fetch(key, { credentials: 'same-origin', cache: 'force-cache' })
        .then(response => {
          if (!response.ok) throw new Error(`Metadata request failed: ${response.status} ${key}`);
          return response.json();
        }).catch(error => { requests.delete(key); throw error; });
      requests.set(key, request);
    }
    return requests.get(key);
  };
  const read = (element) => element?.dataset.jsonSrc
    ? load(element.dataset.jsonSrc)
    : Promise.resolve().then(() => JSON.parse(element?.textContent || 'null'));
  window.OpenRiakMetadata = { load, read };
})();
