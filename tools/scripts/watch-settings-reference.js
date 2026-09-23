#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { configurationReference } = require('./configuration-reference');
const { defaultsByOs } = require('./defaults-by-os');
const { annotateSettings, defaultSettingsRoot } = require('./settings-annotations');
const { annotationFiles } = require('./cli-annotation-markdown');
const repository = path.resolve(__dirname, '../..');
function watchSettings({outputRoot = path.join(repository, 'tools/generated'), once = false,
  inputRoot = path.join(repository, 'content/openriak-kv/metadata'), overrideRoot = defaultSettingsRoot, intervalMs = 1000} = {}) {
  const stamps = new Map();
  const tick = () => {
    for (const version of fs.readdirSync(inputRoot).filter(v => /^\d+\.\d+\.\d+$/.test(v))) {
      const source = path.join(inputRoot, version, 'kv-settings.json');
      const supported = path.join(inputRoot, version, 'kv-supported-os.json');
      const versionFile = path.join(outputRoot, 'openriak-kv/data/versions', `${version}.json`);
      if (![source, supported, versionFile].every(file => fs.existsSync(file))) continue;
      const files = [source, supported, versionFile, ...annotationFiles(overrideRoot, version)];
      const stamp = files.map(file => `${file}:${fs.statSync(file).mtimeMs}:${fs.statSync(file).size}`).join('|');
      if (stamps.get(version) === stamp) continue;
      try {
        const document = JSON.parse(fs.readFileSync(source, 'utf8'));
        const targets = JSON.parse(fs.readFileSync(supported, 'utf8')).operating_systems;
        const operatingSystems = JSON.parse(fs.readFileSync(versionFile, 'utf8')).operatingSystems;
        const reference = annotateSettings(configurationReference({productId: 'openriak-kv'}, version,
          {...document, effective_defaults: defaultsByOs(document, targets)}, operatingSystems), document, {overrideRoot});
        // Lazy import avoids a cycle when the combined CLI watcher starts this one.
        const { writeChanged } = require('./watch-cli-reference');
        writeChanged(path.join(outputRoot, 'openriak-kv/data/configuration-reference', `${version}.json`), JSON.stringify(reference, null, 2) + '\n');
        writeChanged(path.join(outputRoot, 'openriak-kv/settings-coverage', `${version}.json`), JSON.stringify(reference.annotationCoverage, null, 2) + '\n');
        console.log(`Settings ${version}: ${reference.annotationCoverage.complete}/${reference.annotationCoverage.total} annotated; ${reference.annotationCoverage.issues.length} review issues.`);
      } catch (error) {
        if (once) throw error;
        console.error(`Settings ${version}: ${error.message}; keeping the last valid preview.`);
      }
      stamps.set(version, stamp);
    }
  };
  tick();
  return once ? null : setInterval(tick, intervalMs);
}
module.exports = { watchSettings };
