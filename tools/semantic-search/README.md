# Semantic search

Documentation versions, Community and the Technical Blog use pre-built document embeddings and
browser-side query embedding/search. Text indexes and text-only search remain in
place. The panel explicitly shows semantic loading, semantic + text search, or
text-only fallback. Searches make no requests to external inference services.

## Files and ownership

- `content/static/semantic-search/`: shared model, browser runtime, search modules,
  licences and `runtime.json`. Hugo publishes this at `/semantic-search/`, beneath
  the configured base path.
- `content/static/semantic-indexes/archived-technical-blog/`: blog manifest, passage
  JSON and binary vectors, published at `/semantic-indexes/archived-technical-blog/`.
- `content/static/semantic-indexes/openriak-kv/3.4.1/`: KV 3.4.1 manifest, passage JSON
  and binary vectors, published at `/semantic-indexes/openriak-kv/3.4.1/`.
- `content/static/semantic-indexes/SECTION[/VERSION]/`: section/version indexes.
- `tools/semantic-search/indexes.json`: Markdown source override for the Technical Blog. Hugo exports determine the complete target list.
  Development covers active versions; release covers every published version and
  both archives, plus Community, Settings and the homepage.

Large indexes are split into ordered passage/vector files of at most 64 MiB;
the browser combines them using the manifest. Small indexes retain their original
single-file format. Generated index files and shared runtime assets belong in Git. `node_modules`,
embedding caches and intermediate Hugo exports are ignored. The core build owns
all shared static search files; archive builds own their HTML subtrees only.

## Rebuild

Run these from the repository root:

```sh
node tools/scripts/build-semantic-index.mjs --section archived-technical-blog
node tools/scripts/build-semantic-index.mjs --section openriak-kv --version 3.4.1
node tools/scripts/build-semantic-index.mjs --all
```

For a product, omitting `--version` rebuilds all its published versions. Unknown
sections/versions and conflicting selectors are rejected. Pinned dependencies
are installed automatically with `npm ci` only if generation requires them.
The first missing model/runtime preparation also requires network access.

The blog builder reads Markdown. Product indexes read rendered Hugo content,
including inherited pages and generated reference pages. When no existing build
is supplied, the command creates a fresh Hugo export under
`tools/generated/semantic-render/`, using local Hugo or the pinned Docker image.
It uses the release build profile unless `OPENRIAK_DOCS_BUILD_PROFILE` is set.
Hugo's configured draft settings determine which pages enter the product index.

To use the output of a build you have already completed:

```sh
node tools/scripts/build-semantic-index.mjs --section openriak-kv --version 3.4.1 \
  --site-dir /path/to/hugo-output
```

Rebuilds write and validate the new passage/vector files before replacing the
manifest. Superseded `passages-*.json` and `vectors-*.bin` files are then removed
from that target's directory. Other targets, runtime files and unrelated files
are untouched. To keep previous generations:

```sh
node tools/scripts/build-semantic-index.mjs --all --retain
```

`--retain` preserves the old files, but the manifest still selects the new index.
Commit additions and removals together after a rebuild.

## Build integration

Shell, PowerShell and Docker core builds run:

```sh
node tools/scripts/build-semantic-index.mjs --ensure --all \
  --site-dir /path/to/hugo-output --publish-dir /path/to/hugo-output
```

Missing manifests or referenced index files trigger generation. Existing indexes
are validated and reused without loading an embedding model or installing ML
packages. Corrupt or stale indexes fail the build with a rebuild instruction;
they are not silently overwritten. Newly generated files are copied into the
output after Hugo, so they are included in that same build. Generations retained
in the source are also included in the published output. Deployment assembly
checks the combined core and archive exports, so every published section is covered.

`docker/run.local.sh` builds the development image before starting containers.
The image contains pinned Node embedding dependencies and Hugo, with Hugo’s musl
libraries isolated from Node’s glibc environment. The core container prepares its
profile’s focused `semantic` Hugo exports (without rendering the HTML site twice),
runs the missing-index check, and then starts the server.
For release, it includes both archive exports before starting; the archive server
waits for core readiness. This ensures all shared static assets exist when Hugo starts.
This also runs on direct core-container restarts. An anonymous dependency volume is
initialised from the image and renewed by the run script when recreating containers;
host dependencies remain separate. There is no build-worker service or query server.

An intermediate source-only render sets `OPENRIAK_SEMANTIC_EXPORT_ONLY=1` to avoid
recursive index generation. This is an internal mechanism, not the normal build
mode. Docker performs conditional generation in a Node/glibc stage, since native
CPU inference dependencies must not run in the Alpine metadata stage.

## Model and passages

Both document and query embeddings use `Xenova/all-MiniLM-L6-v2`, revision
`751bff37182d3f1213fa05d7196b954e230abad9`, q8 ONNX weights, mean pooling and L2
normalisation (384 dimensions). `model.json` records the model configuration;
`runtime.json` records the served assets and their hashes.

Prose uses article/page title + section heading + three-sentence rolling windows,
advancing one sentence at a time. Windows stay within sections. Short sections
use their available sentences. Code, lists and tables are handled separately;
oversized inputs are split without dropping their tails. Each input stays within
256 model tokens, including its title and heading. Controls, navigation and
embedded metadata are excluded. KV deduplicates identical passages within the
same page and heading, which substantially reduces repetitive captured output.
Embeddings are cached by model revision and input text under
`tools/generated/semantic-cache/`. Prepared passages are also cached by their
content, title, model revision and chunking implementation, allowing unchanged
content to be reused across historical versions.

The browser loads the selected index and shared model on demand. A Web Worker
embeds only the query and compares it with prepared vectors. Semantic and text
rankings are combined, with one result per page. The blog index is approximately
14.2 MiB and KV 3.4.1 approximately 44.6 MiB; shared model/runtime assets add about
44 MiB on the first use. Browser caches can be evicted. Serve WASM as
`application/wasm` and JavaScript modules with a JavaScript MIME type.

## Tests

```sh
npm ci --prefix tools/semantic-search
node --test tools/semantic-search/manager.test.mjs tools/semantic-search/passages.test.mjs \
  tools/semantic-search/kv-source.test.mjs tools/semantic-search/ranking.test.mjs
node --test tools/semantic-search/discovery.test.mjs tools/semantic-search/startup.test.mjs tools/semantic-search/shards.test.mjs
node --test tools/semantic-search/export.test.mjs
node --test tools/semantic-search/missing-index.integration.test.mjs
node tools/semantic-search/preview.mjs
OPENRIAK_BROWSER_EXECUTABLE=/path/to/chromium node tools/semantic-search/browser.test.mjs
OPENRIAK_BROWSER_EXECUTABLE=/path/to/chromium node tools/semantic-search/kv-browser.test.mjs
node tools/semantic-search/evaluate.mjs
node tools/semantic-search/evaluate.mjs --kv
```

The blog browser test serves fixtures at domain root and `/docs/`. The KV test uses
`OPENRIAK_KV_TEST_BASE` (default `http://localhost:1410/docs/`). Tests check scope,
visible modes, exact terms, model failures and the 3.4.0 semantic endpoint.
Discovery/startup tests cover build profiles and startup ordering; the Hugo export
test checks domain-root/subdirectory deployment and generated Settings content.
The evaluation commands print example results for relevance review, not a claim
that one passage strategy is universally better.

Model and Transformers.js licences are Apache-2.0; ONNX Runtime is MIT. Licence
texts ship beside the runtime. Sources:
https://huggingface.co/Xenova/all-MiniLM-L6-v2 and
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2.
