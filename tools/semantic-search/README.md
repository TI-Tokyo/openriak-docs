# Semantic search

Documentation versions, Community, Site Settings and both archives use pre-built document embeddings and
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
  both archives, plus Community, Site Settings and the homepage.

Large indexes are split into ordered passage/vector files of at most 45 MiB (below GitHub’s 50 MB warning threshold);
the browser combines them using the manifest. Small indexes retain their original
single-file format. Generated index files and shared runtime assets belong in Git. `node_modules`,
embedding caches and intermediate Hugo exports are ignored. The core build owns
all shared static search files; archive builds own their HTML subtrees only.

## Update indexes

Run these from the repository root:

```sh
node tools/scripts/build-semantic-index.mjs --section archived-technical-blog --all
node tools/scripts/build-semantic-index.mjs --section openriak-kv --version 3.4.1
node tools/scripts/build-semantic-index.mjs --all
```

Normal runs leave valid indexes unchanged and rebuild only missing, stale or
invalid indexes. Use `--force` to rebuild regardless of validity; unchanged text
can still reuse cached embeddings. Superseded generations are cleaned only when
an index is rebuilt, unless `--retain` is supplied.

`--section` accepts `openriak-kv`, `openriak-cs`, `openriak-ts`, `community`,
`settings`, `archived-technical-blog` or `archived-mailing-list`. It requires
`--all` or one or more `--version` arguments. Sections without versions use
`--all`. Global `--all` includes all published sections and versions, including
the homepage. Unknown sections, unavailable versions and conflicting selectors
are rejected before any index is changed.

```sh
node tools/scripts/build-semantic-index.mjs --section openriak-kv --version 3.4.0 --version 3.4.1
node tools/scripts/build-semantic-index.mjs --section openriak-kv --all
node tools/scripts/build-semantic-index.mjs --section settings --all
node tools/scripts/build-semantic-index.mjs --all --force
```

Pinned dependencies are installed with `npm ci` only if generation requires them.
The first missing model/runtime preparation also requires network access.

The blog builder reads Markdown. Product indexes read rendered Hugo content,
including inherited pages and generated reference pages. When no existing build
is supplied, the command creates a fresh Hugo export under
`tools/generated/semantic-render/`, using local Hugo or the pinned Docker image.
It uses the release build profile unless `OPENRIAK_DOCS_BUILD_PROFILE` is set.
Hugo's configured draft settings determine which pages enter the product index.

Stale Hugo indexes report the stored and current source fingerprints and the
export file used for comparison. Newly rebuilt indexes also record page
fingerprints, allowing subsequent checks to list added, removed or changed pages
(up to ten in the console). These diagnostics do not change freshness rules or
require existing indexes to be rebuilt.

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

## Check without rebuilding

```sh
OPENRIAK_DOCS_BUILD_PROFILE=release node tools/scripts/build-semantic-index.mjs --all --whatif
```

This reports `OK` or `WOULD REBUILD` for every selected index and continues after a
failure. It checks freshness, checksums, scope, passage counts, vector sizes and
shared-runtime compatibility. It never rebuilds indexes, repairs runtime files,
installs embedding dependencies or publishes assets. The exit status is 1 if any
index would be rebuilt or the shared runtime needs attention, otherwise 0.

Fresh Hugo source exports are rendered for comparison. To avoid that export,
add `--site-dir /path/to/hugo-output`; freshness is then checked against those
existing exports, which must cover the sections and versions you want to check.
Use the same selectors as a normal run. `--whatif --force` previews a forced
rebuild of every selected index. `--whatif` cannot be combined with
`--publish-dir`. The old `--check` option is replaced by `--whatif`; `--ensure`
is no longer needed because updating only when necessary is now the default.

Source fingerprints normalise site URLs without changing external documentation
links or literal paths. New indexes use normalisation version 3. Older manifests
can record a verified `sourceBaseURL`, allowing validation to reproduce their
original fingerprint rules at another deployment URL. Adding that provenance
requires an exact match against the existing digest; it does not make stale
indexes current or change any passages or vectors. `HUGO_BASEURL` and
`INCLUDE_DRAFTS` also apply to fresh what-if exports, including Docker exports.

