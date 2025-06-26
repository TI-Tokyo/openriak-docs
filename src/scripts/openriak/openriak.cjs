#!/usr/bin/env node

const {
  updateSchemas, 
  updateSchemaFiles,
  updateTemplateFiles,
  updateSchemaOSFiles,
 } = require('./commands/updateSchemas.cjs');
const {
  migrateRiakDocs
} = require('./commands/migrateRiakDocs.cjs');

const commands = {
  updateSchemas: {
    description: 'Updates the Cuttlefish schema and template files for a project, either for all versions or a specific version.',
    usage: 'updateSchemas <project> [version]',
    example: '"updateSchemas kv 1.0.0" will update schema files for OpenRiak KV version 1.0.0.'
  },
  updateSchemaFiles: {
    description: 'Updates the Cuttlefish schema files for a project, either for all versions or a specific version.',
    usage: 'updateSchemaFiles <project> [version]',
    example: '"updateSchemaFiles kv 1.0.0" will update cuttlefish schema files for OpenRiak KV version 1.0.0.'
  },
  updateTemplateFiles: {
    description: 'Updates the Cuttlefish template files for a project, either for all versions or a specific version.',
    usage: 'updateTemplateFiles <project> [version]',
    example: '"updateTemplateFiles kv 1.0.0" will update cuttlefish template files for OpenRiak KV version 1.0.0.'
  },
  updateSchemaOSFiles: {
    description: 'Updates the per-OS merged schema files for a project, either for all versions or a specific version.',
    usage: 'updateSchemaOSFiles <project> [version]',
    example: '"updateSchemaOSFiles kv 1.0.0" will update cuttlefish OS-specific schema files for OpenRiak KV version 1.0.0.'
  },
  migrateRiakDocs: {
    description: 'Imports an old RiakDocs markdown version from a source path to specific version. Note that this is destructive of the destination!',
    usage: 'updateSchemaOSFiles sourcePath project version',
    example: '"updateSchemaOSFiles \'../riak-docs-fork/content/kv/3.0.16\' kv 3.0.16" will try to import from the path to project kv version 3.0.16.'
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
    case 'migrateRiakDocs':
      if (args.length === 0 || args.length > 3) {
        console.error(`❌ Please provide only the source path and destination project and version.\n`);
        console.log(`Usage: ${commands[command].usage}`);
        process.exit(1);
      }
      const sourcePath = args[0];
      const destinationProject = args[1];
      const destinationVersion = args[2];

      if (!['kv','cs','ts'].includes(destinationProject)) {
        console.error(`❌ Unknown project ${destinationProject}.\n`);
        process.exit(1);
      }

      if (!destinationVersion.match(/^[0-9]\.[0-9]\.[0-9]{1,2}$/s)) {
        console.error(`❌ Invalid version ${destinationVersion}.\n`);
        process.exit(1);
      }

      console.log(`Importing RiakDocs from ${sourcePath} to project ${destinationProject} version ${destinationVersion}`);
      migrateRiakDocs(sourcePath, destinationProject, destinationVersion);
      break;
    case 'updateSchemas':
    case 'updateSchemaFiles':
    case 'updateTemplateFiles':
    case 'updateSchemaOSFiles':
      if (args.length === 0 || args.length > 2) {
        console.error(`❌ Please provide only the project and optional version.\n`);
        console.log(`Usage: ${commands[command].usage}`);
        process.exit(1);
      }
      const project = args[0];
      const version = (args.length === 2)?args[1]:null;
      if (!project) {
        console.error(`❌ Missing required <project> for ${command}.\n`);
        console.log(`Usage: ${commands[command].usage}`);
        process.exit(1);
      }
      var message = `Updating for project "${project}"`;
      if (version) {
        message += ` version "${version}"`;
      }
      message += `...`;
      console.log(message);
      
      switch (command) {
          case 'updateSchemaOSFiles': updateSchemaOSFiles(project, version); break;
          case 'updateSchemaFiles': updateSchemaFiles(project, version); break;
          case 'updateTemplateFiles': updateTemplateFiles(project, version); break;
          case 'updateSchemas':
          default: updateSchemas(project, version);
      }
      break;
    default:
      console.error(`❌ Command handler not implemented.`);
      process.exit(1);
  }
}

main();

