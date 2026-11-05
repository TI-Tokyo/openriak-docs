#!/usr/bin/env node
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {parseArgs,run} from '../semantic-search/manager.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
try{
 const options=parseArgs(process.argv.slice(2));
 if(options.help)console.log(`Usage: node tools/scripts/build-semantic-index.mjs --section NAME [--version VERSION] [--retain]
       node tools/scripts/build-semantic-index.mjs --all [--retain]

Rebuild indexes discovered from Hugo output. Product sections without --version
select every rendered version. --all selects every published version and section.
The default profile is release; OPENRIAK_DOCS_BUILD_PROFILE=development limits
a fresh export to development versions. --site-dir follows that output exactly.
--retain keeps previous index files; otherwise superseded files are removed after
successful generation. A fresh Hugo export is built automatically when needed.

Build integration:
  --ensure           Generate missing indexes; validate and reuse existing ones.
  --site-dir PATH    Read rendered version exports from this Hugo output.
  --publish-dir PATH Copy validated indexes and shared runtime into build output.

Pinned build dependencies are installed only when generation requires them.`);
 else await run(root,options);
}catch(error){console.error(error.stack||error.message);process.exitCode=1;}
