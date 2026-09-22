'use strict';

const assert = require('node:assert/strict');
const { test } = require('node:test');
const { buildVersionCandidates, pageExists } = require('../../layouts/docs-theme/static/js/docs-runtime');

const root = 'https://www.tiot.jp/openriak-docs-beta/openriak-kv/3.2.4/';
const candidate = root + 'reference/commands/riak/';
const response = (url, status = 200) => ({ url, status, ok: status >= 200 && status < 300 });

test('version probes accept pages and redirects only within the selected version', async () => {
  for (const destination of [candidate, root, root + 'reference/command-line-tools/']) {
    assert.equal(await pageExists(candidate, root, async () => response(destination)), true, destination);
  }
  for (const destination of [
    'https://www.tiot.jp/en/solutions/riak/',
    root.replace('www.tiot.jp', 'other.example'),
    root.replace('https:', 'http:'),
    root.replace('3.2.4/', '3.4.0/'),
    root.replace('3.2.4/', '3.2.40/'),
    root.replace('openriak-kv/', 'openriak-cs/'),
  ]) {
    assert.equal(await pageExists(candidate, root, async () => response(destination)), false, destination);
  }
  assert.equal(await pageExists(candidate, root, async () => response(candidate, 404)), false);
  assert.equal(await pageExists(candidate, root, async () => { throw new Error('Network failure'); }), false);
});

test('GET fallback after unsupported HEAD also validates the redirect destination', async () => {
  for (const [destination, expected] of [[candidate, true], ['https://www.tiot.jp/en/solutions/riak/', false]]) {
    const methods = [];
    assert.equal(await pageExists(candidate, root, async (url, options) => {
      methods.push(options.method || 'GET');
      return options.method === 'HEAD' ? response(url, 405) : response(destination);
    }), expected);
    assert.deepEqual(methods, ['HEAD', 'GET']);
  }
});

test('a missing CLI page skips the WordPress redirect and falls back to the version homepage', async () => {
  const candidates = buildVersionCandidates({
    currentUrl: root.replace('3.2.4/', '3.4.0/') + 'reference/commands/riak/admin/aae-status/',
    productBase: '/openriak-docs-beta/openriak-kv/', currentVersion: '3.4.0', targetVersion: '3.2.4',
  });
  const visited = [];
  let selected;
  for (const url of candidates) {
    if (await pageExists(url, root, async () => {
      visited.push(url);
      if (url === candidate) return response('https://www.tiot.jp/en/solutions/riak/');
      return response(url, url === root ? 200 : 404);
    })) { selected = url; break; }
  }
  assert.ok(visited.includes(candidate));
  assert.equal(selected, root);
});
