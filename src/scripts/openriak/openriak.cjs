#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const request = require('sync-request');

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
    //console.log(`ℹ️  Checking schema for "${project}" version "${version}" using tag or commit name "${versionTagOrCommit}":`);

    const versionRebarConfigFile  = object.rebarConfigFile || defaultRebarConfigFile;
    const versionRebarLockFile    = object.rebarLockFile   || defaultRebarLockFile;
    
    const actualRebarConfigFile = versionRebarConfigFile.replace('{versionTagOrCommit}', versionTagOrCommit);
    const actualRebarLockFile   = versionRebarLockFile.replace('{versionTagOrCommit}', versionTagOrCommit  );

    const actualRebarConfigFileRaw = convertGithubToRawUrl(actualRebarConfigFile);
    const actualRebarLockFileRaw   = convertGithubToRawUrl(actualRebarLockFile  );

    //console.log('ℹ️  Resolved rebar.config path:', actualRebarConfigFileRaw);
    //console.log('ℹ️  Resolved rebar.lock path:  ', actualRebarLockFileRaw  );

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

    // Make sure we have metadata for each schema defined in the project rebar.config file
    // and that the metadata is specific to this project and version
    var unfoundRepos = false;
    desiredSchemas.forEach((schemaName, index) => {
      //console.log(`ℹ️  Finding "${schemaName}" at index ${index}.`);
      const repoInfo = versionRepoMappings[schemaName];
      if (!repoInfo) {
        console.log(`❌ Unable to find "${schemaName}" at position ${index} in schemaToRepoMappings for version "${version}".`);
        unfoundRepos = true;
      } else if (repoInfo.repoUrl) {
        repoInfo.tagOrCommit = versionTagOrCommit;
        //console.log(`ℹ️  Using "${repoInfo.repo}" with tagOrCommit "${repoInfo.tagOrCommit}" for schema "${schemaName}".`);
      } else if (repoInfo.repo in rebarLockSections) {
        repoInfo.repoUrl = rebarLockSections[repoInfo.repo].url;
        repoInfo.tagOrCommit = rebarLockSections[repoInfo.repo].tagOrCommit;
        //console.log(`ℹ️  Using "${repoInfo.repo}" with tagOrCommit "${repoInfo.tagOrCommit}" for schema "${schemaName}".`);
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
      const fullUrl = `${repoUrl}${fileUrl}`;
      const rawUrl = convertGithubToRawUrl(fullUrl);
      const schemaSavePath = path.join(versionRoot, `${schemaName}.schema`);
      downloadFile(rawUrl, schemaSavePath);
      const schemaObject = parseCuttlefishSchema(schemaSavePath);
      console.log(schemaObject);
      
      const objectSavePath = path.join(versionRoot, `${index}-${schemaName}.json`);
      fs.writeFileSync(objectSavePath, JSON.stringify(schemaObject, null, 2), 'utf8');
      console.log(`✅ Converted and saved to ${objectSavePath}`);

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

  //console.log(`ℹ️  Erlang code block "${sectionName}" extracted from "${path}" and converted to Object.`);
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

  //console.log(`ℹ️  Save url "${url}" to file "${savePath}"`);

  try {
    const res = request('GET', url, { timeout: 10000 }); // timeout in ms
    if (res.statusCode === 200) {
      fs.writeFileSync(savePath, res.getBody());
      //console.log(`✅ Downloaded and saved to ${savePath}`);
    } else {
      console.error(`❌ Failed: HTTP ${res.statusCode}`);
      process.exit(1);
    }
  } catch (err) {
    console.error(`❌ Download error: ${err.message}`);
    process.exit(1);
  }
}

function parseCuttlefishSchema(filePath) {
  const raw = fs.readFileSync(filePath, 'utf-8');

  const lines = raw.split('\n');

  const results = [];

  let commentBuffer = [];

  for (let i = 0; i < lines.length; i++) {
    var line = lines[i].trim();

    // Skip header line like: %%-*- mode: erlang -*-
    if (/^%%-*-.*-*-$/.test(line)) continue;

    // Collect comments
    if (line.startsWith('%%')) {
      commentBuffer.push(line.replace(/^%%\s?/, ''));
      continue;
    }

    // Detect mapping block start
    if (line.startsWith('{mapping,')) {
      let blockLines = [line];
      while (!line.endsWith('}.')) {
        i++;
        line = lines[i].trim();
        blockLines.push(line);
      }

      const mappingBlock = blockLines.join(' ').trim();

      const mappingMatch = mappingBlock.match(/^\{mapping,\s*"([^"]+)",\s*"([^"]+)",\s*\[(.*)\]\s*\}\.$/s);
      if (!mappingMatch) continue;

      const mappingObject = parseErlangToObject(mappingBlock).value;
      console.log(mappingObject);
      const blockType   = mappingObject[0].value;
      const configName  = mappingObject[1].value;
      const settingName = mappingObject[2].value;
      const properties  = mappingObject[3].value;

      results.push({
        rawSchema: mappingBlock,
        comment: commentBuffer,
        type: blockType,
        configName: configName,
        settingName: settingName,
        properties: properties,
      });

      commentBuffer = [];
    }
  }
  return results;
}

function parseSchemaValidators(value) {
  // Normalize input (remove quotes if present)
  // I know we did this before but, I'm untrusting on occasion
  const trimmed = value.replace(/^"(.*)"$/, '$1').trim();

  try {
    // Replace Erlang-style list with JSON-compatible string
    const values = JSON.parse(
      trimmed.replace(/'/g, '"')
    );
    return { rawDatatype: trimmed, validators: values };
  } catch {
    return { rawDatatype: trimmed, validators: [] };
  }
}

function parseSchemaDataType(value) {
  // Normalize input (remove quotes if present)
  // I know we did this before but, I'm untrusting on occasion
  const trimmed = value.replace(/^"(.*)"$/, '$1').trim();

  // Match outer Erlang tuple: {key, value}
  //const tupleRegex = /^\{([^,]+),\s*(.+)\}$/;
  const tupleRegex = /(^[^{},]+$)|(^\{([^,]+),\s*(.+)\}$)|(^\[(.+)\]$)/;
    const match = trimmed.match(tupleRegex);

  if (!match) {
    return { type: 'unknown-nomatch', rawDatatype: trimmed };
  }  

  const [rawDatatype, simpleType, complexRaw, complexType, valuesRaw, arrayRaw, array ] = match;
  if (arrayRaw) {

  }
  const cleanType = (simpleType || complexType).trim();
  const cleanValuesRaw = (valuesRaw || "").trim();
  // Handle known types
  switch (cleanType) {
    case 'atom':
    case 'bytesize':
    case 'directory':
    case 'file':
    case 'float':
    case 'integer':
    case 'ip':
    case 'string':
      return { rawDatatype: rawDatatype, type: cleanType };

    case 'duration':
      return { rawDatatype: rawDatatype, type: 'duration', unit: cleanValuesRaw };

    case 'enum':
      try {
        //console.log(`ℹ️  Found "${cleanType}" with values "${cleanValuesRaw}".`);
        const singleToDoubleQuoted = cleanValuesRaw.replace(/'([^']*)'/g, (_, inner) =>
            `"${inner.replace(/"/g, '\\"')}"`
          );
        //console.log(`ℹ️  Cleaned values to "${singleToDoubleQuoted}".`);
        const valuesArray = JSON.parse(singleToDoubleQuoted);
        //console.log(`ℹ️  Parsed values to "${valuesArray}".`);
        return { rawDatatype: rawDatatype, type: 'enum', valuesArray };
      } catch (err) {
        return { rawDatatype: rawDatatype, type: 'unknown', err: err };
      }

    default:
      // Fallback: return unknown but matched  if unrecognized
      return { rawDatatype: rawDatatype, type: 'unknown-matched' };
  }
}

function findClosingQuote(input, from, quoteChar) {
  //console.log(`ℹ️  Finding quote <<${quoteChar}>> in <<${input.slice(from)}>>.`)
  var skipMarker = '\\';
  for (var i=from; i<input.length; i++) {
    //console.log(`ℹ️  i: ${i}, char: ${input[i]}`);
    switch (input[i]) {
      case skipMarker: i++; break;
      case quoteChar:  return i;
    }
  }
  throw new Error(`❌ Error: Closing quote "${quoteChar}" not found in "${input}" from ${{from}}.`);
}

function findClosingBracket(input, from, opener, closer, skipMarker) {
  //console.log(`ℹ️  Finding "${opener}" to "${closer}" in "${input}" starting from ${from}.`)
  var openCounter = 0;
  for (var i=from; i<input.length; i++) {
    //console.log(`ℹ️  openCouter: ${openCounter}, i: ${i}, char: ${input[i]}`);
    switch (input[i]) {
      case skipMarker: i++; break;
      case opener: openCounter++; break;
      case closer: openCounter--; break;
      case '"':    i = findClosingQuote(input, i+1, '"'); break;
      case '\'':   i = findClosingQuote(input, i+1, '\''); break;
    }
    if (!openCounter) {
      return i;
    }
  }
  throw new Error(`❌ Error: Closing not found for "${opener}"/"${closer}" pair in "${input.slice(from)}".`);
}

function findComma(input, from) {
  //console.log(`ℹ️  Finding "," in "${input}" starting from ${from}.`)
  for (var i=from; i<input.length; i++) {
    //console.log(`ℹ️  i: ${i}, char: ${input[i]}`);
    switch (input[i]) {
      case ',': return i; break;
    }
  }
  // no comma found, which is fine
  return input.length;
}

function parseErlangToObject(input) {
  var cleanInput = input.trim();
  if (!cleanInput) {
    throw new Error(`❌ Error: No string to parse: ${input}`);
  }
  const results = [];

  while (cleanInput) {
    //console.log(`ℹ️  Checking <<${cleanInput}>>`);
    switch (cleanInput[0]) {
      case '{': 
        if (cleanInput[1] === '{') {
          // it'S a schema template placeholder like "{{somename}}"
          var closingLocation = findClosingQuote(cleanInput, 2, '}');
          var innerText = cleanInput.slice(2,closingLocation);
          //console.log(`ℹ️  Found template placeholder content <<${innerText}>>.`)
          results.push({type: "template", value: innerText});
          cleanInput = cleanInput.slice(closingLocation+2);
          break;
        } else {
          // tuple
          var closingLocation = findClosingBracket(cleanInput, 0, '{', '}');
          var innerText = cleanInput.slice(1,closingLocation);
          //console.log(`ℹ️  Found tuple content <<${innerText}>>.`)
          results.push({type:"tuple",value:parseErlangToObject(innerText)});
          cleanInput = cleanInput.slice(closingLocation+1);
        }
        break;
      case '[':
        //array
        var closingLocation = findClosingBracket(cleanInput, 0, '[', ']');
        var innerText = cleanInput.slice(1,closingLocation);
        //console.log(`ℹ️  Found array content <<${innerText}>>.`)
        results.push({type:"array", value: parseErlangToObject(innerText)});
        cleanInput = cleanInput.slice(closingLocation+1);
        //console.log(`ℹ️  Finished. Moving on to next input: ${cleanInput}`)
        break;
      case '\'':
        // single-quoted string
        var closingLocation = findClosingQuote(cleanInput, 1, '\'');
        var innerText = cleanInput.slice(1,closingLocation);
        //console.log(`ℹ️  Found single-quoted string content <<${innerText}>>.`)
        results.push({type: "text", value: innerText});
        cleanInput = cleanInput.slice(closingLocation+1);
        break;
      case '"':
        // double-quoted string
        var closingLocation = findClosingQuote(cleanInput, 1, '"');
        var innerText = cleanInput.slice(1,closingLocation);
        //console.log(`ℹ️  Found double-quoted string content <<${innerText}>>.`)
        results.push({type:"text", value: innerText});
        cleanInput = cleanInput.slice(closingLocation+1);
        break;
      case '<':
        //binary string
        var closingLocation = findClosingBracket(cleanInput, 1, '<', '>');
        var innerText = cleanInput.slice(2,closingLocation-1);
        //console.log(`ℹ️  Found binary content <<${innerText}>>.`)
        results.push({type:"binary", value:innerText});
        cleanInput = cleanInput.slice(closingLocation+2);
        break;
      case ' ':
        // space
        //console.log(`ℹ️  Found space.`)
        cleanInput = cleanInput.slice(1);
        break;
      case ',':
        // space
        //console.log(`ℹ️  Found comma.`)
        cleanInput = cleanInput.slice(1);
        break;
      default:
        //atom
        var closingLocation = findComma(cleanInput, 0);
        var innerText = cleanInput.slice(0,closingLocation);
        //console.log(`ℹ️  Found atom <<${innerText}>>.`)
        results.push({type:"atom", value:innerText});
        cleanInput = cleanInput.slice(closingLocation+1);
        break;
    }
  }
  
  if (results.length === 2 && results[1].type === "atom" && results[1].value === ".") {
    return results[0];
  }
  return results;
}

function testHarness() {
  const input = `{mapping, {{logger.level}}, "kernel.logger_level", [ {default, {{logger_level}} }, {datatype, {enum, [debug, info, notice, warning, error, critical, alert, emergency, none]}} ]}.`;
  //const input = `{mapping}`;
  //const input = `{mapping, darn}`;
  //const input = `{"mapping"}`;
//  const input = `{"mapping", "darn"}`;
//  const input = `{mapping, "darn"}`;
//const input = `{mapping, {{logger.level}}}`
  const jsObject = parseErlangToObject(input);
  console.log("✅ Success:", JSON.stringify(jsObject, null, 2));
}

main();
//testHarness();
