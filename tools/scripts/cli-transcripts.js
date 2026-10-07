'use strict';

const quote = value => /^[a-zA-Z0-9_@%+=:,./-]+$/.test(value) ? value : "'" + value.replace(/'/g, "'\"'\"'") + "'";
function invocation(argv) { return argv.map(quote).join(' '); }

function prepareTranscripts(reference, document, displayShellInvocation) {
  const os = document.runtime?.os_release || '';
  reference.testEnvironment = {
    os: os.match(/^NAME="?([^"\n]+)"?$/m)?.[1] || os.match(/^PRETTY_NAME="?([^"\n]+)"?$/m)?.[1] || 'Recorded runtime',
    osVersion: os.match(/^VERSION_ID="?([^"\n]+)"?$/m)?.[1] || '',
    otp: document.runtime?.otp_release || '',
    image: document.runtime?.tag || '',
  };
  for (const page of reference.pages) {
    const content = page.reference;
    content.examples.forEach((example, index) => {
      example.number = index + 1;
      example.anchor = `example-${example.number}`;
      if (!example.observed) return;
      const observed = example.observed;
      const casePhase = `case:${observed.verification.case}`;
      const steps = observed.test_steps || [];
      example.steps = steps.filter(s => s.phase !== 'setup').map(step => ({
        ...step,
        invocation: step.phase === casePhase ? (example.display_invocation || example.invocation) : displayShellInvocation(invocation(step.argv)),
        language: step.phase === casePhase && page.context === 'erlang' ? 'erlang' : 'sh',
        purpose: step.phase.startsWith('case_setup:') ? 'Prepare the example' : step.phase.startsWith('verify:') ? 'Verify the result' : 'Run the command',
      }));
      if (!example.steps.length) example.steps = [{invocation: example.display_invocation || example.invocation,
        language: page.context === 'erlang' ? 'erlang' : 'sh', purpose: 'Run the command',
        stdout: observed.stdout, stderr: observed.stderr, exit_code: observed.exit_code}];
      example.environment_steps = steps.filter(s => s.phase === 'setup').map(s => ({...s,
        invocation: displayShellInvocation(invocation(s.argv)), language: 'sh', purpose: 'Prepare the environment'}));
      example.recipe_url = 'https://github.com/TI-Tokyo/openriak-metadata/blob/' +
        (observed.verification.repository_commit || 'main') + '/scenarios/' +
        (observed.verification.file || '').split('/').map(encodeURIComponent).join('/');
    });
    const successful = content.examples.filter(e => e.outcome === 'success' && e.observed && !e.observed.known_issue);
    content.knownFailure = content.examples.find(e => e.observed?.known_issue) ||
      content.examples.find(e => e.observed && page.availability !== 'available');
    content.knownGood = content.known_good_example ? successful.find(e => e.id === content.known_good_example) :
      successful.find(e => !/(?:^|\s)(?:--help|help)(?:\s|$)/.test(e.invocation)) ||
      ((!content.knownFailure || page.children?.length) ? successful[0] : undefined);
    if (content.known_good_example && !content.knownGood) throw new Error(`${page.key}: known good example must identify a verified success`);
    for (const error of content.errors) {
      const example = content.examples.find(e => e.id === (error.example_id || error.id));
      if (example) error.example = {number: example.number, title: example.title, anchor: example.anchor};
    }
    const coverage = reference.annotationCoverage.commands.find(c => c.key === page.key);
    coverage.known_good = content.knownGood?.id || null;
    coverage.errors_without_examples = content.errors.filter(e => !e.example).map(e => e.id);
    coverage.examples_without_output = content.examples.filter(e => !e.observed).map(e => e.id);
  }
  return reference;
}
module.exports = {prepareTranscripts, invocation};
