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
  const describe=ref.pages.find(p=>p.route==='riak/admin/describe');assert.match(describe.syntax.forms[0].text,/\[--format \{csv\|human\|json\}\]/);
  assert.ok(admin.syntax.forms[0].tokens.some(t=>t.text==='node')===(version==='3.4.1'));
 }
});
