'use strict';
const assert = require('node:assert/strict');
const {test} = require('node:test');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {buildAnnotatedReference, fingerprint, reviewFingerprint} = require('./cli-annotations');
const {parseMarkdown} = require('./cli-annotation-markdown');
const command = {id:'shell:riak admin describe',path:['riak','admin','describe'],invocation:'riak admin describe',context:'shell',availability:'available',arguments:[],options:[],global_options:[{name:'--format',allowed_values:['human','json'],default:'human'}],help:'Usage: riak admin describe <variable>',reference:{examples:[{id:'describe:ok',title:'A single name',invocation:'riak admin describe ring_size',description:'Generated description',stdout:'ring_size: documentation',stderr:'',exit_code:0,verification:{image_id:'sha256:test'}}],results:[{id:'ok',description:'Generated result'}],errors:[{id:'missing',condition:'No name',description:'Usage',remedy:'Supply a name'}]}};
command.reference.examples[0].verification.command_fingerprint = fingerprint(command);
const document = {runtime:{id:'sha256:test'},schema_version:1,product:'kv',version:'3.4.1',status:'complete',commands:[command]};
function fixture(fn) {const root = fs.mkdtempSync(path.join(os.tmpdir(),'cli-annotations-')); try {fn(root);} finally {fs.rmSync(root,{recursive:true,force:true});}}
function write(root, name, text, commandPath = 'cli/riak/admin/describe') {
 const file = path.join(root,commandPath,name+'.md'); fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,text);return file;
}
const review = () => `\n# Reviewed against\n\n3.4.1: ${reviewFingerprint(command)}\n`;

test('every released CLI topic has usable annotations and matching runtime evidence', () => {
  for (const version of ['3.4.0', '3.4.1']) {
    const raw = JSON.parse(fs.readFileSync(path.join(__dirname, `../../content/openriak-kv/metadata/${version}/kv-cli-commands.json`)));
    const ref = buildAnnotatedReference(raw);
    assert.equal(ref.annotationCoverage.complete, ref.pages.length, version);
    assert.deepEqual(ref.annotationCoverage.issues, [], version);
    for (const page of ref.pages) {
      assert.ok(page.reference.summary && page.reference.description, page.key);
      assert.ok(page.reference.overrides.length, page.key);
      for (const parameter of page.parameters) {
        assert.ok(parameter.description, `${page.key}: ${parameter.name}`);
        assert.ok(parameter.datatype || parameter.allowedValues?.length, `${page.key}: ${parameter.name} values`);
      }
      for (const example of page.reference.examples) {
        assert.ok(example.title && example.invocation && example.description, page.key);
        if (example.observed) assert.equal(example.observed.verification.image_id, raw.runtime.id);
      }
    }
  }
});

