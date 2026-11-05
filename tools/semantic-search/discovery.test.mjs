import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {discoverTargets} from './discovery.mjs';
test('discovery follows the rendered profile, including historical versions and sections',()=>{
 const site=fs.mkdtempSync(path.join(os.tmpdir(),'semantic-discovery-'));
 const write=(scope,section,version='')=>{const dir=path.join(site,scope);fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,'semantic-source.json'),JSON.stringify({scope,section,version,pages:[]}));};
 write('openriak-kv/3.4.0/','openriak-kv','3.4.0');write('openriak-kv/3.4.1/','openriak-kv','3.4.1');write('community/','community');write('settings/','settings');write('','homepage');
 const before=discoverTargets(site);assert.equal(before.length,5);assert.ok(!before.some(t=>t.section==='archived-mailing-list'));
 write('riak-kv/1.0.0/','riak-kv','1.0.0');write('archived-mailing-list/','archived-mailing-list');
 const after=discoverTargets(site);
 assert.equal(after.length,7);assert.equal(after.find(t=>t.version==='3.4.1').publicPath,'semantic-indexes/openriak-kv/3.4.1');
 assert.equal(after.find(t=>t.version==='1.0.0').directory,'content/static/semantic-indexes/riak-kv/1.0.0');
 fs.rmSync(site,{recursive:true});
});
test('missing exports fail rather than silently accepting an incomplete build',()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'semantic-empty-'));assert.throws(()=>discoverTargets(dir),/No semantic source/);fs.rmSync(dir,{recursive:true});
});

test('a version outputs override cannot silently omit its index',()=>{
 const site=fs.mkdtempSync(path.join(os.tmpdir(),'semantic-omitted-'));
 fs.mkdirSync(path.join(site,'openriak-kv/3.4.0'),{recursive:true});
 fs.writeFileSync(path.join(site,'openriak-kv/3.4.0/index.html'),'<body data-product="openriak-kv">');
 assert.throws(()=>discoverTargets(site),/Missing semantic export for published version/);
 fs.rmSync(site,{recursive:true});
});
