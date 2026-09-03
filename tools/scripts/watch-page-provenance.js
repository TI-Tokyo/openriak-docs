'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { generatePageProvenance, productSources } = require('./generate-version-mounts.js');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const defaults = {
  contentRoot: path.join(repositoryRoot, 'content'),
  outputRoot: path.join(repositoryRoot, 'tools', 'generated', 'page-provenance'),
  debounceMs: 180
};

const parseArguments = (argumentsList) => {
  const options = { ...defaults };
  for (let index = 0; index < argumentsList.length; index += 1) {
    const argument = argumentsList[index];
    if (argument === '--content-root') options.contentRoot = path.resolve(argumentsList[++index]);
    else if (argument === '--page-provenance-root') options.outputRoot = path.resolve(argumentsList[++index]);
    else if (argument === '--debounce-ms') options.debounceMs = Number(argumentsList[++index]);
    else throw new Error(`Unknown argument: ${argument}`);
  }
  if (!Number.isFinite(options.debounceMs) || options.debounceMs < 0) {
    throw new Error('--debounce-ms must be a non-negative number');
  }
  return options;
};

const isRelevantChange = (eventType, filename) => (
  eventType === 'rename' || !filename || String(filename).toLowerCase().endsWith('.md')
);

const watchPageProvenance = ({ contentRoot, outputRoot, debounceMs }) => {
  let timer = null;
  let running = false;
  let pending = false;

  const regenerate = () => {
    timer = null;
    if (running) {
      pending = true;
      return;
    }
    running = true;
    try {
      generatePageProvenance(contentRoot, productSources, outputRoot);
      console.log('Regenerated page provenance after a Markdown content change.');
    } catch (error) {
      console.error(`Unable to regenerate page provenance: ${error.message}`);
    } finally {
      running = false;
      if (pending) {
        pending = false;
        timer = setTimeout(regenerate, debounceMs);
      }
    }
  };

  const schedule = () => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(regenerate, debounceMs);
  };
  const watcher = fs.watch(contentRoot, { recursive: true }, (eventType, filename) => {
    if (isRelevantChange(eventType, filename)) schedule();
  });
  watcher.on('error', (error) => console.error(`Page-provenance watcher failed: ${error.message}`));
  return watcher;
};

if (require.main === module) {
  try {
    const options = parseArguments(process.argv.slice(2));
    watchPageProvenance(options);
    console.log(`Watching ${options.contentRoot} for Markdown changes.`);
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}

module.exports = { isRelevantChange, parseArguments, watchPageProvenance };