## Build integration

Shell, PowerShell and Docker core builds run:

```sh
node tools/scripts/build-semantic-index.mjs --all \
  --site-dir /path/to/hugo-output --publish-dir /path/to/hugo-output
```

Builds use the same default update behaviour: missing, stale or invalid indexes
are regenerated and validated; valid indexes are reused without loading an
embedding model or installing ML packages. A failed generation or validation
stops the build. Generated assets are copied into the output after Hugo, so they
are included in that build. Generations retained in the source are also included
in the published output. Deployment assembly checks the combined core and archive
exports, so every published section is covered.

`docker/run.local.sh` builds the development image before starting containers.
The image contains pinned Node embedding dependencies and Hugo, with Hugo’s musl
libraries isolated from Node’s glibc environment. The core container prepares its
profile’s focused `semantic` Hugo exports (without rendering the HTML site twice),
updates indexes as needed, and then starts the server.
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
test checks domain-root/subdirectory deployment and generated Site Settings content.
The evaluation commands print example results for relevance review, not a claim
that one passage strategy is universally better.

Model and Transformers.js licences are Apache-2.0; ONNX Runtime is MIT. Licence
texts ship beside the runtime. Sources:
https://huggingface.co/Xenova/all-MiniLM-L6-v2 and
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2.

Site Settings and Archived Mailing List panels combine their specialised text results with the shared semantic client. They retain text search if the model or semantic index cannot load. Site Settings semantic results currently point to settings sections; exact text results can link to individual controls.

All semantic panels report download progress (file number and MiB), model preparation, search execution and elapsed time. Index, model and WASM downloads retry network failures, stalled transfers (30 seconds without data), HTTP 408/429 and server errors up to twice, after 1 and 2 seconds. Other HTTP errors, including 404/403, are not retried. Failed transfers restart the current file; completed index parts are retained for the current load. Exhausted retries retain text search.

Editing a query while the model loads reuses the current download and retains its progress display. The worker searches the latest queued query after initialisation. If the worker produces no progress or result for two minutes, it is terminated and the panel retains text search; keystrokes do not extend that deadline.

Search tolerates a single-letter edit or adjacent-letter transposition in an unknown word of at least five letters when a sufficiently common, unambiguous replacement occurs in section titles/headings. Exact indexed words and technical identifiers are preserved. Query expansion is applied to both lexical ranking and the query embedding; passage embeddings do not need rebuilding. Refocusing a search panel reopens existing results without rerunning the query.

Search status reserves two fixed rows: text-search progress and counts on the first, semantic progress on the second. Completed searches show “Semantic + text search” above the combined result count. Long messages stay on one row with an ellipsis; hovering reveals the full message.

## Per-section search preferences

`layouts/common-docs/data/search.json` configures the initial text/semantic switches and result timing for each site section. Both search types default to `true`; `timing` is `asap` or `together`. The same configuration is loaded by core and archive builds. Product preferences cover all versions, including legacy Riak URLs. The homepage is excluded.

Site Settings → Search presents these defaults with section logos and browser overrides. Overrides use `openriak-docs-search:SECTION` and participate in settings export, import and reset. Disabled types are not run; a disabled semantic search does not load its model or vectors. Disabling an active semantic search terminates its worker and aborts its index requests. Text search on documentation/blog pages still uses the existing passage index as its text corpus.

ASAP displays each enabled type's results as they arrive. Together waits for all enabled types to finish (including failure), so disabling one type does not cause an indefinite wait. Semantic-only results exclude lexical ranking. Inline links and the both-disabled choices save the selected section preference and rerun the current query.

Result highlighting is enabled by default per section (`highlight: true` in the shared search configuration). Site Settings → Search can override it independently of text/semantic search. Enabled results highlight literal query terms safely in titles/snippets and carry those terms to the destination page. Disabling highlighting removes both marks and highlight query parameters from new result links, while preserving other URL parameters and anchors.
