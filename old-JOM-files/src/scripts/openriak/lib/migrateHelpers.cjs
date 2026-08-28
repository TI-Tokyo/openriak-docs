#!/usr/bin/env node

const { getFileContent, setFileContent, doesFileExist, ensureFolderExists } = require('./fileHelpers.cjs');
const path = require('path');
const matter = require('gray-matter');

function getDestinationPath(project, version) {
  const destinationRoot = path.join(`${project}_versioned_docs`, `version-${version}`);
  // Ensure folder exists
  ensureFolderExists(destinationRoot);
  return destinationRoot;
}

function getMarkdown(filePath) {
  var raw = getFileContent(filePath).trimStart();

  raw = raw.replace(
    `version_history:\n  in: "2.0.0-2.9999.9999"\n`,
    ``
  );

  const parsed = matter(raw);

  return parsed;
}

module.exports = { 
  getDestinationPath, getMarkdown
};
