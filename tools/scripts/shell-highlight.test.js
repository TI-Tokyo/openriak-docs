'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

const source = fs.readFileSync(path.join(__dirname, '../../layouts/docs-theme/static/js/page-tools.js'), 'utf8');
const helpers = source.slice(source.indexOf('  const shellCommentIndex ='), source.indexOf('  const highlightShellCode ='));

for (const line of [
  'LOW=$(date -u +%s)',
  'HIGH=$(date -u +%s)',
  'echo $((1 + 2))',
  'echo $',
  'echo ${unfinished',
  'echo $: $$ $? $HOME ${HOME}',
  'echo "$(date)" && printf \'%s\' "$HOME" # comment',
]) {
  test(`shell highlighting terminates and preserves: ${line}`, () => {
    const tokens = [];
    const context = vm.createContext({
      document: {
        createElement: () => ({ textContent: '' }),
        createTextNode: textContent => ({ textContent }),
      },
      content: {
        replaceChildren: () => { tokens.length = 0; },
        append: token => tokens.push(token),
      },
      line,
    });
    vm.runInContext(`(() => { ${helpers}\n highlightShellLine(content, line); })()`, context, { timeout: 1000 });
    assert.equal(tokens.map(token => token.textContent).join(''), line);
  });
}
