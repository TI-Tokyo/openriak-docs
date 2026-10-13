'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {prepareTranscripts, compactSteps} = require('./cli-transcripts');

function fixture() {
  const long = Array.from({length: 80}, (_, i) => `module_${i} 3.4.1`).join('\n') + '\n';
  const evidence = {stdout: long, stderr: 'warning on stderr\n', exit_code: 0,
    verification: {case: 'ok', file: 'cli/status.json', repository_commit: 'abc123'},
    test_steps: [
      {phase: 'setup', argv: ['prepare'], stdout: 'ready\n', stderr: '', exit_code: 0},
      {phase: 'case_setup:ok', argv: ['configure', 'a b'], stdout: '', stderr: '', exit_code: 0},
      {phase: 'case:ok', argv: ['riak', 'status'], stdout: long, stderr: 'warning on stderr\n', exit_code: 0},
      {phase: 'verify:ok', argv: ['check'], stdout: 'verified\n', stderr: '', exit_code: 0},
    ]};
  return {pages: [{key: 'shell:riak status', availability: 'available', context: 'shell', reference: {
    examples: [{id: 'scenario:bad', title: 'Rejected', invocation: 'riak invalid', outcome: 'error', observed: {...evidence, test_steps: []}},
      {id: 'scenario:ok', title: 'Status', invocation: 'riak status', outcome: 'success', observed: evidence}],
    errors: [{id: 'bad', example_id: 'scenario:bad'}],
  }}], annotationCoverage: {commands: [{key: 'shell:riak status'}]}};
}
const document = {runtime: {os_release: 'PRETTY_NAME="Alpine Linux v3.24"\nVERSION_ID=3.24.1\n', otp_release: '26'}};

test('expected results select verified success and preserve every byte on both streams', () => {
  const reference = fixture();
  prepareTranscripts(reference, document, x => x);
  const content = reference.pages[0].reference;
  assert.equal(content.knownGood.id, 'scenario:ok');
  assert.equal(content.knownGood.steps[1].stdout, content.knownGood.observed.stdout);
  assert.equal(content.knownGood.steps[1].stderr, 'warning on stderr\n');
  assert.match(content.knownGood.steps[1].stdout, /module_79 3\.4\.1\n$/);
  assert.equal(content.knownGood.environment_steps.length, 1);
  assert.deepEqual(content.knownGood.steps.map(s => s.purpose), ['Prepare the example', 'Run the command', 'Verify the result']);
  assert.equal(content.knownGood.steps[0].invocation, "configure 'a b'");
  assert.equal(content.knownGood.recipe_url, 'https://github.com/TI-Tokyo/openriak-metadata/blob/abc123/scenarios/cli/status.json');
  assert.deepEqual(content.errors[0].example, {number: 1, title: 'Rejected', anchor: 'example-1'});
  assert.equal(reference.testEnvironment.osVersion, '3.24.1');
});

test('a zero exit status never promotes a rejected or unverified example to known good', () => {
  for (const mode of ['error', 'unverified', 'known_issue']) {
    const reference = fixture(), content = reference.pages[0].reference;
    if (mode === 'error') content.examples[1].outcome = 'error';
    if (mode === 'unverified') delete content.examples[1].observed;
    if (mode === 'known_issue') content.examples[1].observed.known_issue = true;
    prepareTranscripts(reference, document, x => x);
    assert.equal(content.knownGood, undefined, mode);
  }
  const reference = fixture();
  reference.pages[0].reference.known_good_example = 'scenario:bad';
  assert.throws(() => prepareTranscripts(reference, document, x => x), /verified success/);
});

test('unlinked errors and missing output remain explicit coverage gaps', () => {
  const reference = fixture(), content = reference.pages[0].reference;
  content.errors.push({id: 'unexplained'});
  content.examples.push({id: 'manual', title: 'Manual', invocation: 'riak status'});
  prepareTranscripts(reference, document, x => x);
  assert.deepEqual(reference.annotationCoverage.commands[0].errors_without_examples, ['unexplained']);
  assert.deepEqual(reference.annotationCoverage.commands[0].examples_without_output, ['manual']);
});

