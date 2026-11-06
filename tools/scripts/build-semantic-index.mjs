#!/usr/bin/env node
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {parseArgs,run} from '../semantic-search/manager.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
try{
 const options=parseArgs(process.argv.slice(2));
 if(options.help)console.log(`Usage: node tools/scripts/build-semantic-index.mjs --all [OPTIONS]
       node tools/scripts/build-semantic-index.mjs --section NAME --all [OPTIONS]
       node tools/scripts/build-semantic-index.mjs --section NAME --version VERSION [--version VERSION ...] [OPTIONS]

Sections: openriak-kv, openriak-cs, openriak-ts, community, settings,
          archived-technical-blog, archived-mailing-list.

By default, rebuild only missing, stale or invalid indexes. Valid indexes are
left unchanged. --all alone selects every published section and version,
including the homepage. With --section, it selects all versions of that section.
For sections without versions, use --section NAME --all.

Options:
  --whatif          Report what would be rebuilt without changing index/runtime
                    files, installing embedding dependencies or publishing.
                    Exit 1 if updates are needed, otherwise 0.
  --force           Rebuild selected indexes regardless of validity. With
                    --whatif, report those rebuilds without performing them.
  --retain          Keep superseded index files after rebuilding.
  --site-dir PATH   Compare with existing Hugo exports instead of rendering them.
  --publish-dir PATH Copy validated indexes and shared runtime into build output.

The default profile is release. OPENRIAK_DOCS_BUILD_PROFILE=development limits
fresh exports to development versions. --site-dir follows its output exactly.
Fresh Hugo source exports are rendered unless --site-dir is supplied, including
for --whatif. Embeddings are cached and reused during rebuilds where possible.`);
 else {
  const report=await run(root,options);
  if(options.whatif&&(report.needed||report.runtimeIssue))process.exitCode=1;
 }
}catch(error){console.error(error.stack||error.message);process.exitCode=1;}
