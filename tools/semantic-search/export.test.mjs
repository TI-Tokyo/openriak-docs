import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {discoverTargets} from './discovery.mjs';
import sourceTools from './kv-source.cjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
test('Hugo exports all active scopes at a domain root and below a base path',()=>{
 const relative='tools/generated/semantic-render/export-test',dir=path.join(root,relative);
 fs.rmSync(dir,{recursive:true,force:true});
 const write=(name,text)=>{fs.mkdirSync(path.dirname(path.join(dir,name)),{recursive:true});fs.writeFileSync(path.join(dir,name),text);};
 write('hugo.yaml',`baseURL: https://example.test/
disableKinds: [RSS, taxonomy, term, sitemap]
outputFormats:
  SemanticSource:
    mediaType: application/json
    baseName: semantic-source
    isPlainText: true
    notAlternative: true
segments:
  semantic:
    includes:
      - output: semanticsource
outputs:
  home: [HTML, SemanticSource]
  section: [HTML, SemanticSource]
`);
 const template=fs.readFileSync(path.join(root,'layouts/docs-theme/layouts/_default/section.semanticsource.json.json'),'utf8');
 for(const name of ['home','section','single'])write(`layouts/_default/${name}.semanticsource.json.json`,template);
 write('layouts/_default/list.html','{{ .Content }}');write('layouts/_default/single.html','{{ .Content }}');
 write('layouts/shortcodes/deployment-links.html', '<p><a href="{{ `community/` | relURL }}">Local</a> <a href="https://docs.example.test/docs/reference/">External</a></p><pre>cat /docs/literal</pre>\n[Image]({{ site.Home.RelPermalink }}images/example.png)');
 const diagram='graph LR; A-->B';
 const diagramKey=createHash('sha256').update(diagram).digest('hex');
 write('layouts/_markup/render-codeblock.html',fs.readFileSync(path.join(root,'layouts/docs-theme/layouts/_markup/render-codeblock.html'),'utf8'));
 for(const width of ['wide','narrow'])write(`assets/mermaid/${diagramKey}.${width}.svg`,'<svg id="__OPENRIAK_DIAGRAM__"><text>A to B</text></svg>');
 write('content/_index.md','---\ntitle: Home\n---\nWelcome.');
 for(const scope of ['openriak-kv/3.4.0','openriak-kv/3.4.1','openriak-kv/1.0.0','community','archived-mailing-list']){
  write(`content/${scope}/_index.md`,'---\ntitle: Section\n---\nSection content.');
  write(`content/${scope}/article.md`,'---\ntitle: Article\n---\nA searchable paragraph.\n\n{{< deployment-links >}}\n\n```mermaid\ngraph LR; A-->B\n```');
 }
 write('content/openriak-kv/latest/_index.md','---\ntitle: Latest\nlatest_redirect_route: openriak-kv\n---\nRedirect.');
 write('content/settings.md','---\ntitle: Settings\nlayout: settings\noutputs: [HTML, SemanticSource]\n---\n');
 write('data/settings_sections.json',JSON.stringify([{id:'appearance',title:'Appearance',description:'Adjust the colour theme.'}]));
 const fingerprints=new Map();
 for(const [folder,base,full] of [['root','https://example.test/'],['prefix','http://localhost:1410/docs/'],['beta','https://www.tiot.jp/openriak-docs-beta/'],['beta-full','https://www.tiot.jp/openriak-docs-beta/',true]]){
  const result=spawnSync('docker',['run','--rm','--user',`${process.getuid?.()||1000}:${process.getgid?.()||1000}`,'-v',`${root}:/project`,'--entrypoint','hugo','ghcr.io/gohugoio/hugo:v0.166.0',`--source=/project/${relative}`,`--destination=/project/${relative}/${folder}`,`--baseURL=${base}`,'--noBuildLock',...(full?[]:['--renderSegments=semantic'])],{encoding:'utf8'});
  assert.equal(result.status,0,result.stdout+result.stderr);
  const targets=discoverTargets(path.join(dir,folder));
  assert.equal(fs.existsSync(path.join(dir,folder,'openriak-kv/3.4.0/index.html')),Boolean(full));
  for(const target of targets){
   const exported=JSON.parse(fs.readFileSync(path.join(dir,folder,target.exportPath)));
   const digest=sourceTools.sourceDigest(exported,target.scope);
   if(folder==='root')fingerprints.set(target.scope,digest);
   else assert.equal(digest,fingerprints.get(target.scope),`${folder}: ${target.scope} must be deployment-independent`);
  }
  assert.equal(targets.length,7);assert.ok(!targets.some(t=>t.version==='latest'));
  const settings=JSON.parse(fs.readFileSync(path.join(dir,folder,'settings/semantic-source.json')));
  assert.match(settings.pages[0].html,/Adjust the colour theme/);
  assert.equal(targets.find(t=>t.version==='1.0.0').scope,'openriak-kv/1.0.0/');
 }
});
