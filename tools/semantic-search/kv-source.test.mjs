import {test} from 'node:test';
import assert from 'node:assert/strict';
import source from './kv-source.cjs';
import {makePassages} from './passages.mjs';
test('rendered source is independent of hostname and base path',()=>{
 const sample=base=>({baseURL:base,pages:[{title:'A',url:new URL('openriak-kv/3.4.1/how-to/a/',base).pathname,html:`<h2>Heading</h2><p>Read <a href="${base}openriak-kv/3.4.1/">this</a>.</p><script src="${base}metadata/different.json"></script>`}]});
 assert.equal(source.sourceDigest(sample('https://example.test/')),source.sourceDigest(sample('http://localhost:1410/docs/')));
});
test('other versions cannot leak into the index',()=>{
 assert.throws(()=>source.canonicalPages({baseURL:'https://example.test/docs/',pages:[{title:'Old',url:'/docs/openriak-kv/3.4.0/',html:'Old'}]}),/outside KV/);
});
test('rendered HTML preserves headings and code, excluding controls and metadata',()=>{
 const p=makePassages('Command','<h2>Usage</h2><p>First sentence. Second sentence. Third sentence.</p><div class="doc-code-header">Shell <button>Copy</button></div><div><pre><code>riak-admin status</code></pre></div><script>Secret metadata</script>',s=>s.split(/\s+/).length,256,true);
 assert.equal(p[0].heading,'Usage');assert.equal(p[0].text,'First sentence. Second sentence. Third sentence.');
 assert.ok(p.some(p=>p.kind==='code'&&p.text.includes('riak-admin status')));assert.ok(p.every(p=>!p.text.includes('Copy')&&!p.text.includes('Secret metadata')&&!p.text.includes('Shell')));
});
test('identical repeated output is collapsed within a page without crossing headings or pages',async()=>{
 const {uniqueIndices}=await import('./index-files.mjs');
 const p={url:'page/',title:'Page',heading:'Output',text:'Repeated output'};
 assert.deepEqual(uniqueIndices([p,{...p},{...p,heading:'Other'},{...p,url:'other/'},{...p,text:'Different output'}]),[0,2,3,4]);
});

test('whitespace-only syntax error highlighting cannot make an index stale',()=>{
 const sample=html=>({baseURL:'https://example.test/docs/',pages:[{title:'Code',url:'/docs/openriak-kv/3.4.1/code/',html}]});
 assert.equal(source.sourceDigest(sample('<pre><code>  value</code></pre>')),source.sourceDigest(sample('<pre><code><span class="err"> </span> value</code></pre>')));
 assert.notEqual(source.sourceDigest(sample('<p>before</p>')),source.sourceDigest(sample('<p>after</p>')));
});

test('stylesheet injection and indentation are independent of the rendered output format',()=>{
 const sample=html=>({baseURL:'https://example.test/docs/',pages:[{title:'Article',url:'/docs/openriak-kv/3.4.1/page/',html}]});
 assert.equal(source.sourceDigest(sample('<p>Text.</p>\n  <div>Note.</div>')),source.sourceDigest(sample('<p>Text.</p>\n        <link rel="stylesheet" href="/css/theme.css">\n  <div>Note.</div>')));
 assert.notEqual(source.sourceDigest(sample('<pre>first\nsecond</pre>')),source.sourceDigest(sample('<pre>first second</pre>')));
});

const deploymentSample=base=>({baseURL:base,pages:[{
 title:'Links and commands',url:new URL('openriak-kv/3.4.1/page/',base).pathname,
 html:`<p><a href="${base}openriak-kv/3.4.1/">Local</a>
 <a href="http://docs.oracle.com/javase/7/docs/technotes/">External</a>
 <a href="https://other.test/docs/page/">Other site</a> <a href="/docs/openriak-kv/3.4.0/page/">Historical internal link</a></p>
 <img src='${new URL(base).pathname}images/example.png'>
 <div data-url=${new URL(base).pathname}community/ data-label="/docs/literal" data-copy-value="${base}downloads/example">Text</div>
 <p>[Image](${new URL(base).pathname}images/example.png)</p>
 <p>[[Example]: ${new URL(base).pathname}community/</p><p>[Missing colon] ${new URL(base).pathname}openriak-kv/3.4.1/</p>
 <pre><code>curl https://other.test/docs/api/\n[Archived link](${new URL(base).pathname}openriak-kv/3.4.1/page/)\ncat /docs/literal\ncurl ${base}downloads/example\n[Code](/docs/code)</code></pre>
 <p><code>/docs/literal</code> and ordinary /docs/literal prose.</p>`
}]});
test('deployment paths do not rewrite external links, code or prose',()=>{
 const original=deploymentSample('https://www.openriak.org/docs/');
 const beta=deploymentSample('https://www.tiot.jp/openriak-docs-beta/');
 // data-label is plain text, not a URL attribute.
 assert.equal(source.sourceDigest(original),source.sourceDigest(beta));
 assert.equal(source.sourceDigest(original),source.sourceDigest(deploymentSample('http://localhost:1410/')));
 const html=source.canonicalPages(original)[0].html;
 assert.match(html,/http:\/\/docs.oracle.com\/javase\/7\/docs\/technotes\//);
 assert.match(html,/cat \/docs\/literal/);
 assert.match(html,/\[Code\]\(\/docs\/code\)/);
 assert.match(html,/ordinary \/docs\/literal prose/);
 assert.match(html,/href="\/openriak-kv\/3.4.1\/"/);
 assert.match(html,/\[Image\]\(\/images\/example.png\)/);
 assert.match(html,/\[\[Example\]: \/community\//);
});
test('historical fingerprints compare using their verified source deployment',()=>{
 const original=deploymentSample('https://www.openriak.org/docs/'),beta=deploymentSample('https://www.tiot.jp/openriak-docs-beta/');
 for(const [version,digest] of [[undefined,source.legacySourceDigest],[undefined,source.sourceDigestV2],[1,source.sourceDigestV1],[2,source.sourceDigestV2],[3,source.sourceDigest]]){
  const manifest={sourceNormalization:version,sourceBaseURL:original.baseURL,sourceDigest:digest(original)};
  assert.equal(source.matchesSourceDigest(beta,'openriak-kv/3.4.1/',manifest),true);
  const changed=structuredClone(beta);changed.pages[0].html+='<p>Changed content.</p>';
  assert.equal(source.matchesSourceDigest(changed,'openriak-kv/3.4.1/',manifest),false);
 }
});
test('external URLs and literal paths remain part of the fingerprint',()=>{
 const original=deploymentSample('https://www.openriak.org/docs/');
 for(const [from,to] of [['/7/docs/technotes/','/8/docs/technotes/'],['cat /docs/literal','cat /other/literal'],['ordinary /docs/literal','ordinary /changed/literal']]){
  const changed=structuredClone(original);changed.pages[0].html=changed.pages[0].html.replace(from,to);
  assert.notEqual(source.sourceDigest(changed),source.sourceDigest(original));
 }
 assert.throws(()=>source.matchesSourceDigest(original,'openriak-kv/3.4.1/',{sourceNormalization:99}),/Unsupported/);
});
