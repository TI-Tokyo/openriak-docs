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
    assert.ok(Array.isArray(data.features),file);
    assert.ok(Array.isArray(data.concepts),file);
    validateTags({feature:data.features,concept:data.concepts},file);
    assert.ok(data.features.length+data.concepts.length>0,file);
  }
});

test('typed header links resolve to global indexes grouped by mounted release', {timeout:120000},()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'openriak-page-tags-'));
  const write=(file,text)=>{const dest=path.join(dir,file);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,text);};
  const copy=(from,to)=>write(to,fs.readFileSync(path.join(root,from)));
  try{
    const config=yaml.load(fs.readFileSync(path.join(root,'content/hugo.yaml'),'utf8'));
    write('hugo.yaml',yaml.dump({baseURL:'https://example.test/docs/',disableKinds:['RSS','sitemap'],taxonomies:config.taxonomies,permalinks:config.permalinks}));
    write('layouts/_default/baseof.html','{{ block "main" . }}{{ end }}');
    write('layouts/_default/single.html','{{ define "main" }}{{ partial "page-summary.html" . }}{{ .Content }}{{ end }}');
    write('layouts/_default/list.html','{{ define "main" }}{{ .Content }}{{ end }}');
    for(const name of ['page-summary','page-tags'])copy(`layouts/docs-theme/layouts/partials/${name}.html`,`layouts/partials/${name}.html`);
    write('layouts/partials/product-context.html','{{ return (dict "version" "3.4.1" "versions" dict) }}');
    for(const kind of ['term','taxonomy'])copy(`layouts/common-docs/layouts/tags/${kind}.html`,`layouts/${kind}.html`);
    write('content/openriak-kv/_index.md','---\ntitle: OpenRiak KV\n---\n');
    for(const version of ['3.4.0','3.4.1']){
      // An inherited page retains the older source front matter: grouping must
      // use its mounted URL to avoid putting 3.4.1 documents in the 3.4.0 group.
      write(`content/openriak-kv/${version}/guide.md`,'---\ntitle: Handoff guide\nproduct_id: openriak-kv\nproduct_version: 3.4.0\nfeatures: [handoff, cluster-management]\nconcepts: [partition-transfer]\n---\nGuide.');
    }
    write('content/community/_index.md','---\ntitle: Community\n---\n');
    write('content/community/same-name.md','---\ntitle: Same name, different type\nconcepts: [handoff]\n---\nCommunity.');
    write('content/community/draft.md','---\ntitle: Hidden draft\ndraft: true\nfeatures: [handoff]\n---\nDraft.');
    const args=['--source',dir,'--destination',path.join(dir,'public'),'--minify'];
    if(process.env.HUGO_EXECUTABLE)execFileSync(process.env.HUGO_EXECUTABLE,args,{stdio:'pipe'});
    else execFileSync('docker',['run','--rm','--user',`${process.getuid()}:${process.getgid()}`,'--mount',`type=bind,source=${dir},target=${dir}`,'--entrypoint','hugo',`ghcr.io/gohugoio/hugo:v${fs.readFileSync(path.join(root,'.hugo-version'),'utf8').trim()}`,...args],{stdio:'pipe',timeout:90000});
    const read=file=>fs.readFileSync(path.join(dir,'public',file,'index.html'),'utf8');
    const guide=read('openriak-kv/3.4.1/guide');
    assert.match(guide,/doc-summary[\s\S]*min read[\s\S]*data-tag-type=feature/);
    for(const route of ['feature/handoff','feature/cluster-management','concept/partition-transfer']){
      assert.ok(guide.includes(`/docs/tags/${route}/`));
      assert.ok(read(`tags/${route}`).includes('/docs/openriak-kv/3.4.1/guide/'));
    }
    const feature=read('tags/feature/handoff');
    assert.match(feature,/<h1>Feature: handoff<\/h1>/);
    assert.match(feature,/<h2>OpenRiak KV 3.4.0<\/h2>/);
    assert.match(feature,/<h2>OpenRiak KV 3.4.1<\/h2>/);
    assert.doesNotMatch(feature,/Same name|Hidden draft/);
    const concept=read('tags/concept/handoff');
    assert.match(concept,/<h1>Concept: handoff<\/h1>/);
    assert.match(concept,/Same name, different type/);
    assert.doesNotMatch(concept,/Handoff guide/);
    assert.match(read('tags/feature'),/\/docs\/tags\/feature\/handoff\//);
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
