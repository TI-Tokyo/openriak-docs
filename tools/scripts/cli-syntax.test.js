'use strict';
const assert=require('node:assert/strict');
const {test}=require('node:test');
const fs=require('node:fs');
const {buildAnnotatedReference}=require('./cli-annotations');
const {reviewMarkdown}=require('./cli-syntax');
const shell=(words,more={})=>({id:`shell:${words}`,path:words.split(' '),invocation:words,context:'shell',kind:'shell',availability:'available',help:'',arguments:[],options:[],usage:[],...more});
const build=commands=>buildAnnotatedReference({schema_version:1,product:'kv',version:'3.4.1',status:'complete',commands},{overrideRoot:'/tmp/no-cli-syntax-overrides'});
test('parent syntax follows discovered children and aliases with real page links',()=>{
 const ref=build([
  shell('riak admin',{usage:['Usage: riak-admin { member_status | ghost }'],options:[{name:'--child-only',source:'usage'}]}),
  shell('riak admin member-status',{aliases:[{invocation:'riak admin member_status'}]}),
  shell('riak admin member_status',{aliases:[{invocation:'riak admin member-status'}]}),
  shell('riak admin remove'),shell('riak admin absent',{availability:'unavailable'}),
  shell('riak admin cluster join'),
 ]);
 const parent=ref.pages.find(p=>p.route==='riak/admin'),review=parent.syntax.review;
 assert.equal(parent.syntax.forms[0].text,'riak admin { cluster | member-status | remove }');
 assert.deepEqual(parent.syntax.forms[0].tokens.filter(t=>t.route).map(t=>t.route),['riak/admin/cluster','riak/admin/member-status','riak/admin/remove']);
 assert.deepEqual(review.missingFromProvided,['cluster','remove']);assert.deepEqual(review.onlyInProvided,['ghost']);
 assert.ok(review.issues.some(i=>i.includes('--child-only')));
});
test('complete arguments and options generate required, optional, repeated and typed forms',()=>{
 const ref=build([shell('riak inspect',{
  argument_format:'positional',arguments:[{name:'key',required:true,repeatable:true},{name:'limit',required:false,repeatable:false}],
  options:[{name:'--verbose',datatype:'boolean',required:false,repeatable:false},{name:'--format',allowed_values:['human','json'],required:false,repeatable:false}],
  usage:['Usage: riak inspect <key> ... [<limit>]'],
 })]);
 const syntax=ref.pages[0].syntax;
 assert.equal(syntax.basis,'arguments_and_options');
 assert.equal(syntax.forms[0].text,'riak inspect <key> ... [<limit>] [--format {human|json}] [--verbose]');
 assert.equal(syntax.review.status,'needs_review');assert.equal(syntax.review.displayed,'generated');
});
test('incomplete metadata retains supplied syntax and flags uncertainty without publishing guesses',()=>{
 const ref=build([shell('riak inspect',{arguments:[{name:'node',source:'usage_placeholder'}],options:[{name:'--all',datatype:'string'}],usage:['Usage: riak inspect [<node>] [--all]']})]);
 const syntax=ref.pages[0].syntax;
 assert.equal(syntax.basis,'supplied_usage');assert.equal(syntax.forms[0].text,'riak inspect [<node>] [--all]');
 assert.ok(syntax.review.generated[0].includes('<value?>'));assert.ok(syntax.review.issues.some(i=>i.includes('grouping')));
});
test('normalization ignores spacing and the documented riak-admin spelling',()=>{
 const syntax=build([shell('riak admin status',{usage:['  Usage: riak-admin   status\n']})]).pages[0].syntax;
 assert.equal(syntax.review.status,'matched');assert.deepEqual(syntax.review.issues,[]);
});
test('declared underscore aliases share canonical syntax without hiding argument differences',()=>{
 const ref=build([
  shell('riak admin aae-status',{aliases:[{invocation:'riak admin aae_status'}],usage:['Usage: riak admin aae-status']}),
  shell('riak admin aae_status',{aliases:[{invocation:'riak admin aae-status'}],usage:['Usage: riak admin aae_status']}),
  shell('riak admin repair-2i',{aliases:[{invocation:'riak admin repair_2i'}]}),
  shell('riak admin repair_2i',{aliases:[{invocation:'riak admin repair-2i'}]}),
  shell('riak admin repair-2i status',{usage:['Usage: riak admin repair-2i status [node_name]']}),
  shell('riak admin repair_2i status',{usage:['Usage: riak admin repair_2i status [node_name]']}),
  shell('riak console_clean',{usage:['Usage: riak console_clean']}),
 ]);
 const aae=ref.pages.find(p=>p.route==='riak/admin/aae-status');
 assert.deepEqual(aae.syntax.forms.map(f=>f.text),['riak admin aae-status']);
 assert.equal(aae.syntax.review.status,'matched');
 assert.ok(aae.aliases.includes('riak admin aae_status'));
 assert.ok(aae.syntax.review.supplied.some(s=>s.includes('aae_status')));
 const status=ref.pages.find(p=>p.route==='riak/admin/repair-2i/status');
 assert.deepEqual(status.syntax.forms.map(f=>f.text),['riak admin repair-2i status [node_name]']);
 assert.equal(status.syntax.basis,'supplied_usage');
 assert.ok(status.syntax.review.issues.some(i=>i.includes('node_name')));
 assert.equal(ref.pages.find(p=>p.route==='riak/console-clean').syntax.forms[0].text,'riak console_clean');
});
test('Clique help is a separate form without the execution arguments',()=>{
 const syntax=build([shell('riak describe',{
  arguments:[{name:'variable',required:true,repeatable:true}],
  global_options:[{name:'--help',short:'-h'}],usage:['Usage: riak describe <variable> ...'],
 })]).pages[0].syntax;
 assert.deepEqual(syntax.forms.map(f=>f.text),['riak describe <variable> ...','riak describe {--help|-h}']);
});
test('incomplete candidates without supplied usage never become displayed guesses',()=>{
 const syntax=build([shell('riak inspect',{options:[{name:'--unknown'}]})]).pages[0].syntax;
 assert.equal(syntax.forms[0].text,'riak inspect');assert.equal(syntax.review.displayed,'known_path_only');
 assert.ok(syntax.review.generated[0].includes('<value?>'));
});
test('editorial syntax is recorded without suppressing a source mismatch',()=>{
 const ref=build([shell('riak inspect',{usage:['Usage: riak inspect <missing>'],reference:{syntax:'```sh\nriak inspect custom\n```'}})]);
 const review=ref.pages[0].syntax.review;
 assert.equal(review.displayed,'editorial_override');assert.match(review.editorial,/custom/);
 assert.match(reviewMarkdown(ref.syntaxReview),/### Editorial syntax/);
 assert.ok(review.issues.some(i=>i.includes('Generated and supplied')));
});
test('a missing supplied form is flagged even when the generated path is complete',()=>{
 const ref=build([shell('riak inspect')]);
 assert.equal(ref.pages[0].syntax.forms[0].text,'riak inspect');
 assert.match(reviewMarkdown(ref.syntaxReview),/No supplied usage/);
});
test('a supplied argument absent from metadata is not silently removed from displayed syntax',()=>{
 const syntax=build([shell('riak inspect',{usage:['Usage: riak inspect NODE']})]).pages[0].syntax;
 assert.equal(syntax.forms[0].text,'riak inspect NODE');assert.equal(syntax.basis,'supplied_usage');
 assert.ok(syntax.review.issues.some(i=>i.includes('terms absent')&&i.includes('NODE')));
});
test('Erlang signatures remain structured AST-derived forms',()=>{
 const c={...shell('unused'),id:'erlang:riak_client:get/3',context:'erlang',kind:'erlang_function',module:'riak_client',function:'get',arity:3,signatures:['get(Bucket, Key, Client)']};
 const syntax=build([c]).pages[0].syntax;
 assert.equal(syntax.forms[0].text,'riak_client:get(Bucket, Key, Client).');assert.equal(syntax.basis,'erlang_ast');
});
test('deployed references preserve source metadata and every syntax link has a page or section',()=>{
 for(const version of ['3.4.0','3.4.1']){
  const doc=JSON.parse(fs.readFileSync(`content/openriak-kv/metadata/${version}/kv-cli-commands.json`));const before=JSON.stringify(doc);
  const ref=buildAnnotatedReference(doc);assert.equal(JSON.stringify(doc),before);
  const routes=new Set([...ref.pages,...ref.sections].map(p=>p.route));
  for(const page of ref.pages)for(const form of page.syntax.forms)for(const token of form.tokens)if(token.route){assert.ok(routes.has(token.route),token.route);assert.ok(token.route.startsWith(page.route+'/'),`${page.route} links to non-child ${token.route}`);}
  const admin=ref.pages.find(p=>p.route==='riak/admin');assert.ok(admin.syntax.review.onlyInProvided.includes('diag'));assert.ok(admin.syntax.review.missingFromProvided.includes('remove'));
  const root=ref.pages.find(p=>p.route==='riak');assert.equal(root.syntax.basis,'command_tree');
  assert.ok(root.syntax.forms[0].tokens.some(t=>t.route==='riak/admin'));
  for(const page of ref.pages.filter(p=>p.context==='shell'))for(const alias of page.aliases.filter(a=>a.includes('_')&&a!==page.title)){
   assert.ok(!page.syntax.forms.some(f=>f.text===alias||f.text.startsWith(alias+' ')),`${page.title}: repeated alias ${alias}`);
  }
  const describe=ref.pages.find(p=>p.route==='riak/admin/describe');assert.match(describe.syntax.forms[0].text,/\[--format \{csv\|human\|json\}\]/);
  assert.ok(admin.syntax.forms[0].tokens.some(t=>t.text==='node')===(version==='3.4.1'));
 }
});

test('AAE selectors show positional tuple fields and all ChangeMethod forms',()=>{
 for(const version of ['3.4.0','3.4.1']) {
  const ref=buildAnnotatedReference(JSON.parse(fs.readFileSync(`content/openriak-kv/metadata/${version}/kv-cli-commands.json`)));
  for(const name of ['erase-keys','reap-tombs']) {
   const page=ref.pages.find(p=>p.route===`erlang/riak-client/aae-fold/${name}`);
   assert.equal(page.syntax.forms.length,6);
   for(const method of ['count','local','{job, JobId}']) {
    assert.ok(page.syntax.forms.some(f=>f.text===`riak_client:aae_fold({${name.replaceAll('-','_')}, Bucket, KeyRange, SegmentFilter, ModifiedRange, ${method}}, Client).`));
   }
   assert.ok(page.syntax.review.issues.some(i=>i.includes('Generated and supplied syntax differ')));
  }
  const clocks=ref.pages.find(p=>p.route.endsWith('/fetch-clocks-nval'));
  assert.equal(clocks.syntax.forms.length,4);
  assert.ok(clocks.syntax.forms.some(f=>f.text==='riak_client:aae_fold({fetch_clocks_nval, NVal, Segments, ModifiedRange}, Client).'));
  for(const page of ref.pages.filter(p=>p.route.includes('/aae-fold/')))for(const f of page.syntax.forms) assert.ok(!f.text.includes('...'),f.text);
  const streams=ref.pages.find(p=>p.route==='erlang/riak-client/stream-list-keys');
  assert.ok(streams.syntax.forms.some(f=>f.text==='riak_client:stream_list_keys(Input, Timeout, Recipient, Client).'));
  assert.ok(!ref.pages.filter(p=>p.context==='erlang').flatMap(p=>p.syntax.forms).some(f=>f.text.includes('{riak_client,')));
 }
});
