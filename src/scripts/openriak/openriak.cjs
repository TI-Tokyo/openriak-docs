#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const request = require('sync-request');
//const { Console } = require('console');

const commands = {
  updateSchemas: {
    description: 'Updates the Cuttlefish schemas files for a project, either for all versions or a specific version.',
    usage: 'updateSchemas <project> [version]',
    example: '"updateSchemas kv 1.0.0" will update schema files for OpenRiak KV version 1.0.0.'
  },
  help: {
    description: 'Show usage information',
    usage: 'help',
    example: '"updateSchemas help" will show this help summary.'
  }
};

function printUsage() {
  console.log('Usage: npm run openriak <command> [options]\n');
  console.log('Commands:');
  for (const [cmd, info] of Object.entries(commands)) {
    console.log(`  ${cmd.padEnd(10)} ${info.description}`);
    console.log(`    Usage:   ${info.usage}`);
    if (info.example) {
      console.log(`    Example: ${info.example}`);
    }
  }
}

function main() {
  const [, , command, ...args] = process.argv;

  if (!command || command === 'help') {
    printUsage();
    process.exit(0);
  }

  if (!commands[command]) {
    console.error(`❌ Unknown command: "${command}"\n`);
    printUsage();
    process.exit(1);
  }

  // Dispatch command
  switch (command) {
    case 'updateSchemas':
      if (args.length === 0 || args.length > 2) {
        console.error(`❌ Please provide only the project and optional version.\n`);
        console.log(`Usage: ${commands.updateSchemas.usage}`);
        process.exit(1);
      }
      const project = args[0];
      const version = (args.length === 2)?args[1]:null;
      if (!project) {
        console.error(`❌ Missing required <project> for updateSchema.\n`);
        console.log(`Usage: ${commands.updateSchemas.usage}`);
        process.exit(1);
      }
      var message = `Updating Schemas for project "${project}"`;
      if (version) {
        message += ` version "${version}"`;
      }
      message += `...`;
      console.log(message);
      // TODO
      updateSchemas(project, version);
      break;

    default:
      console.error(`❌ Command handler not implemented.`);
      process.exit(1);
  }
}

function getFileContent(path) {
  // Check that the file exists
  if (!fs.existsSync(path)) {
    console.error(`❌ Error: File not found at "${path}"`);
    process.exit(1);
  }

  try {
    const fileContent = fs.readFileSync(path, 'utf8');
    return fileContent;
  } catch (err) {
    console.error(`❌ Error: Failed to load text from "${path}":`, err.message);
    process.exit(1);
  }
}

