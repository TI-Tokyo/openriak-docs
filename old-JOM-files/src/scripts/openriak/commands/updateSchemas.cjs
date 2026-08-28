#!/usr/bin/env node

const { 
  getFileContent, 
  setFileContent, 
  doesFileExist} = require('../lib/fileHelpers.cjs');
const { 
  getMetadataRoot, 
  getVersionRoot, 
  getSchemaDefinitions, 
  getVersionsToUpdate, 
  parseTemplatePlaceholders, 
  getRebarConfSectionFromFile,
  getRebarLockSections,
  parseCuttlefishSchema } = require('../lib/schemaHelpers.cjs');
const { 
  convertGithubToRawUrl, 
  downloadFile} = require('../lib/netHelpers.cjs');
const {simplifySchemaJSON} = require("../lib/simplifySchemaJSON.cjs");
const {mergeClone} = require("../lib/mergeClone.cjs");
const path = require('path');

function updateSchemas(project, version) {
  updateSchemaFiles(project, version);
  updateTemplateFiles(project, version);
  updateSchemaOSFiles(project, version);
}

function updateSchemaOSFiles(project, desiredVersion) {
  const schemas = getSchemaDefinitions(project, desiredVersion);
  const versionsToUpdate = getVersionsToUpdate(schemas, desiredVersion)
  for (const [version, object] of Object.entries(versionsToUpdate)) {
    const versionRoot = getVersionRoot(project, version);
    const schemaFile = path.join(versionRoot, 'schemas', 'allSchemas.json');
    if (!doesFileExist(schemaFile)) {
      console.error(`❌ Error: Cannot find schemas file for project "${project}" version "${version}" at "${schemaFile}".`)
      process.exit(1);
    }

    for (templateName of Object.keys(schemas.templates)) {
      var allSchemas = getFileContent(schemaFile);
      if (templateName.startsWith('#')) { continue; }
      const templateFileName = path.join(versionRoot, 'templates', templateName + `.templatePlaceholders.json`);
      const templateFile = getFileContent(templateFileName);
      const templateObject = JSON.parse(templateFile);
      for ([key, value] of Object.entries(templateObject)) {
        var safeValue = JSON.stringify(value, null, 0);
        safeValue = safeValue.replace(/^(['"])(.*)\1$/, '$2');
        allSchemas = allSchemas.replaceAll(`{{${key}}}`, safeValue);
      }
      const schemaOSFileName = path.join(getMetadataRoot(), 'config-reference', `openriak-${project}-${version}.config-reference.${templateName}.json`);

      //const schemaOSFileName  = path.join(versionRoot, `openriak-${project}-${version}.config-reference.${name}.json`);
      setFileContent(schemaOSFileName, allSchemas);
      console.log(`✅ Schema file for project "${project}" version "${version}" created at ${schemaOSFileName}.`);
    }
  }
}

function updateSchemaFiles(project, version) {
  const schemas = getSchemaDefinitions(project, version);
  const versionsToUpdate = getVersionsToUpdate(schemas, version)

  for (const [version, object] of Object.entries(versionsToUpdate)) {
    const versionRoot = getVersionRoot(project, version);

    const versionTagOrCommit = object.tagOrCommit || version;
    //console.log(`ℹ️  Checking schema for "${project}" version "${version}" using tag or commit name "${versionTagOrCommit}":`);

    const versionRebarConfigFile  = object.rebarConfigFile || schemas.defaultRebarConfigFile;
    const versionRebarLockFile    = object.rebarLockFile   || schemas.defaultRebarLockFile;
    
    const actualRebarConfigFile = versionRebarConfigFile.replace('{versionTagOrCommit}', versionTagOrCommit);
    const actualRebarLockFile   = versionRebarLockFile.replace('{versionTagOrCommit}', versionTagOrCommit  );

    const actualRebarConfigFileRaw = convertGithubToRawUrl(actualRebarConfigFile);
    const actualRebarLockFileRaw   = convertGithubToRawUrl(actualRebarLockFile  );

    //console.log('ℹ️  Resolved rebar.config path:', actualRebarConfigFileRaw);
    //console.log('ℹ️  Resolved rebar.lock path:  ', actualRebarLockFileRaw  );

    const rebarConfigDestPath = path.join(versionRoot, 'rebar', 'rebar.config');
    const rebarLockDestPath   = path.join(versionRoot, 'rebar', 'rebar.lock'  );
  
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
    const results = [];

    desiredSchemas.forEach((schemaName, index) => {
      const repoInfo = versionRepoMappings[schemaName];
      // remove ".git" and any trailing slash if present from the repo url
      const repoUrl = repoInfo.repoUrl.replace(/(\.git)?\/?$/, '');
      const fileUrl = repoInfo.fileUrl.replace('{tagOrCommit}', repoInfo.tagOrCommit);
      const fullUrl = `${repoUrl}${fileUrl}`;
      const rawUrl = convertGithubToRawUrl(fullUrl);
      const schemaSavePath = path.join(versionRoot, 'schemas', `${index}-${schemaName}.schema`);
      downloadFile(rawUrl, schemaSavePath);
      const schemaObject = parseCuttlefishSchema(schemaSavePath);
      //console.log(schemaObject);
      
      const rawObjectSavePath = path.join(versionRoot, 'schemas', `${index}-${schemaName}.raw.json`);
      const objectSavePath = path.join(versionRoot, 'schemas', `${index}-${schemaName}.json`);
      setFileContent(rawObjectSavePath, JSON.stringify(schemaObject, null, 2));
      const simplerSchemaObject = simplifySchemaJSON(schemaObject);
      results.push(simplerSchemaObject);
      try {
        setFileContent(objectSavePath, JSON.stringify(simplerSchemaObject, null, 2));
      } catch (err) {
        console.error(`❌ Error when simplifying JSON schema object: ${err.message}`);
        process.exit(1);
      }
      console.log(`✅ Converted and saved to ${objectSavePath}.`);
    });

    const mergedResultSavePath = path.join(versionRoot, 'schemas', `allSchemas.json`);
    try {
      var mergedResult = {}
      for (result of results) {
        mergedResult = mergeClone(0, result, mergedResult);
      }
      
      // tag mappins with default fields that have placeholders
      Object.values(mergedResult.mappings).filter(item => {
        return (item.properties?.default && item.properties?.default.includes('{{'))
      }).map(item => {
        item.properties.defaultHasPlaceholder = true;
      });
      
      setFileContent(mergedResultSavePath, JSON.stringify(mergedResult, null, 2));
    } catch (err) {
      console.error(`❌ Error when merging and saving JSON schema objects: ${err.message}`);
      throw err;
      //process.exit(1);
    }
    console.log(`✅ Merged and saved to ${mergedResultSavePath}.`);
  }
}

function updateTemplateFiles(project, version) {
  // Now handle the cuttlefish template placeholders
  const schemas = getSchemaDefinitions(project, version);

  if (!schemas.templates) {
    console.log(`✅ No cuttlefish template placeholders defined, so exiting as done.`);
    return;
  }

  const versionsToUpdate = getVersionsToUpdate(schemas, version);

  for (const [templateName, files] of Object.entries(schemas.templates)) {
    if (templateName.startsWith('#')) { continue; }
    for (const [version, versionObject] of Object.entries(versionsToUpdate)) {
      const versionRoot = getVersionRoot(project, version);
      const versionTagOrCommit = versionObject.tagOrCommit || version;

      var templateFiles = null;
      if (Array.isArray(files)) {
        templateFiles = [];
        templateFiles = structuredClone(files);
      } else if (files.path) {
        templateFiles = [structuredClone(files)];
      } else {
        throw Error(`❌ Error: unknown template detail type for template "${templateName}".`);
      }

      const convertedTemplatePlaceholders = [];
      for (const [index, templateFile] of templateFiles.entries()) {
        if (templateFile.path) {
          templateFile.path = templateFile.path.replace('{versionTagOrCommit}', versionTagOrCommit);
          templateFile.path = convertGithubToRawUrl(templateFile.path);
          const templateSavePath = path.join(versionRoot, `templates`, `${templateName}-${index}.vars.config`);
          downloadFile(templateFile.path, templateSavePath);

          const templateObject = parseTemplatePlaceholders(templateSavePath, version, templateFile);
          //console.log(schemaObject);
          
          convertedTemplatePlaceholders.push(templateObject);
        } else if (templateFile.placeholderName && templateFile.value) {
          const templateObject = {};
          templateObject[templateFile.placeholderName] = templateFile.value;
          convertedTemplatePlaceholders.push(templateObject);
        } else if (templateFile.placeholderName && templateFile.source) {
          switch (templateFile.source) {
            case 'version':
              const templateObject = {};
              templateObject[templateFile.placeholderName] = version;
              convertedTemplatePlaceholders.push(templateObject);
              //console.log(`ℹ️  source version`);
              break;
            default:
              console.error(`❌ Unknown placeholder source of "${templateFile.source}"`);
              process.exit(1);
          }
        }
      }

      // merge them together, with later values overwriting earlier values
      const templatePlaceholdersObject = {};
      for (source of convertedTemplatePlaceholders) {
        for (const [name, value] of Object.entries(source)) {
          templatePlaceholdersObject[name] = value;
        }
      }

      //console.log(`ℹ️  sortedTemplatePlaceholdersObject: `, sortedTemplatePlaceholdersObject);


      // perform replacements on the placeholders 
      const placeHolderRegExp = /(\{\{([^}]+)\}\})/s;
      for (const [name, value] of Object.entries(templatePlaceholdersObject)) {
        var newValue = value;
        const limitMax = 10;
        var limitCounter = 0;
        while (limitCounter < limitMax && newValue.match(placeHolderRegExp)) {
          limitCounter++;
          const [, replacementKey, replacementProperty] = newValue.match(placeHolderRegExp);
          //console.log(`ℹ️  Replacing placeholder: "${replacementKey}" with "${replacementProperty}".`);
          // check if desired placeholder exists
          if (templatePlaceholdersObject[replacementProperty]) {
            newValue = newValue.replace(replacementKey, templatePlaceholdersObject[replacementProperty]);
            //console.log(`ℹ️  Loop: New value for "${name}" is "${newValue}" (was "${value}").`);

          } else {
            console.error(`❌ Placeholder replacement loop on project "${project}" version "${version}" placeholder "${name}" in template "${templateName}" wants placeholder "${replacementProperty}" which could not be found.`)
            process.exit(1);
          }
        }
        if (limitCounter === limitMax) {
          console.error(`❌ Placeholder replacement loop on project "${project}" version "${version}" with template placeholder name "${name}" exceeded limit.`)
          process.exit(1);
        }
        //console.log(`ℹ️  New value for "${name}" is "${newValue}" (was "${value}").`);
        templatePlaceholdersObject[name] = newValue;
      }


      // order by name to make it more human readable
      const sortedTemplatePlaceholdersObject = Object.keys(templatePlaceholdersObject)
        .sort() // Sort keys alphabetically
        .reduce((acc, key) => {
          acc[key] = templatePlaceholdersObject[key]; // Rebuild object with sorted keys
          return acc;
        }, {});


      const templatePlaceholdersSavePath = path.join(versionRoot, 'templates', `${templateName}.templatePlaceholders.json`);
      setFileContent(templatePlaceholdersSavePath, JSON.stringify(sortedTemplatePlaceholdersObject, null, 2));
//      console.log(`✅ Converted var.config named "${templateName}" for project "${project}" version "${version}" and saved to ${templatePlaceholdersSavePath}`);
      console.log(`✅ Converted and saved to ${templatePlaceholdersSavePath}`);
    }
  }
}

module.exports = { updateSchemas, updateSchemaFiles, updateTemplateFiles, updateSchemaOSFiles };

