#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function getFileContent(filePath) {
  // Check that the file exists
  if (!doesFileExist(filePath)) {
    console.error(`❌ Error: File not found at "${filePath}"`);
    process.exit(1);
  }

  try {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    return fileContent;
  } catch (err) {
    console.error(`❌ Error: Failed to load text from "${filePath}":`, err.message);
    process.exit(1);
  }
}

function setFileContent(filePath, content) {
  try {
    // ensure folder exists
    const dir = getParentFolder(filePath);
    // save file
    fs.writeFileSync(filePath, content, 'utf8');
  } catch (err) {
    console.error(`❌ File system error: Failed to write text as utf8 to "${filePath}":`, err.message);
    process.exit(1);
  }
}

function doesFileExist(filePath) {
  return fs.existsSync(filePath);
}

function ensureFolderExists(folderPath) {
  try {
    fs.mkdirSync(folderPath, { recursive: true });
  } catch (err) {
    console.error(`❌ File system error: Failed to check or create folder "${folderPath}": `, err.message)
    process.exit(1);
  }
}

function getParentFolder(folderPath) {
  const parentPath = path.dirname(folderPath);
  ensureFolderExists(parentPath);
  return parentPath;
}

function forFiles(folderPath, func) {
  const files = fs.readdirSync(folderPath);
  files.forEach((file) => {
    const fullPath = path.join(folderPath, file);
    const stat = fs.statSync(fullPath);
    return func({
      name: file,
      baseName: path.basename(file, path.extname(file)),
      extension: path.extname(file),
      fullPath: fullPath,
      parentPath: path.dirname(fullPath),
      size: stat.size,
      isFile: stat.isFile(fullPath),
      isDirectory: stat.isDirectory(fullPath),
      //stat: stat,
    });
  });
}

function join(...args) {
  return path.join(...args);
}

function resolve(relativePath) {
  const fullPath = path.resolve(relativePath);
  return fullPath;
}

function relative(from, to) {
  const relativePath = path.relative(from, to);
  return relativePath;
}


module.exports = {
  getParentFolder,
  ensureFolderExists,
  doesFileExist,
  setFileContent,
  getFileContent,
  forFiles,
  join,
  resolve,
  relative
};

