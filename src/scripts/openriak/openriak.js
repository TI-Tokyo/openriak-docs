#!/usr/bin/env node

const commands = {
  updateSchemas: {
    description: 'Updates the Cuttlefish schemas files for a project, either for all versions or a specific version.',
    usage: 'updateSchemas <project> [version]',
    example: '"updateSchemas kv 1.0.0" will update schema files for OpenRiak KV version 1.0.0'
  },
  help: {
    description: 'Show usage information',
    usage: 'help'
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
        console.error('❌ Please provide only the project and optional version.\n');
        console.log(`Usage: ${commands.updateSchemas.usage}`);
        process.exit(1);
      }
      const project = args[0];
      const version = (args.length === 2)?args[1]:null;
      if (!project) {
        console.error('❌ Missing required <project> for updateSchema.\n');
        console.log(`Usage: ${commands.updateSchemas.usage}`);
        process.exit(1);
      }
      console.log(`Updating Schemas for project "${project}"...`);
      if (version) {
        console.log(`Only updating ${version}.`);
      }
      // TODO
      break;

    default:
      console.error('❌ Command handler not implemented.');
      process.exit(1);
  }
}

main();
