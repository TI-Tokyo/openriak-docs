#!/usr/bin/env node

const path = require('path');
const request = require('sync-request');
const { setFileContent } = require('./fileHelpers.cjs');

function convertGithubToRawUrl(url) {
  const match = url.match(/^https:\/\/github\.com\/([^/]+)\/([^/]+)\/blob\/([^/]+)\/(.+)$/);
  if (!match) {
    throw new Error(`❌ Error: Invalid GitHub blob URL format: ${url}`);
  }

  const [, owner, repo, ref, filePath] = match;
  return `https://raw.githubusercontent.com/${owner}/${repo}/${ref}/${filePath}`;
}

function downloadFile(url, savePath) {
  //console.log(`ℹ️  Save url "${url}" to file "${savePath}"`);
  try {
    const res = request('GET', url, { timeout: 10000 }); // timeout in ms
    if (res.statusCode === 200) {
      setFileContent(savePath, res.getBody());
      //console.log(`✅ Downloaded and saved to ${savePath}`);
    } else {
      console.error(`❌ Server responded with a failure to download file "${url}": HTTP ${res.statusCode}`);
      process.exit(1);
    }
  } catch (err) {
    console.error(`❌ Failed to download file: ${err.message}`);
    process.exit(1);
  }
}

module.exports = { downloadFile, convertGithubToRawUrl };
