#!/usr/bin/env node

const { getFileContent, setFileContent, doesFileExist, ensureFolderExists } = require('./fileHelpers.cjs');
const { downloadFile, convertGithubToRawUrl } = require('./netHelpers.cjs');
const path = require('path');

function getSchemaRoot(project) {
  const schemaRoot = path.join('static', 'cached-data', 'schemas', project);
  // Ensure folder exists
  ensureFolderExists(schemaRoot);
  return schemaRoot;
}

function getVersionRoot(project, version) {
  const versionRoot = path.join(getSchemaRoot(project), version);
  // Ensure folder exists
  ensureFolderExists(versionRoot);
  return versionRoot;
}

function getSchemaDefinitions(project, version) {
  const schemaRoot = getSchemaRoot(project);
  const schemaPath = path.join(schemaRoot, 'schemas.json');

  // Check that the file exists
  if (!doesFileExist(schemaPath)) {
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

  // templates are optional, so don't check them
  return schemas;
}

function getVersionsToUpdate(schemas, version) {
  // Loop over the versions to update
  var versionsToUpdate = {};
  if (version) {
    versionsToUpdate[version] = schemas.versions[version];
  } else {
    versionsToUpdate = schemas.versions;
  }
  return versionsToUpdate;
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
/*
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
*/

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

function parseTemplatePlaceholders(templateSavePath, version, config) {
  const result = {};

  const raw = getFileContent(templateSavePath);
  const lines = raw.split('\n');

  // get substituion variables
  const variables = {};
  if (config.variables) {
    for (const variable of config.variables) {
      if (variable.pattern) {
        //console.log(`ℹ️  Looking for pattern`);
        for (let i = 0; i < lines.length; i++) {
          const nameGroup = variable.nameGroup || "name";
          const valueGroup = variable.valueGroup || "value";
          
          var line = lines[i].trim();
          const regExp = new RegExp(variable.pattern, );
          const match = line.match(regExp, "gm");
          //console.log(i);
          //console.log(line);
          //console.log(variable.pattern);
          //console.log(match);
          if (match && match.groups) {
            const name = match.groups[nameGroup];
            const value = match.groups[valueGroup];
            variables[name] = value;
            //console.log(`ℹ️  Variable "${name}" with value "${value}".`);
          }
        }
      } else if (variable.value) {
        //console.log(`ℹ️ℹ  Variable "${variable["name"]}" with value "${variable["value"]}".`);
        variables[variable["name"]] = variable["value"];
      } else if (variable.source) {
        //console.log(`ℹ️ℹ  Variable "${variable.name}" with source "${variable.source}".`)
        switch (variable.source) {
          case 'version': variables[variable["name"]] = version; break;
          default:
            console.error(`❌ Unknown placeholder variable source of "${variable.source}"`);
            process.exit(1);
        }
      } else {
        console.error(`❌ Unknown placeholder variable format for "${JSON.stringify(variable, null, 0)}"`);
        process.exit(1);
      }
    }
  }

  //console.log(`ℹ️  Variables: ${JSON.stringify(variables, null, 2)}`);

  // get template placeholders
  var inSelectedSection = false;
  if (!config.after) {
    inSelectedSection = true;
  }

  for (let i = 0; i < lines.length; i++) {
    var line = lines[i].trim();

    // ignore blank lines
    if (!line) { continue; }

    if (config.after && line === config.after) {
      inSelectedSection = true;
    }

    if (config.until && line === config.until) {
      inSelectedSection = false;
    }

    // Ignore comments
    if (line.startsWith('%%')) {
      continue;
    }

    // Detect mapping block start
    if (inSelectedSection && line.startsWith('{')) {
      let blockLines = [line];
      while (!line.endsWith('}.')) {
        i++;
        line = lines[i].trim();
        blockLines.push(line);
      }

      const templateBlock = blockLines.join(' ').trim();

      const templateMatch = templateBlock.match(/^\{\s*([^,]+)\s*,\s*"?([^"]+)"?\s*\}\.$/s);
      if (!templateMatch) continue;

      //console.log("ℹ️  Template match: ", JSON.stringify(templateMatch, null, 2));

      const [rawTemplateMatch, templateName, templateValue] = templateMatch;

      //console.log(`ℹ️  Template Placeholder "${templateName}" with value "${templateValue}".`);

      var templateValueWithVariables = templateValue;
      // stick a max limit on it in case of issues
      var replaceIterationCounterMax = 10;
      var replaceIterationCounter = 0;
      while (replaceIterationCounter < replaceIterationCounterMax && templateValueWithVariables.includes("%{")) {
        replaceIterationCounter++;
        for ([varName, varValue] of Object.entries(variables)) {
          const replaceVarName = `%{${varName}}`;
          if (templateValueWithVariables.includes(replaceVarName)) {
            //console.log(`ℹ️ℹ️  Template Placeholder contains "${replaceVarName}" so will replace with value "${varValue}".`);
            templateValueWithVariables = templateValueWithVariables.replace(replaceVarName, varValue);
            //console.log(`ℹ️ℹ️  New Template Placeholder "${templateName}" with value "${templateValueWithVariables}".`);
          }
        }
      }
      if (templateValueWithVariables !== templateValue) {
        //console.log(`ℹ️ℹ️ℹ️  New Template Placeholder "${templateName}" with value "${templateValueWithVariables}".`);
      }
      if (replaceIterationCounter === replaceIterationCounterMax) {
        console.error(`❌ Variable replacement loop on "${templateSavePath}" with template placeholder name "${templateName}" exceeded limit.`)
        process.exit(1);
      }
      result[templateName] = templateValueWithVariables;
    }
  }

  return result;
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

function parseComments(comments) {
  const docText = [];
  const docSections = [];
  const docRelateds = [];
  const docSees = [];
  const docOther = [];

  var inDocText = false;

  for (const line of comments) {
    var cleanLine = line.trim();
    if (cleanLine.startsWith('@doc')) {
      inDocText = true;
      cleanLine = cleanLine.replace('@doc','').trim();
      docText.push(cleanLine);
      continue;
    }
    if (cleanLine.startsWith('@see')) {
      inDocText = false;
      cleanLine = cleanLine.replace('@see','').trim();
      docSees.push(cleanLine);
      continue;
    }
    if (cleanLine.startsWith('@related')) {
      inDocText = false;
      cleanLine = cleanLine.replace('@related','').trim();
      docRelateds.push(cleanLine);
      continue;
    }
    if (cleanLine.startsWith('@section')) {
      inDocText = false;
      cleanLine = cleanLine.replace('@section','').trim();
      docSections.push(cleanLine);
      continue;
    }
    if (inDocText) {
      docText.push(line);
    } else {
      docOther.push(line);
    }
  }
  
  return {
    docText: docText,
    docSections: docSections,
    docRelateds: docRelateds,
    docSees: docSees,
    docOther: docOther,
  }
}

function parseCuttlefishSchema(filePath) {
  const raw = getFileContent(filePath);

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
      //console.log(mappingObject);
      const blockType   = mappingObject[0].value;
      const configName  = mappingObject[1].value;
      const settingName = mappingObject[2].value;
      const properties  = mappingObject[3].value;

      const parsedComments = parseComments(commentBuffer);

      results.push({
        rawSchema: mappingBlock,
        comment: commentBuffer,
        docText: parsedComments.docText,
        docSections: parsedComments.docSections,
        docRelateds: parsedComments.docRelateds,
        docSees: parsedComments.docSees,
        docOther: parsedComments.docOther,
        type: blockType,
        configName: configName,
        settingName: settingName,
        properties: properties,
      });

      commentBuffer = [];
    } else if (line.startsWith('{translation,')) {
      let blockLines = [line];
      while (!line.endsWith('}.')) {
        i++;
        line = lines[i].trim();
        blockLines.push(line);
      }

      const translationBlock = blockLines.join(' ').trim();

      const translationRegExp = /^\{(translation),\s*"([^"]+)",\s*(.*)\s*\}\.$/s
      const translationMatch = translationBlock.match(translationRegExp);
      if (!translationMatch) continue;

      const [rawTranslationBlock, blockType, configName, func] = translationMatch;
      
      const parsedComments = parseComments(commentBuffer);

      results.push({
        rawSchema: rawTranslationBlock,
        comment: commentBuffer,
        docText: parsedComments.docText,
        docSections: parsedComments.docSections,
        docRelateds: parsedComments.docRelateds,
        docSees: parsedComments.docSees,
        docOther: parsedComments.docOther,
        type: blockType,
        configName: configName,
        func: func,
      });

      commentBuffer = [];
    } else if (line.startsWith('{validator,')) {
      let blockLines = [line];
      while (!line.endsWith('}.')) {
        i++;
        line = lines[i].trim();
        blockLines.push(line);
      }

      const validatorBlock = blockLines.join(' ').trim();

      const validatorRegExp = /^\{(validator),\s*"([^"]+)",\s*"([^"]+)",\s*(.*)\s*\}\.$/s
      const validatorMatch = validatorBlock.match(validatorRegExp);
      if (!validatorMatch) continue;

      const [rawValidatorBlock, blockType, name, description, func] = validatorMatch;
      
      const parsedComments = parseComments(commentBuffer);

      results.push({
        rawSchema: rawValidatorBlock,
        comment: commentBuffer,
        docText: parsedComments.docText,
        docSections: parsedComments.docSections,
        docRelateds: parsedComments.docRelateds,
        docSees: parsedComments.docSees,
        docOther: parsedComments.docOther,
        type: blockType,
        name: name,
        description: description,
        func: func,
      });

      commentBuffer = [];
    }

  }
  return results;
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

module.exports = { 
  convertErlangTuplePairsToObject, 
  getSchemaDefinitions, 
  getVersionRoot, 
  getSchemaRoot, 
  getVersionsToUpdate, 
  parseTemplatePlaceholders,
  getRebarLockSections,
  getRebarConfSectionFromFile,
  convertErlangTuplePairsToObject,
  parseCuttlefishSchema,
  parseErlangToObject
 };
