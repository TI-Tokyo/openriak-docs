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
test('generated tags, large outputs and downloadable evidence render in production', {timeout:120000}, () => {
  const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'openriak-reference-render-'));
  const write = (file, value) => {
    const target = path.join(fixture, file);
    fs.mkdirSync(path.dirname(target), {recursive:true});
    fs.writeFileSync(target, value);
  };
  try {
    write('hugo.yaml', 'baseURL: https://example.test/docs/\ntimeout: 30s\ndisableKinds: [taxonomy, term, RSS, sitemap]\n');
    for (const name of ['reference-tag-pages', 'reference-tag-index', 'page-summary', 'page-version-status', 'code-block', 'json-resource', 'whats-changed-section', 'whats-changed-table', 'cli/evidence-download', 'cli/output']) {
      write(`layouts/partials/${name}.html`, fs.readFileSync(path.join(root, `layouts/docs-theme/layouts/partials/${name}.html`)));
    }
    write('layouts/partials/product-context.html', '{{ return (dict "id" "openriak-kv" "version" "3.4.1" "productBase" "/docs/openriak-kv/" "versions" (dict "3.4.1" (dict "documentationSource" "openriak-kv"))) }}');
    write('data/page_provenance/openriak-kv/3.4.1.json', JSON.stringify(Object.fromEntries(
      ['reference','reference/tags','reference/tags/concept','reference/tags/feature'].map(key=>[key,{status:'inherited',since:'3.4.0'}]))));
    write('content/reference/_index.md', '---\ntitle: Reference\n---\n');
    write('content/reference/tags/_index.md', '---\ntitle: Tags\n---\n');
    write('layouts/index.html', '{{ partial "whats-changed-section.html" (dict "section" (site.GetPage "/reference") "pathTitles" (slice)) }}');
    write('layouts/partials/search-test.html', fs.readFileSync(path.join(root,'layouts/docs-theme/layouts/_default/section.search.json.json')));
    write('content/downloads/_index.md', '---\ntitle: Downloads\n---\n');
    write('content/downloads/records.md', '---\ntitle: Execution records\ndownload_fixture: true\n---\n{{< evidence >}}');
    write('layouts/downloads/list.html', '{{ partial "search-test.html" . }}');
    write('layouts/shortcodes/evidence.html', '{{ partial "cli/evidence-download.html" (dict "data" hugo.Data.records "filename" "execution" "label" "Download execution records") }}');
    write('content/outputs.md', '---\ntitle: Output whitespace\ndownload_fixture: true\n---\n{{< output-cases >}}');
    write('layouts/shortcodes/output-cases.html', '{{ range hugo.Data.outputcases }}{{ partial "cli/output.html" (dict "page" $.Page "text" .raw "stream" "Standard output") }}{{ end }}');
    write('data/cli-reference/openriak-kv/3.4.1.json', JSON.stringify({pages:[{reference:{tags:{concept:['authentication'],module:['riak_core'],repository:['riak_core']}}}]}));
    write('data/configuration-reference/openriak-kv/3.4.1.json', JSON.stringify({settings:[{tags:{feature:['security']}}]}));
    write('content/reference/tags/_content.gotmpl', '{{ partial "reference-tag-pages.html" (dict "adapter" . "version" "3.4.1") }}');
    write('layouts/shortcodes/reference-tag.html', fs.readFileSync(path.join(root, 'layouts/docs-theme/layouts/shortcodes/reference-tag.html')));
    write('content/openriak-kv/3.4.1/reference/tags/_content.gotmpl', '{{ partial "reference-tag-pages.html" (dict "adapter" . "version" "3.4.1") }}');
    for (const [name, tags] of Object.entries({
      'module-only': {annotation_tags:{module:['riak_core']}},
      'repository-only': {tags:{repository:['riak_core']}},
      'both-types': {annotation_tags:{module:['riak_core'],repository:['riak_core']}},
      'untyped': {tags:['riak_core']},
    })) {
      write(`content/openriak-kv/3.4.1/${name}.md`, JSON.stringify({title:name, download_fixture:true, ...tags}) + '\nDocument.');
    }
    write('content/large.md', '---\ntitle: Large capture\n---\n');
    write('layouts/_default/list.html', '{{ .Content }}');
    write('layouts/_default/single.html', '{{ if .Params.reference_tag_page }}<h1>{{ .Title }}</h1>{{ partial "page-summary.html" . }}{{ .Content }}{{ else if .Params.download_fixture }}{{ .Content }}{{ else }}{{ partial "code-block.html" (dict "Page" . "Type" "text" "Attributes" (dict "output-limit" 15) "Inner" (readFile "large.txt")) }}{{ end }}');
    const source = JSON.stringify({stdout:'<script>unsafe & text</script>\n' + 'handoff-'.repeat(2*1024*1024) + '\nFINAL OUTPUT', stderr:'complete stderr'});
    write('large.txt', source);
    const outputCases = [
      {raw:'No transfers active\n \nActive Transfers:\n \n \nok\n \n\t', displayed:'No transfers active\n \nActive Transfers:\n \n \nok'},
      {raw:'\n  indented value  \r\n \t\r\n', displayed:'\n  indented value  '},
      {raw:'one\n\n two', displayed:'one\n\n two'},
      {raw:'\n \t\n', displayed:''},
    ];
    write('data/outputcases.json', JSON.stringify(outputCases));
    const records = [{phase:'verify:example', argv:['curl','http://localhost:8098/test'],
      stdout:'RAW_RECORD_SENTINEL\n' + source, stderr:'all stderr\n', exit_code:0}];
    records.push(...outputCases.map(c=>({stdout:c.raw, stderr:'', exit_code:0})));
    write('data/records.json', JSON.stringify(records));
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
      assert.match(html,/reference-tag-documents/);
      assert.doesNotMatch(html,/doc-version-status/);
    }
    for (const type of ['module','repository']) {
      const tagHtml = fs.readFileSync(path.join(fixture,`public/openriak-kv/3.4.1/reference/tags/${type}/riak_core/index.html`),'utf8');
      assert.match(tagHtml, new RegExp(`<h1>${type[0].toUpperCase()+type.slice(1)}: riak_core</h1>`));
      assert.ok(tagHtml.includes(`${type}-only`));
      assert.ok(tagHtml.includes('both-types'));
      assert.ok(!tagHtml.includes(`${type==='module'?'repository':'module'}-only`));
      assert.ok(!tagHtml.includes('untyped'));
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
    const downloadHtml = fs.readFileSync(path.join(fixture,'public/downloads/records/index.html'),'utf8');
    assert.doesNotMatch(downloadHtml,/RAW_RECORD_SENTINEL|<pre|data-code-block/);
    assert.match(downloadHtml,/download=["']?execution\.json/);
    const href = downloadHtml.match(/href=["']?([^\s"'>]+)/)[1];
    assert.deepEqual(JSON.parse(fs.readFileSync(path.join(fixture,'public',href.replace(/^\/docs\//,'')),'utf8')), records);
    const search = fs.readFileSync(path.join(fixture,'public/downloads/index.html'),'utf8');
    assert.doesNotMatch(search,/RAW_RECORD_SENTINEL/);
    assert.match(search,/Download execution records/);
    const outputHtml = fs.readFileSync(path.join(fixture,'public/outputs/index.html'),'utf8');
    const outputResources = [...outputHtml.matchAll(/data-json-src=["']?([^\s"'>]+)/g)];
    assert.equal(outputResources.length, outputCases.length);
    for (const [i, match] of outputResources.entries()) {
      const displayed = JSON.parse(fs.readFileSync(path.join(fixture,'public',match[1].replace(/^\/docs\//,'')),'utf8'));
      assert.equal(displayed, outputCases[i].displayed, 'trim only trailing blank lines, preserving internal whitespace');
    }
    write('content/reference/untracked.md', '---\ntitle: Missing history\n---\n');
    assert.throws(build, /missing page provenance/, 'authored pages still require provenance');
  } finally { fs.rmSync(fixture,{recursive:true,force:true}); }
});