function updateSchemas(project, version) {

  const schemaRoot = path.join('cached-data', 'schemas', project);
  const schemaPath = path.join(schemaRoot, 'schemas.json');

  // Ensure folder exists
  if (!fs.existsSync(schemaRoot)) {
    fs.mkdirSync(schemaRoot, { recursive: true });
  }

  // Check that the file exists
  if (!fs.existsSync(schemaPath)) {
    console.error(`❌ Error: Schema file not found for project "${project}" at "${schemaPath}"`);
    process.exit(1);
  }

  // Load the file as a JSON object
  let schemas;
  try {
    const fileContent = getFileContent(schemaPath);
    schemas = JSON.parse(fileContent);
  } catch (err) {
    console.error(`❌ Error: Failed to load or parse JSON file for project "${project}" at "${schemaPath}":`, err.message);
    process.exit(1);
  }

  // Check that "versions" exists and is an object
  if (!schemas.versions || typeof schemas.versions !== 'object') {
    console.error(`❌ Error: The "versions" property is missing or invalid in the schema file.`);
    process.exit(1);
  }

  // If a version was provided, validate that it exists
  if (version && !(version in schemas.versions)) {
    console.error(`❌ Error: Specified version "${version}" for project "${project}" not found in available schema versions in "${schemaPath}".`);
    console.error(`Available versions:`, Object.keys(schemas.versions).join(', '));
    process.exit(1);
  }

  // Get the root config and lock files
  const defaultRebarConfigFile = schemas.defaultRebarConfigFile;
  const defaultRebarLockFile = schemas.defaultRebarLockFile;  

  // Optional: check they exist
  if (!defaultRebarConfigFile || !defaultRebarLockFile) {
    console.error('❌ Error: Missing "defaultRebarConfigFile" or "defaultRebarLockFile" in schema file.');
    process.exit(1);
  }

  // Loop over the versions to update
  var versionsToUpdate = {};
  if (version) {
    versionsToUpdate[version] = schemas.versions[version];
  } else {
    versionsToUpdate = schemas.versions;
  }

  for (const [version, object] of Object.entries(versionsToUpdate)) {
    const versionRoot = path.join(schemaRoot, version);

    // Ensure folder exists
    if (!fs.existsSync(versionRoot)) {
      fs.mkdirSync(versionRoot, { recursive: true });
    }

    const versionTagOrCommit = object.tagOrCommit || version;
    console.log(`ℹ️  Checking schema for "${project}" version "${version}" using tag or commit name "${versionTagOrCommit}":`);

    const versionRebarConfigFile  = object.rebarConfigFile || defaultRebarConfigFile;
    const versionRebarLockFile    = object.rebarLockFile   || defaultRebarLockFile;
    
    const actualRebarConfigFile = versionRebarConfigFile.replace('{versionTagOrCommit}', versionTagOrCommit);
    const actualRebarLockFile   = versionRebarLockFile.replace('{versionTagOrCommit}', versionTagOrCommit  );

    const actualRebarConfigFileRaw = convertGithubToRawUrl(actualRebarConfigFile);
    const actualRebarLockFileRaw   = convertGithubToRawUrl(actualRebarLockFile  );

    console.log('ℹ️  Resolved rebar.config path:', actualRebarConfigFileRaw);
    console.log('ℹ️  Resolved rebar.lock path:  ', actualRebarLockFileRaw  );

    const rebarConfigDestPath = path.join(versionRoot, 'rebar.config');
    const rebarLockDestPath   = path.join(versionRoot, 'rebar.lock'  );
  
    downloadFile(actualRebarConfigFileRaw, rebarConfigDestPath);
    downloadFile(actualRebarLockFileRaw,   rebarLockDestPath  );

    const cuttlefishConfig = getRebarConfSectionFromFile(rebarConfigDestPath, "cuttlefish");
    const desiredSchemas = cuttlefishConfig["schema_order"];
    //console.log(`ℹ️  Desired schemas: `, desiredSchemas);

    const rebarLockFileContent = getFileContent(rebarLockDestPath);
    const rebarLockSections = getRebarLockSections(rebarLockFileContent);
    //console.log(`ℹ️  Loaded rebar.lock sections: `, rebarLockSections);

    var versionRepoMappings = object.schemaToRepoMappings || {};
    for (const [schemaName, repoInfo] of Object.entries(schemas.defaultSchemaToRepoMappings)) {
      if (!(schemaName in versionRepoMappings)) {
        // clone the info
        versionRepoMappings[schemaName] = { ...repoInfo };
      }
    }

    var unfoundRepos = false;
    desiredSchemas.forEach((schemaName, index) => {
      //console.log(`ℹ️  Finding "${schemaName}" at index ${index}.`);
      const repoInfo = versionRepoMappings[schemaName];
      if (!repoInfo) {
        console.log(`❌ Unable to find "${schemaName}" at position ${index} in schemaToRepoMappings for version "${version}".`);
        unfoundRepos = true;
      } else if (repoInfo.repoUrl) {
        repoInfo.tagOrCommit = versionTagOrCommit;
        console.log(`ℹ️  Using "${repoInfo.repo}" with tagOrCommit "${repoInfo.tagOrCommit}" for schema "${schemaName}".`);
      } else if (repoInfo.repo in rebarLockSections) {
        repoInfo.repoUrl = rebarLockSections[repoInfo.repo].url;
        repoInfo.tagOrCommit = rebarLockSections[repoInfo.repo].tagOrCommit;
        console.log(`ℹ️  Using "${repoInfo.repo}" with tagOrCommit "${repoInfo.tagOrCommit}" for schema "${schemaName}".`);
      } else {
        console.log(`❌ Unable to find repo for schema"${schemaName}".`);
        unfoundRepos = true;
      }
    });
    if (unfoundRepos) {
      console.log(`❌ Unable to find repos for all schemas.`);
      process.exit(1);
    }

    desiredSchemas.forEach((schemaName, index) => {
      const repoInfo = versionRepoMappings[schemaName];
      // remove ".git" and any trailing slash if present from the repo url
      const repoUrl = repoInfo.repoUrl.replace(/(\.git)?\/?$/, '');
      const fileUrl = repoInfo.fileUrl.replace('{tagOrCommit}', repoInfo.tagOrCommit);
      const fullUrl = `${repoUrl}/blob${fileUrl}`;
      const rawUrl = convertGithubToRawUrl(fullUrl);
      const savePath = path.join(versionRoot, `${schemaName}.schema`);
      downloadFile(rawUrl, savePath);
    });
  }
}

