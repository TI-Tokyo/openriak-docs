'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const root = path.resolve(__dirname, '../..');

// Exercise real Hugo partials in a static (non-server) build. Docker provides the
// repository's pinned Hugo; HUGO_EXECUTABLE can select an installed binary.
test('generated tag pages and full-size execution records render in production', {timeout:120000}, () => {
  const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'openriak-reference-render-'));
  const write = (file, value) => {
    const target = path.join(fixture, file);
    fs.mkdirSync(path.dirname(target), {recursive:true});
    fs.writeFileSync(target, value);
  };
  try {
    write('hugo.yaml', 'baseURL: https://example.test/docs/\ntimeout: 30s\ndisableKinds: [taxonomy, term, RSS, sitemap]\n');
    for (const name of ['reference-tag-pages', 'page-summary', 'page-version-status', 'code-block', 'json-resource', 'whats-changed-section', 'whats-changed-table']) {
      write(`layouts/partials/${name}.html`, fs.readFileSync(path.join(root, `layouts/docs-theme/layouts/partials/${name}.html`)));
    }
    write('layouts/partials/product-context.html', '{{ return (dict "id" "openriak-kv" "version" "3.4.1" "versions" (dict "3.4.1" (dict "documentationSource" "openriak-kv"))) }}');
    write('data/page_provenance/openriak-kv/3.4.1.json', JSON.stringify(Object.fromEntries(
      ['reference','reference/tags','reference/tags/concept','reference/tags/feature'].map(key=>[key,{status:'inherited',since:'3.4.0'}]))));
    write('content/reference/_index.md', '---\ntitle: Reference\n---\n');
    write('content/reference/tags/_index.md', '---\ntitle: Tags\n---\n');
    write('layouts/index.html', '{{ partial "whats-changed-section.html" (dict "section" (site.GetPage "/reference") "pathTitles" (slice)) }}');
    write('data/cli-reference/openriak-kv/3.4.1.json', JSON.stringify({pages:[{reference:{tags:{concept:['authentication']}}}]}));
    write('data/configuration-reference/openriak-kv/3.4.1.json', JSON.stringify({settings:[{tags:{feature:['security']}}]}));
    write('content/reference/tags/_content.gotmpl', '{{ partial "reference-tag-pages.html" (dict "adapter" . "version" "3.4.1") }}');
    write('layouts/shortcodes/reference-tag.html', 'Related documents');
    write('content/large.md', '---\ntitle: Large capture\n---\n');
    write('layouts/_default/list.html', '{{ .Content }}');
    write('layouts/_default/single.html', '{{ if .Params.reference_tag_page }}{{ partial "page-summary.html" . }}{{ .Content }}{{ else }}{{ partial "code-block.html" (dict "Page" . "Type" "json" "Attributes" (dict "output-limit" 15) "Inner" (readFile "large.txt")) }}{{ end }}');
    const source = JSON.stringify({stdout:'<script>unsafe & text</script>\n' + 'handoff-'.repeat(2*1024*1024) + '\nFINAL OUTPUT', stderr:'complete stderr'});
    write('large.txt', source);
    const args = ['--source', fixture, '--destination', path.join(fixture,'public'), '--buildDrafts', '--minify'];
    const build = () => {
      if (process.env.HUGO_EXECUTABLE) return execFileSync(process.env.HUGO_EXECUTABLE, args, {timeout:90000, stdio:'pipe'});
      const version = fs.readFileSync(path.join(root,'.hugo-version'),'utf8').trim();
      return execFileSync('docker', ['run','--rm','--user',`${process.getuid()}:${process.getgid()}`,
        '--mount',`type=bind,source=${fixture},target=${fixture}`, '--entrypoint','hugo',
        `ghcr.io/gohugoio/hugo:v${version}`, ...args], {timeout:90000, stdio:'pipe'});
    };
    build();
    for (const tag of ['concept/authentication','feature/security']) {
      const html = fs.readFileSync(path.join(fixture,`public/reference/tags/${tag}/index.html`),'utf8');
      assert.match(html,/Related documents/);
      assert.doesNotMatch(html,/doc-version-status/);
    }
    const html = fs.readFileSync(path.join(fixture,'public/large/index.html'),'utf8');
    assert.ok(html.includes('FINAL OUTPUT'));
    assert.ok(html.includes('&lt;script&gt;unsafe &amp; text&lt;/script&gt;'));
    assert.ok(!html.includes('<script>unsafe'));
    const rendered = html.match(/<pre\b[^>]*><code\b[^>]*>([\s\S]*?)<\/code><\/pre>/)[1]
      .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
      .replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
    assert.equal(rendered, source, 'the visible block also retains the complete capture');
    assert.match(html,/data-code-expand/);
    assert.match(html,/data-code-copy/);
    assert.match(html,/data-code-download/);
    const resource = html.match(/data-json-src=["']?([^\s"'>]+)/)[1];
    const payload = JSON.parse(fs.readFileSync(path.join(fixture,'public',resource.replace(/^\/docs\//,'')),'utf8'));
    assert.equal(payload,source,'copy/download payload keeps every byte of both streams');
    write('content/reference/untracked.md', '---\ntitle: Missing history\n---\n');
    assert.throws(build, /missing page provenance/, 'authored pages still require provenance');
  } finally { fs.rmSync(fixture,{recursive:true,force:true}); }
});