test('Markdown retains multiple paragraphs, lists and code headings inside long fields', () => {
 const annotation = parseMarkdown('# Options\n\n## --format\nrequired: false\nrepeatable: false\ndefault: human\n\n### Valid values\n- human\n- `json`\n\n### Description\nFirst paragraph.\n\nSecond paragraph.\n\n```sh\n# not a section\necho hi\n```\n\n# Notes\n\n- A note\n- Another note');
 assert.equal(annotation.option_overrides['--format'].required,false);
 assert.deepEqual(annotation.option_overrides['--format'].allowed_values,['human','json']);
 assert.match(annotation.option_overrides['--format'].description,/First paragraph\.\n\nSecond paragraph/);
 assert.match(annotation.option_overrides['--format'].description,/# not a section/);
 assert.equal(annotation.notes[0],'- A note\n- Another note');
});
test('shared and release Markdown inherit fields, retain evidence, and clear lists explicitly', () => fixture(root => {
 write(root,'common','# Summary\nShared\n\n# Examples\n## describe:ok\ntitle: Read a setting\n### Description\nEditorial description'+review());
 write(root,'3.4.1','# Summary\nVersion-specific\n\n# Errors\n'+review());
 write(root,'3.4.0','# Summary\nWrong release');
 const result = buildAnnotatedReference(document,{overrideRoot:root}), ref = result.pages[0].reference;
 assert.equal(ref.summary,'Version-specific');assert.equal(ref.examples[0].title,'Read a setting');assert.equal(ref.examples[0].description,'Editorial description');
 assert.equal(ref.examples[0].observed.stdout,'ring_size: documentation');assert.equal(ref.evidence[0].description,'Generated description');
 assert.equal(ref.results[0].description,'Generated result');assert.deepEqual(ref.errors,[]);assert.deepEqual(result.annotationCoverage.issues,[]);
 assert.equal(command.reference.examples[0].description,'Generated description');
}));
test('option fields merge independently; arguments form one table with flags and defaults', () => fixture(root => {
 write(root,'common','# Options\n## --format\nrequired: false\nrepeatable: false\n### Description\nFirst paragraph.\n\nSecond paragraph.\n\n# Arguments\n## variable\nrequired: true\nrepeatable: true\ndatatype: setting name\n### Description\nOne or more names.');
 write(root,'3.4.1','# Options\n## --format\ndefault: json\n### Valid values\n- json');
 const page = buildAnnotatedReference(document,{overrideRoot:root}).pages[0];
 assert.equal(page.options[0].defaultValue,'json');assert.deepEqual(page.options[0].allowedValues,['json']);
 assert.match(page.options[0].description,/First paragraph\.\n\nSecond paragraph/);
 assert.equal(page.parameters.length,2);assert.equal(page.parameters[0].required,true);assert.equal(page.parameters[0].repeatable,true);assert.equal(page.parameters[1].required,false);
 assert.equal(command.global_options[0].default,'human');
}));
test('changing an invocation does not reuse output as verified evidence', () => fixture(root => {
 write(root,'common','# Examples\n## describe:ok\n### Invocation\n```sh\nriak admin describe storage_backend\n```');
 const ref = buildAnnotatedReference(document,{overrideRoot:root}).pages[0].reference;
 assert.equal(ref.examples[0].invocation,'riak admin describe storage_backend');assert.equal(ref.examples[0].observed,undefined);assert.equal(ref.evidence[0].stdout,'ring_size: documentation');
}));
test('visible shell examples use riak while preserving exact evidence and argument quoting', () => fixture(root => {
 const input=structuredClone(document), example=input.commands[0].reference.examples[0];
 const launcher='VMARGS_PATH=/var/lib/riak/vm.args /usr/lib/riak/bin/riak';
 for(const [invocation,display] of [
  [`${launcher} admin cluster join openriak-kv@node2.test`,'riak admin cluster join openriak-kv@node2.test'],
  [`RELX_COOKIE=wrong ${launcher} admin member-status`,'RELX_COOKIE=wrong riak admin member-status'],
  [`env ${launcher} admin bucket-type update orders '{"props":{"allow_mult":true}}'`, `riak admin bucket-type update orders '{"props":{"allow_mult":true}}'`],
  [`${launcher} eval '"/usr/lib/riak/bin/riak VMARGS_PATH=/var/lib/riak/vm.args".'`, `riak eval '"/usr/lib/riak/bin/riak VMARGS_PATH=/var/lib/riak/vm.args".'`],
  ['VMARGS_PATH=/custom/node.args /usr/lib/riak/bin/riak ping','VMARGS_PATH=/custom/node.args riak ping'],
  ['riak admin cluster plan','riak admin cluster plan'],
 ]) {
  example.invocation=invocation;
  const rendered=buildAnnotatedReference(input,{overrideRoot:root}).pages[0].reference;
  assert.equal(rendered.examples[0].display_invocation,display);
  assert.equal(rendered.examples[0].invocation,invocation);
  assert.equal(rendered.examples[0].observed.invocation,invocation);
  assert.equal(rendered.evidence[0].invocation,invocation);
 }
 example.description=`On the joining node:\n\n\`\`\`sh\n${launcher} admin cluster join openriak-kv@node2.test\n\`\`\`\n\n\`\`\`text\n${launcher}\n\`\`\``;
 const rendered=buildAnnotatedReference(input,{overrideRoot:root}).pages[0].reference.examples[0];
 assert.ok(rendered.display_description.includes('```sh\nriak admin cluster join openriak-kv@node2.test\n```'));
 assert.ok(rendered.display_description.includes('```text\n'+launcher+'\n```'));
 assert.equal(rendered.observed.description,example.description);
}));
test('per-example test details retain matching setup and checks without unrelated cases', () => fixture(root => {
 const input=structuredClone(document), proof=input.commands[0].reference.examples[0].verification;
 Object.assign(proof,{scenario:'describe',case:'ok',sha256:'recipe-hash'});
 input.coverage={scenarios:{scenarios:[{id:'describe',sha256:'recipe-hash',image_id:'sha256:test',steps:[
  {phase:'setup',argv:['prepare']},{phase:'case_setup:ok',argv:['prepare-case']},
  {phase:'case:ok',argv:['describe']},{phase:'verify:ok',argv:['read-back']},
  {phase:'case:other',argv:['unrelated']}
 ]}]}};
 const example=buildAnnotatedReference(input,{overrideRoot:root}).pages[0].reference.examples[0];
 assert.deepEqual(example.observed.test_steps.map(s=>s.argv[0]),['prepare','prepare-case','describe','read-back']);
 assert.equal(input.commands[0].reference.examples[0].test_steps,undefined);
 input.coverage.scenarios.scenarios[0].sha256='different-recipe';
 assert.equal(buildAnnotatedReference(input,{overrideRoot:root}).pages[0].reference.examples[0].observed.test_steps,undefined);
}));
test('new authored examples and errors require complete descriptions', () => fixture(root => {
 write(root,'common','# Examples\n## local-example\ntitle: Another setting\n### Invocation\nriak admin describe storage_backend\n### Description\nRead its schema.\n\n# Errors\n## local-error\n### Condition\nUnknown name\n### Description\nAn error is printed.\n### Remedy\nCorrect the name.');
 const ref = buildAnnotatedReference(document,{overrideRoot:root}).pages[0].reference;
 assert.equal(ref.examples[1].observed,undefined);assert.equal(ref.errors[1].id,'local-error');
 write(root,'common','# Examples\n## typo\n### Description\nWrong');
 assert.throws(()=>buildAnnotatedReference(document,{overrideRoot:root}),/unknown example/);
}));
test('invalid fields, unknown flags and attempts to edit evidence are rejected', () => fixture(root => {
 for(const [text, expected] of [
  ['# Examples\n## describe:ok\n### Stdout\nForged',/invalid example_overrides/],
  ['# Options\n## --typo\n### Description\nUnknown',/unknown option/],
  ['# Options\n## --format\nrequired: maybe',/true or false/],
  ['# Options\n## --format\n### Valid values\njson',/bullet list/],
  ['# Summary\nOne\n# Summary\nTwo',/duplicate section/],
  ['# Notes\n```\nUnclosed',/unclosed code fence/],
  ['# Typo\nText',/unknown section/],
 ]) {write(root,'common',text);assert.throws(()=>buildAnnotatedReference(document,{overrideRoot:root}),expected);}
}));
test('command directories and optional arities cannot target unrelated commands', () => fixture(root => {
 write(root,'common','# Summary\nMissing','cli/riak/admin/missing');
 assert.throws(()=>buildAnnotatedReference(document,{overrideRoot:root}),/missing command/);
 fs.rmSync(path.join(root,'cli'),{recursive:true});
 write(root,'common','# Metadata\ncommand: shell:riak stop\n# Summary\nWrong');
 assert.throws(()=>buildAnnotatedReference(document,{overrideRoot:root}),/does not match its directory/);
}));
test('shared errors link to their ancestor without duplicating test examples', () => fixture(root => {
 const parent={id:'shell:riak admin',path:['riak','admin'],invocation:'riak admin',context:'shell',availability:'available',options:[],arguments:[],reference:{errors:[{id:'cookie',condition:'Wrong cookie',description:'No connection',remedy:'Use configured cookie'}],examples:[{id:'cookie',invocation:'RELX_COOKIE=wrong riak admin member-status',description:'Test cookie'}]}};
 const ref=buildAnnotatedReference({...document,commands:[parent,command]},{overrideRoot:root});
 const child=ref.pages.find(p=>p.route==='riak/admin/describe');
 assert.deepEqual(child.reference.sharedErrors,[{route:'riak/admin',title:'riak admin'}]);
 assert.equal(child.reference.examples.length,1);assert.ok(!child.reference.examples[0].invocation.includes('COOKIE'));
}));
test('stale reviews and observations are reported without discarding original evidence', () => fixture(root => {
 write(root,'common','# Summary\nReview me\n# Reviewed against\n3.4.1: '+'0'.repeat(64));
 const changed=structuredClone(document);changed.commands[0].help='Changed';
 const ref=buildAnnotatedReference(changed,{overrideRoot:root});
 assert.deepEqual(ref.annotationCoverage.issues.map(i=>i.status),['stale','stale_evidence']);
 assert.equal(ref.pages[0].reference.examples[0].observed,undefined);assert.ok(ref.pages[0].reference.evidence[0].stdout);
}));
test('scenario contracts require review; observation timestamps do not', () => {
 const current=reviewFingerprint(command), rerun=structuredClone(command);
 rerun.reference.examples[0].verification.tested_at='later';assert.equal(reviewFingerprint(rerun),current);
 rerun.reference.examples[0].verification.sha256='changed';assert.notEqual(reviewFingerprint(rerun),current);
});
test('preview watcher notices nested Markdown edits, additions and removals, retaining valid output on errors', async () => {
 const {watch}=require('./watch-cli-reference');const root=fs.mkdtempSync(path.join(os.tmpdir(),'cli-watch-'));
 const inputRoot=path.join(root,'metadata'),overrideRoot=path.join(root,'overrides'),outputRoot=path.join(root,'output');
 fs.mkdirSync(path.join(inputRoot,'3.4.1'),{recursive:true});fs.writeFileSync(path.join(inputRoot,'3.4.1/kv-cli-commands.json'),JSON.stringify(document));
 const common=write(overrideRoot,'common','# Summary\nFirst');
 const log=console.log,error=console.error,errors=[];console.log=()=>{};console.error=e=>errors.push(e);let timer;
 const output=path.join(outputRoot,'openriak-kv/data/cli-reference/3.4.1.json');
 const wait=()=>new Promise(resolve=>setTimeout(resolve,70));const summary=()=>JSON.parse(fs.readFileSync(output)).pages[0].reference.summary;
 try {
  timer=watch({inputRoot,overrideRoot,outputRoot,intervalMs:10});assert.equal(summary(),'First');
  write(overrideRoot,'common','# Summary\nSecond');await wait();assert.equal(summary(),'Second');
  const version=write(overrideRoot,'3.4.1','# Summary\nVersion');await wait();assert.equal(summary(),'Version');
  fs.unlinkSync(version);await wait();assert.equal(summary(),'Second');
  const valid=fs.readFileSync(output,'utf8');fs.writeFileSync(common,'# Unknown\nBad');await wait();
  assert.equal(fs.readFileSync(output,'utf8'),valid);assert.ok(errors.length);
 } finally {clearInterval(timer);console.log=log;console.error=error;fs.rmSync(root,{recursive:true,force:true});}
});

test('annotations can omit spurious discovered flags without editing source evidence', () => fixture(root => {
 write(root,'common','# Options\n## --format\nomit: true');
 const result=buildAnnotatedReference(document,{overrideRoot:root});
 assert.deepEqual(result.pages[0].options,[]);
 assert.deepEqual(result.pages[0].parameters,[]);
 assert.equal(command.global_options[0].name,'--format');
 write(root,'3.4.1','# Options\n## --format\nomit: false');
 assert.equal(buildAnnotatedReference(document,{overrideRoot:root}).pages[0].options[0].name,'--format');
}));
test('nested selector annotations resolve an arity before the selector suffix', () => fixture(root => {
 const c={id:'erlang:riak_client:aae_fold/1:list_buckets',context:'erlang',kind:'erlang_function',
  module:'riak_client',function:'aae_fold',arity:1,path:['riak_client','aae_fold','list_buckets'],
  selector:'list_buckets',arguments:[],options:[],signatures:['aae_fold(Query)'],availability:'available'};
 write(root,'common','# Metadata\ncommand: erlang:riak_client:aae_fold/1:list_buckets\n\n# Summary\nList AAE buckets.','riak-attach/riak_client/aae_fold/list_buckets');
 const result=buildAnnotatedReference({...document,commands:[c]},{overrideRoot:root});
 assert.equal(result.pages[0].reference.summary,'List AAE buckets.');
}));
test('Erlang topics link to shared attach errors', () => fixture(root => {
 const attach={id:'shell:riak attach',invocation:'riak attach',path:['riak','attach'],context:'shell',arguments:[],options:[],help:'',availability:'available'};
 const api={id:'erlang:riak:local_client/0',module:'riak',function:'local_client',arity:0,context:'erlang',kind:'erlang_function',path:['riak','local_client'],arguments:[],options:[],signatures:['local_client()'],availability:'available'};
 write(root,'common','# Errors\n## undef\n### Condition\nMissing function\n### Description\nundef\n### Remedy\nCheck the arity','cli/riak/attach');
 const result=buildAnnotatedReference({...document,commands:[attach,api]},{overrideRoot:root});
 assert.deepEqual(result.pages.find(p=>p.context==='erlang').reference.sharedErrors,[{route:'riak/attach',title:'riak attach'}]);
}));

test('module and operation parents own shared Erlang parameter descriptions',()=>{
 const parsed=parseMarkdown('# Shared arguments\n\n## Client\n\ndatatype: riak_client handle\n\n### Description\n\nFirst paragraph.\n\nSecond paragraph.');
 assert.equal(parsed.shared_arguments[0].name,'Client');
 assert.match(parsed.shared_arguments[0].description,/First paragraph\.\n\nSecond paragraph/);
 for(const version of ['3.4.0','3.4.1']) {
  const ref=buildAnnotatedReference(JSON.parse(fs.readFileSync(`content/openriak-kv/metadata/${version}/kv-cli-commands.json`)));
  const parent=ref.sections.find(p=>p.route==='erlang/riak-client');
  assert.match(parent.reference.shared_arguments.find(p=>p.name==='Bucket').description, /\{<<"cli_examples">>, <<"orders">>\}/);
  for(const page of ref.pages.filter(p=>p.route.startsWith('erlang/riak-client/'))) {
   const client=page.parameters.find(p=>p.name==='Client');
   if(client) assert.deepEqual(client.shared,{route:'erlang/riak-client',title:'riak_client',anchor:'argument-client'});
  }
  const erase=ref.pages.find(p=>p.route.endsWith('/erase-keys'));
  assert.equal(erase.parameters.find(p=>p.name==='ModifiedRange').shared.route,'erlang/riak-client/aae-fold');
  assert.equal(erase.parameters.find(p=>p.name==='Client').required,false);
  const dates=ref.pages.find(p=>p.route==='erlang/riak-client/aae-fold').reference.shared_arguments.find(p=>p.name==='ModifiedRange');
  assert.match(dates.description,/2026-12-24T23:59:59Z/);
 }
});
