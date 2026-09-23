#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { buildAnnotatedReference, defaultOverrideRoot, annotationFiles } = require('./cli-annotations');
const { reviewMarkdown } = require('./cli-syntax');
const repository = path.resolve(__dirname, '../..');
const metadataRoot = path.join(repository, 'content/openriak-kv/metadata');
function writeChanged(file, content) {
  if (fs.existsSync(file) && fs.readFileSync(file, 'utf8') === content) return;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const temporary = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(temporary, content);
  fs.renameSync(temporary, file);
}
function watch({outputRoot = path.join(repository, 'tools/generated'), once = false,
  inputRoot = metadataRoot, overrideRoot = defaultOverrideRoot, intervalMs = 1000} = {}) {
  const stamps = new Map();
  const tick = () => {
    for (const version of fs.readdirSync(inputRoot).filter(v => /^\d+\.\d+\.\d+$/.test(v))) {
      const file = path.join(inputRoot, version, 'kv-cli-commands.json');
      if (!fs.existsSync(file)) continue;
      const files = [file, ...annotationFiles(overrideRoot, version).filter(file => path.relative(overrideRoot, file).split(path.sep)[0] !== 'settings')];
      const stamp = files.map(file => fs.existsSync(file) ? `${file}:${fs.statSync(file).mtimeMs}:${fs.statSync(file).size}` : file + ':missing').join('|');
      if (stamps.get(version) === stamp) continue;
      try {
        const reference = buildAnnotatedReference(JSON.parse(fs.readFileSync(file, 'utf8')), { overrideRoot });
        writeChanged(path.join(outputRoot, 'openriak-kv/data/cli-reference', `${version}.json`), JSON.stringify(reference, null, 2) + '\n');
        writeChanged(path.join(outputRoot, 'openriak-kv/cli-coverage', `${version}.json`), JSON.stringify(reference.annotationCoverage, null, 2) + '\n');
        writeChanged(path.join(outputRoot, 'openriak-kv/cli-syntax-review', `${version}.json`), JSON.stringify(reference.syntaxReview, null, 2) + '\n');
        writeChanged(path.join(outputRoot, 'openriak-kv/cli-syntax-review', `${version}.md`), reviewMarkdown(reference.syntaxReview));
        console.log(`CLI ${version}: ${reference.annotationCoverage.complete}/${reference.annotationCoverage.total} topics have examples, results and errors; ${reference.annotationCoverage.issues.length} review issues.`);
        console.log(`CLI ${version}: ${reference.syntaxReview.needsReview}/${reference.syntaxReview.total} syntax topics need manual review.`);
      } catch (error) {
        if (once) throw error;
        console.error(`CLI ${version}: ${error.message}; keeping the last valid preview.`);
      }
      stamps.set(version, stamp);
    }
  };
  tick();
  return once ? null : setInterval(tick, intervalMs);
}
module.exports = { watch, writeChanged };
if (require.main === module) {
  try {
    const args = process.argv.slice(2), options = {};
    for (let i=0; i<args.length; i++) {
      if (args[i] === '--output-root' && args[i+1]) options.outputRoot = path.resolve(args[++i]);
      else if (args[i] === '--once') options.once = true;
      else if (['-h','--help'].includes(args[i])) {console.log('Usage: node tools/scripts/watch-cli-reference.js [--output-root DIRECTORY] [--once]\nMerge deployed CLI/settings metadata and docs annotations. Without --once, poll changes every second.');process.exit(0);}
      else throw new Error('Unknown argument: ' + args[i]);
    }
    watch(options);
    require('./watch-settings-reference').watchSettings(options);
  } catch(error) {console.error(error.message);process.exitCode=1;}
}