test('removed commands prefer the verified limitation over an argument usage error', () => {
  const reference = fixture(), page = reference.pages[0];
  page.availability = 'removed';
  page.reference.examples[1].outcome = 'error';
  page.reference.examples[1].observed.known_issue = true;
  prepareTranscripts(reference, document, x => x);
  assert.equal(page.reference.knownFailure.id, 'scenario:ok');
  assert.equal(page.reference.knownGood, undefined);
});

test('every 3.4.1 command has a verified outcome, every displayed error an example', () => {
  const {buildAnnotatedReference} = require('./cli-annotations');
  const raw = require('../../content/openriak-kv/metadata/3.4.1/kv-cli-commands.json');
  const reference = buildAnnotatedReference(raw);
  for (const page of reference.pages) {
    assert.ok(page.reference.knownGood || page.reference.knownFailure, page.key);
    assert.ok(page.reference.examples.every(e => e.observed && e.steps.length), `${page.key}: output`);
    assert.ok(page.reference.errors.every(e => e.example), `${page.key}: error examples`);
  }
});


test('CLI polling shows the first pending and final complete observations, preserving raw evidence', () => {
  const reference = fixture(), example = reference.pages[0].reference.examples[1];
  const retry = {attempts:60, interval_seconds:3};
  const records = Array.from({length:20}, (_, i) => ({phase:'verify:ok', node:1,
    argv:['riak','admin','ringready'], stdout:i === 19 ? 'TRUE ready\n' : `FALSE waiting ${i}\n`,
    stderr:i === 0 ? 'warning\n' : '', exit_code:0, failures:i === 19 ? [] : ['not ready'],
    retry, attempt:i+1, description:'Wait for ring agreement.'}));
  example.observed.test_steps = records;
  prepareTranscripts(reference, document, x => x);
  assert.equal(example.steps.length, 1);
  assert.equal(example.steps[0].invocation, 'riak admin ringready');
  assert.deepEqual(example.steps[0].observations.map(o => o.label), ['While waiting', 'When complete']);
  assert.equal(example.steps[0].observations[0].stderr, 'warning\n');
  assert.equal(example.steps[0].observations[1].stdout, 'TRUE ready\n');
  assert.equal(example.steps[0].attempt_count, 20);
  assert.equal(example.observed.test_steps, records);
  assert.equal(records.length, 20);
});

test('waits never combine nodes, independent loops, or phases, and never invent a pending result', () => {
  const base = {phase:'verify:ok', node:1, argv:['check'], retry:{attempts:3, interval_seconds:1}, failures:[], attempt:1};
  assert.equal(compactSteps([base, base]).length, 2);
  assert.equal(compactSteps([base, {...base, node:2, attempt:2}]).length, 2);
  assert.equal(compactSteps([base, {...base, phase:'setup', attempt:2}]).length, 2);
  assert.deepEqual(compactSteps([base])[0].observations.map(o => o.label), ['When complete']);
  assert.match(compactSteps([{...base, failures:['not ready']}])[0].observations[0].label, /Retry limit reached/);
});

test('HTTP fixture requests share one numbered step with separate command lines and complete output', () => {
  const reference = fixture(), example = reference.pages[0].reference.examples[1];
  example.observed.test_steps = [{phase:'verify:ok', requests:[{argv:['curl','http://localhost:8098/one']},
    {argv:['curl','http://localhost:8098/two']}], stdout:'one\ntwo\n', stderr:'warning\n', exit_code:0}];
  prepareTranscripts(reference, document, x => x);
  assert.equal(example.steps.length, 1);
  assert.equal(example.steps[0].invocation, 'curl http://localhost:8098/one\ncurl http://localhost:8098/two');
  assert.equal(example.steps[0].stdout, 'one\ntwo\n');
});
