'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {prepareTranscripts} = require('./cli-transcripts');

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
