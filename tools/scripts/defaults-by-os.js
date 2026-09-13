'use strict';

const { isDeepStrictEqual } = require('node:util');

// Defaults schema 2 shares one map across all releases/architectures of an OS.
// Read older metadata too, but never silently collapse conflicting values.
const defaultsByOs = (document, targets) => {
  if (document.schema_version === 2 && document.defaults_scope === 'os') {
    return document.effective_defaults || {};
  }
  if (document.schema_version !== 1) throw new Error('Unsupported defaults metadata schema');
  const result = {};
  for (const target of targets) {
    const values = document.effective_defaults?.[target.id];
    if (!values) continue;
    if (result[target.family] && !isDeepStrictEqual(result[target.family], values)) {
      throw new Error(`Conflicting defaults for OS ${target.family}: ${target.id}`);
    }
    result[target.family] = values;
  }
  return result;
};

module.exports = { defaultsByOs };
