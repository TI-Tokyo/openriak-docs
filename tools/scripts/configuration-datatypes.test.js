'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { datatypeAlternatives } = require('./configuration-datatypes');
const { configurationReference } = require('./configuration-reference');
const { annotateSettings } = require('./settings-annotations');
const value = value => ({kind:'value', value});
const type = value => ({kind:'type', value});

test('union alternatives distinguish literal atoms and numbers from unrestricted types', () => {
 assert.deepEqual(datatypeAlternatives("['integer', {'$erlang_tuple': ['atom', 'unlimited']} ]"),[type('Integer'),value('unlimited')]);
 assert.deepEqual(datatypeAlternatives("[{'$erlang_tuple': ['atom', 'unlimited']}, {'$erlang_tuple': ['duration', 'ms']}]"),[value('unlimited'),type('Duration (ms)')]);
 assert.deepEqual(datatypeAlternatives("[{'$erlang_tuple': ['integer', 0]}, {'$erlang_tuple': ['integer', -1]}]"),[value('0'),value('-1')]);
 assert.deepEqual(datatypeAlternatives("['atom', {'$erlang_tuple': ['enum', ['integer', 'atom']]}]"),[type('Atom'),value('integer'),value('atom')]);
 assert.deepEqual(datatypeAlternatives("['integer', 'flag']"),[type('Integer'),value('on'),value('off')]);
 assert.deepEqual(datatypeAlternatives("[{'$erlang_tuple': ['flag', 'enabled', 'disabled']}]"),[value('enabled'),value('disabled')]);
 assert.deepEqual(datatypeAlternatives("[{'$erlang_tuple': ['flag', {'$erlang_tuple': ['yes', 1]}, {'$erlang_tuple': ['no', 0]}]}]"),[value('yes'),value('no')]);
 assert.deepEqual(datatypeAlternatives('[{"$erlang_tuple": ["atom", "unlimited"]}, "integer", "integer"]'),[value('unlimited'),type('Integer')]);
});

test('datatype parsing handles quoted literals and rejects malformed expressions without evaluation', () => {
 assert.deepEqual(datatypeAlternatives("[{'$erlang_tuple': ['atom', 'can\\'t']}]"),[value("can't")]);
 for(const input of ["['integer'", "['integer'] + code()", '[process.exit()]', "[{'$erlang_tuple': ['unknown', 1]}]"]) {
  assert.throws(()=>datatypeAlternatives(input),/datatype/i);
 }
});

test('both releases resolve union choices and expose the reviewed schema validation limits', () => {
 for(const version of ['3.4.0','3.4.1']) {
  const document=require(`../../content/openriak-kv/metadata/${version}/kv-settings.json`);
  const reference=configurationReference({productId:'openriak-kv'},version,document,[]);
  const annotated=annotateSettings(reference,document);
  const byName=Object.fromEntries(annotated.settings.map(s=>[s.name,s]));
  for(const prefix of ['', 'multi_backend.$name.']) {
   assert.deepEqual(byName[prefix+'bitcask.fold.max_puts'].datatype.alternatives,[type('Integer'),value('unlimited')]);
   assert.deepEqual(byName[prefix+'bitcask.fold.max_age'].datatype.alternatives,[value('unlimited'),type('Duration (ms)')]);
   assert.deepEqual(byName[prefix+'leveldb.tiered'].datatype.alternatives,['off','1','2','3','4','5','6'].map(value));
  }
  assert.deepEqual(byName['object.format'].datatype.alternatives,[value('1'),value('0')]);
  assert.deepEqual(byName['anti_entropy.tree.expiry'].datatype.alternatives,[type('Duration (ms)'),value('never')]);
  assert.deepEqual(byName['buckets.default.r'].datatype.alternatives,[value('quorum'),value('all'),type('Integer')]);
  assert.deepEqual(byName['datatypes.compression_level'].datatype.alternatives,[type('Integer'),value('on'),value('off')]);
  assert.match(byName['datatypes.compression_level'].datatype.constraints.join(' '),/0 through 9 inclusive/);
  assert.match(byName.delete_mode.datatype.constraints.join(' '),/1 through 299999/);
  assert.equal(annotated.settings.filter(s=>s.datatype.label==='One of').length,31);
  assert.ok(annotated.settings.filter(s=>s.datatype.label==='One of').every(s=>s.datatype.alternatives.every(c=>c.value!=='Atom')));
 }
});
