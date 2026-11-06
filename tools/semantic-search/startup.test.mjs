import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {parse} from 'yaml';
const compose=parse(fs.readFileSync(new URL('../../docker/compose.yaml',import.meta.url),'utf8'),{merge:true});
test('run script builds the toolchain; core prepares every selected index before either server starts',()=>{
 const runner=fs.readFileSync(new URL('../../docker/run.local.sh',import.meta.url),'utf8');
 assert.match(runner,/up --build --force-recreate --renew-anon-volumes/);
 assert.ok(!compose.services['semantic-indexer']);
 const service=compose.services.core,command=service.command.join(' ');
 assert.equal(service.build.dockerfile,'docker/Dockerfile.dev');
 for(const name of ['core','archives']){
  const generation=command.indexOf(`--site-dir /project/tools/generated/semantic-dev/${name}`);
  assert.ok(generation>0&&generation<command.indexOf('exec hugo server'));
 }
 assert.match(command,/if \[ "\$\$\{OPENRIAK_DOCS_BUILD_PROFILE\}" = release \]/);
 assert.ok(service.volumes.includes('../content/static:/project/content/static'));
 assert.ok(service.volumes.includes('/project/tools/semantic-search/node_modules'));
 assert.equal(compose.services.archives.depends_on.core.condition,'service_healthy');
});

test('release repairs legacy root-owned archive output before starting unprivileged Hugo',()=>{
 const init=compose.services['archive-output-init'];
 assert.equal(init.user,'0:0');
 assert.equal(init.restart,'no');
 assert.deepEqual(init.profiles,['release']);
 assert.deepEqual(init.volumes,['../build/archives:/archive-output']);
 assert.deepEqual(init.command,['chown -R node:node /archive-output']);
 assert.equal(compose.services.archives.depends_on['archive-output-init'].condition,'service_completed_successfully');
 assert.equal(compose.services.archives.user,undefined);
});
