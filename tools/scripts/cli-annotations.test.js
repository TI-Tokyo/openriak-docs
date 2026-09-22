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
