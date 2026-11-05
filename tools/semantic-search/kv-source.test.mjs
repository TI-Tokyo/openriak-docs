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