function getRebarLockSections(rebarLockContent) {
  // Match blocks like: {<<"bitcask">>, {git,"https://...", {ref,"..."}} , 1}
  const blockRegex = /\{\s*<<\"([^\"]+)\"\>>,\s*\{\s*git\s*,\s*\"([^\"]+)\"\s*,\s*\{\s*ref\s*,\s*\"([^\"]+)\"\s*\}\s*\}\s*,\s*\d+\s*\}/g;

  const results = {};
  let match;

  while ((match = blockRegex.exec(rebarLockContent)) !== null) {
    const name = match[1];            // bitcask
    const url = match[2];             // https://github.com/...
    const tagOrCommit = match[3];     // 1fcc4fb...

    results[name] = {
      sourceType: "git",
      url,
      tagOrCommit,
    };
  }
  return results;
}

function convertGithubToRawUrl(url) {
  const match = url.match(/^https:\/\/github\.com\/([^/]+)\/([^/]+)\/blob\/([^/]+)\/(.+)$/);
  if (!match) {
    throw new Error(`❌ Error: Invalid GitHub blob URL format: ${url}`);
  }

  const [, owner, repo, ref, filePath] = match;
  return `https://raw.githubusercontent.com/${owner}/${repo}/${ref}/${filePath}`;
}

/**
 * Returns a JavaScript object from a key-value tuple pair 
 * in a named section of an Erlang file.
 * 
 * @param {string} path The path to the source file
 * @param {string} sectionName The name of the section to extract.
 * @returns 
 */
function getRebarConfSectionFromFile(path, sectionName) {
  const fileContent = getFileContent(path);

  const escapedSectionName = sectionName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
//  const sectionRegex = new RegExp(`\\{${escapedSectionName},\\s*\\[[\\s\\S]*?\\]\\}\\.`);
  const sectionRegex = new RegExp(`\\{${escapedSectionName},\\s*\\[([\\s\\S]*?)\\]\\}\\.`);

  const match = fileContent.match(sectionRegex);

  if (!match) {
    console.error(`❌ No {${sectionName}, [...]} block found in file.`);
    process.exit(1);
  }

  const extractedBlock = match[1];
  const blockAsObject = convertErlangTuplePairsToObject(extractedBlock);

  console.log(`ℹ️  Erlang code block "${sectionName}" extracted from "${path}" and converted to Object.`);
  //console.log(blockAsObject);

  return blockAsObject;
}

/**
 * Convert a string of erlang key-value tuple pairs into a 
 * JavaScript object.
 * 
 * - Top-level is a list of Erlang-style {key, value} tuples.
 * - Keys are atoms (e.g., file_name).
 * - Values can be:
 *   - Strings (e.g., "riak.conf")
 *   - Booleans (true, false)
 *   - Lists of atoms (e.g., [riak, riak_kv])
 * 
 * @param {string} erlang A text string containing the erlang 
 *                        key-value tuple pairs to convert. 
 *                        Tuples in tuples is not allowed.
 */
function convertErlangTuplePairsToObject(erlang) {
  const result = {};
  const tupleRegex = /\{([a-zA-Z0-9_]+),\s*((?:\[.*?\])|(?:\".*?\")|(?:true|false)|(?:[a-zA-Z0-9_]+))\}/gs;

  let m;
  while ((m = tupleRegex.exec(erlang)) !== null) {
    const key = m[1];
    let value = m[2].trim();

    // Handle strings
    if (value.startsWith('"') && value.endsWith('"')) {
      value = value.slice(1, -1);
    }
    // Handle booleans
    else if (value === 'true') {
      value = true;
    }
    else if (value === 'false') {
      value = false;
    }
    // Handle lists of atoms: [atom1, atom2]
    else if (value.startsWith('[') && value.endsWith(']')) {
      const items = value
        .slice(1, -1)
        .split(',')
        .map(s => s.trim())
        .filter(Boolean);
      value = items;
    }
    // Otherwise it's just a single atom
    else {
      value = value;
    }

    result[key] = value;
  }

  return result;
}

function downloadFile(url, savePath) {
  const dir = path.dirname(savePath);
  fs.mkdirSync(dir, { recursive: true });

  console.log(`ℹ️  Save url "${url}" to file "${savePath}"`);

  try {
    const res = request('GET', url, { timeout: 10000 }); // timeout in ms
    if (res.statusCode === 200) {
      fs.writeFileSync(savePath, res.getBody());
      console.log(`✅ Downloaded and saved to ${savePath}`);
    } else {
      console.error(`❌ Failed: HTTP ${res.statusCode}`);
      process.exit(1);
    }
  } catch (err) {
    console.error(`❌ Download error: ${err.message}`);
    process.exit(1);
  }
}

main();
