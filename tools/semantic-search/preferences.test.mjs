import {test} from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const source=fs.readFileSync(new URL('../../layouts/common-docs/static/js/search-preferences.js',import.meta.url),'utf8');
test('section configuration supplies defaults; browser overrides stay isolated and can be reset',()=>{
 const saved=new Map(),window={OpenRiakSettings:{write:(key,value)=>saved.set(key,value)}};
 const sections=[{id:'community',defaults:{text:false,semantic:true,timing:'together'}},{id:'settings',defaults:{text:true,semantic:false,timing:'asap'}}];
 vm.runInNewContext(source,{window,document:{getElementById:()=>({textContent:JSON.stringify(sections)})},localStorage:{getItem:key=>saved.get(key)||null},URL,location:{href:'https://example.test/docs/'}});
 const p=window.OpenRiakSearchPreferences;
 assert.equal(p.read('community').text,false);assert.equal(p.read('community').timing,'together');
 assert.equal(p.read('community').highlight,true);p.write('community',{highlight:false});assert.equal(p.read('community').highlight,false);
 p.write('community',{text:true});assert.equal(p.read('community').text,true);assert.equal(p.read('settings').semantic,false);
 assert.throws(()=>p.write('community',{semantic:'false'}));assert.throws(()=>p.write('homepage',{text:true}));
 saved.clear();assert.equal(p.read('community').text,false);
 assert.equal(p.section('/docs/semantic-indexes/riak-kv/2.0.0/manifest.json'),'openriak-kv');
});
