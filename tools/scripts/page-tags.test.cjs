'use strict';
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const {execFileSync}=require('node:child_process');
const yaml=require('./vendor/js-yaml/js-yaml');
const {validateTags}=require('./annotation-tags');
const root=path.resolve(__dirname,'../..');
const walk=dir=>fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):e.name.endsWith('.md')?[path.join(dir,e.name)]:[]);

test('3.4.0 and 3.4.1 pages carry explicit, valid feature and concept lists',()=>{
  for(const version of ['3.4.0-new-release','3.4.1'])for(const file of walk(path.join(root,'content/openriak-kv',version))){
    const source=fs.readFileSync(file,'utf8');
    const data=yaml.load(source.match(/^---\n([\s\S]*?)\n---/)[1]);
    if(data.reference_tag_page) {
      assert.equal(data.hide_sidebar,true,file);
      assert.equal(data.exclude_search,true,file);
      assert.match(source,/\{\{< tag-list >\}\}/,file);
      continue;
    }
    assert.ok(Array.isArray(data.features),file);
    assert.ok(Array.isArray(data.concepts),file);
    validateTags({feature:data.features,concept:data.concepts},file);
    assert.ok(data.features.length+data.concepts.length>0,file);
  }
});

test('typed header links and tag results stay within the mounted product release', {timeout:120000},()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'openriak-page-tags-'));
  const write=(file,text)=>{const dest=path.join(dir,file);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,text);};
  const copy=(from,to)=>write(to,fs.readFileSync(path.join(root,from)));
  try{
    write('hugo.yaml',yaml.dump({baseURL:'https://example.test/docs/',disableKinds:['RSS','sitemap','taxonomy','term']}));
    write('layouts/_default/baseof.html','{{ block "main" . }}{{ end }}');
    write('layouts/_default/single.html','{{ define "main" }}{{ partial "page-summary.html" . }}{{ .Content }}{{ end }}');
    write('layouts/_default/list.html','{{ define "main" }}{{ .Content }}<aside>{{ partial "nav-tree.html" (dict "pages" .Pages "current" .) }}</aside><nav>{{ range .Pages }}<a href="{{ .RelPermalink }}">{{ .Title }}</a>{{ end }}</nav><script id="search" type="application/json">{{ partial "search-test.html" . | safeJS }}</script>{{ end }}');
    copy('layouts/docs-theme/layouts/partials/nav-tree.html','layouts/partials/nav-tree.html');
    copy('layouts/docs-theme/layouts/_default/section.search.json.json','layouts/partials/search-test.html');
    for(const name of ['page-summary','page-tags','reference-tag-index'])copy(`layouts/docs-theme/layouts/partials/${name}.html`,`layouts/partials/${name}.html`);
    write('layouts/partials/product-context.html','{{ $parts := strings.Split (strings.TrimPrefix "/" .Path) "/" }}{{ return (dict "id" (index $parts 0) "version" (index $parts 1) "productBase" "/docs/openriak-kv/" "versions" dict) }}');
    copy('layouts/docs-theme/layouts/shortcodes/tag-list.html','layouts/shortcodes/tag-list.html');
    write('content/_index.md','---\ntitle: Documentation\n---\n');
    write('content/openriak-kv/_index.md','---\ntitle: OpenRiak KV\n---\n');
    for(const version of ['3.4.0','3.4.1']){
      write(`content/openriak-kv/${version}/_index.md`,'---\ntitle: Version\n---\n');
      // An inherited page retains the older source front matter: grouping must
      // use its mounted URL to avoid putting 3.4.1 documents in the 3.4.0 group.
      write(`content/openriak-kv/${version}/guide.md`,'---\ntitle: Handoff guide\nproduct_id: openriak-kv\nproduct_version: 3.4.0\nfeatures: [handoff, cluster-management]\nconcepts: [partition-transfer]\n---\nGuide.');
    }
    write('content/community/_index.md','---\ntitle: Community\n---\n');
    write('content/openriak-kv/3.4.1/same-name.md','---\ntitle: Same name, different type\nconcepts: [handoff]\n---\nCommunity.');
    write('content/openriak-kv/3.4.1/draft.md','---\ntitle: Hidden draft\ndraft: true\nfeatures: [handoff]\n---\nDraft.');
    for(const version of ['3.4.0','3.4.1']) {
      const {tagPageSource}=require('./validate-page-tags');
      write(`content/openriak-kv/${version}/tags/_index.md`,tagPageSource());
      for(const [type,tags] of Object.entries({feature:['handoff','cluster-management'],concept:['partition-transfer',...(version==='3.4.1'?['handoff']:[])]})) {
        write(`content/openriak-kv/${version}/tags/${type}/_index.md`,tagPageSource(type));
        for(const tag of tags)write(`content/openriak-kv/${version}/tags/${type}/${tag}.md`,
          tagPageSource(type,tag).replace('<!-- Add introductory text here. -->','Before the list.').replace('<!-- Add further context here. -->','After the list.'));
      }
      write(`data/cli-reference/openriak-kv/${version}.json`,JSON.stringify({pages:[]}));
      write(`data/configuration-reference/openriak-kv/${version}.json`,JSON.stringify({settings:[]}));
    }
    const args=['--source',dir,'--destination',path.join(dir,'public'),'--minify'];
    if(process.env.HUGO_EXECUTABLE)execFileSync(process.env.HUGO_EXECUTABLE,args,{stdio:'pipe'});
    else execFileSync('docker',['run','--rm','--user',`${process.getuid()}:${process.getgid()}`,'--mount',`type=bind,source=${dir},target=${dir}`,'--entrypoint','hugo',`ghcr.io/gohugoio/hugo:v${fs.readFileSync(path.join(root,'.hugo-version'),'utf8').trim()}`,...args],{stdio:'pipe',encoding:'utf8',timeout:90000});
    const read=file=>fs.readFileSync(path.join(dir,'public',file,'index.html'),'utf8');
    for(const version of ['3.4.0','3.4.1']) {
      const prefix=`openriak-kv/${version}`;
      const versionHtml=read(prefix);
      assert.doesNotMatch(versionHtml.match(/<aside>([\s\S]*?)<\/aside>/)[1],/\/tags\//,'sidebar omits the entire tag tree');
      const search=JSON.parse(versionHtml.match(/<script id=search[^>]*>([\s\S]*?)<\/script>/)[1]);
      assert.ok(search.some(entry=>entry.url.endsWith('/guide/')));
      assert.ok(search.every(entry=>!entry.url.includes('/tags/')),'search omits all tag pages');
      assert.ok(read(`${prefix}/tags`).includes(`/docs/${prefix}/tags/feature/`));
      assert.ok(read(`${prefix}/tags/feature`).includes(`/docs/${prefix}/tags/feature/handoff/`));
      const guide=read(`${prefix}/guide`);
      assert.match(guide,/doc-summary[\s\S]*min read[\s\S]*data-tag-type=feature/);
      for(const route of ['feature/handoff','feature/cluster-management','concept/partition-transfer']) {
        assert.ok(guide.includes(`/docs/${prefix}/tags/${route}/`));
        const tag=read(`${prefix}/tags/${route}`);
        assert.ok(tag.includes(`/docs/${prefix}/guide/`));
        assert.ok(!tag.includes(`/docs/openriak-kv/${version==='3.4.0'?'3.4.1':'3.4.0'}/`));
        assert.doesNotMatch(tag,/Same name|Hidden draft/);
        assert.match(tag,/Before the list[\s\S]*reference-tag-documents[\s\S]*After the list/);
      }
    }
    const concept=read('openriak-kv/3.4.1/tags/concept/handoff');
    assert.match(concept,/Same name, different type/);
    assert.doesNotMatch(concept,/Handoff guide/);
    assert.ok(!fs.existsSync(path.join(dir,'public/tags')),'no site-wide tag pages');
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});

test('missing tag pages fail the build after staging editable Markdown stubs',()=>{
  const fixture=fs.mkdtempSync(path.join(os.tmpdir(),'openriak-tag-stubs-'));
  try {
    const {generatePageProvenance}=require('./generate-version-mounts');
    const content=path.join(fixture,'content');
    const release=path.join(content,'openriak-kv/3.4.0-new-release');
    fs.mkdirSync(release,{recursive:true});
    fs.writeFileSync(path.join(release,'guide.md'),'---\ntitle: Guide\nfeatures: [new-feature]\nconcepts: [new-concept]\n---\nGuide.');
    const products=[{source:'openriak-kv',target:'openriak-kv',minVersion:'3.4.0'}];
    const build=()=>generatePageProvenance(content,products,path.join(fixture,'page-provenance'));
    assert.throws(build,/missing Markdown tag pages:[\s\S]*Stub files created/);
    const stubs=path.join(fixture,'tag-stubs/openriak-kv/3.4.0-new-release');
    assert.equal(walk(stubs).length,5,'create both type indexes, two tags and the root index');
    assert.match(fs.readFileSync(path.join(stubs,'tags/feature/new-feature.md'),'utf8'),/\{\{< tag-list >\}\}/);
    assert.ok(!fs.existsSync(path.join(release,'tags')),'build cannot silently fill authored content');
    fs.cpSync(path.join(stubs,'tags'),path.join(release,'tags'),{recursive:true});
    assert.doesNotThrow(build);
    const patch=path.join(content,'openriak-kv/3.4.1');
    fs.mkdirSync(patch);
    fs.writeFileSync(path.join(patch,'second.md'),'---\ntitle: Second guide\nfeatures: [new-feature]\n---\nInherited tag page.');
    assert.doesNotThrow(build,'inherited Markdown tag pages satisfy the newer release');
    fs.writeFileSync(path.join(patch,'second.md'),'---\ntitle: Second guide\nfeatures: [unregistered]\n---\nMissing tag page.');
    assert.throws(build,/3.4.1: missing Markdown tag pages:[\s\S]*tags\/feature\/unregistered/);
  }finally{fs.rmSync(fixture,{recursive:true,force:true});}
});
