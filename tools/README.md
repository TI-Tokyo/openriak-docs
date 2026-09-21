# Tools

- `scripts/` — split production builds, assembly, architecture checks, metadata synchronization, and link validation.
- `generated/` — generated Hugo data adapters; safe for build tools to rewrite.

The main build entry points are `tools/scripts/build.sh` and
`tools/scripts/build.ps1`. Both accept `development`, `beta-test`, or `release`.
Development builds core with one selected historical Riak KV version, the newest
legacy Riak CS and Riak TS versions, and every OpenRiak version. Beta-test builds
the complete core project, and release additionally builds the archives before
`assemble-site.sh` validates ownership and combines them into `public/`.

`tools/scripts/generate-version-mounts.js` scans the flat product/version
directories and expands their cumulative inheritance chains into
`tools/generated/hugo.yaml` before the core project starts. It also mounts the
newest release under each product's `latest` route and generates redirect-only
section roots in `tools/generated/latest-redirects/`. The legacy `riak-kv/latest`
route targets the newest `openriak-kv` release. `--include-version
SOURCE=VERSION` limits generated targets for one source family while preserving
the selected release's required inheritance layers; the development profile uses
this to select one `riak-kv` release. `--include-latest SOURCE` similarly limits
a source family to its highest semantic version; development uses it for
`riak-cs` and `riak-ts`.

Local `hugo server` runs also start `scripts/watch-page-provenance.js`. It
regenerates page-version provenance after Markdown pages are added, removed,
renamed, or edited, so new pages do not require restarting the Docker stack.
During the short regeneration window, a previously unseen page is treated as
new for its current version. Static builds still fail if generated provenance is
missing.

## Release metadata

The generator is maintained in the separate
[openriak-metadata repository](https://github.com/TI-Tokyo/openriak-metadata).
Run `kv-packages`, `kv-settings`, `kv-cli-commands`, `list`, then
`deploy --docs-root ../openriak-docs` from that checkout. Generation stages files
there; deployment copies validated JSON into this repository's
`content/openriak-kv/metadata/VERSION/` directory.

This repository owns the deployed metadata, Hugo adapters, and page rendering.
Docs builds consume the deployed JSON and do not require the generator checkout.
The generator's `kv-cli-commands` uses its own bundled Markdown hints and runtime
discovery. Only `deploy` needs a docs checkout; its default is the sibling
`openriak-docs` repository.

## CLI reference pages

After deploying complete CLI metadata, generate the version's command pages:

```sh
node tools/scripts/generate-cli-pages.js --version 3.4.0
node tools/scripts/generate-cli-pages.js --version 3.4.0 --check
```

The generator creates an index and one page per command topic under
`content/openriak-kv/3.4.0-new-release/reference/commands/`. Aliases share a
page, Erlang arities share a function page, and AAE selectors have child pages.
Authored companion pages are preserved. Generated stubs use Hugo shortcodes;
`sync-product-metadata.js`, run by the normal build, prepares their display data
from the deployed metadata. No discovery containers run during a docs build.

The page's `cli_reference_version` pins the inventory it describes. When a later
docs version inherits these pages, they still identify their original reference
version. Deploy that release's metadata and generate its pages to update it.

Run normalization and generation checks with
`node --test tools/scripts/cli-reference.test.js`. The optional
`tools/scripts/cli-reference.browser.test.cjs` uses Playwright against a built
site; set `OPENRIAK_CLI_TEST_URL` to the command index and, if needed,
`OPENRIAK_BROWSER_EXECUTABLE` to a Chromium executable.

## OpenRiak KV Docker metadata

Docker configurations are generated from the authoritative KV operating-system
and package metadata, then built and tested only when an operator explicitly
runs `openriak-docker refresh`. Documentation builds consume published records
under `records/openriak-docker/images/` and verify their associated artifacts
before advertising downloads. The separate tool updates this checkout through
`openriak-docker publish --docs-root PATH`. See the
[openriak-docker repository](https://github.com/TI-Tokyo/openriak-docker) for
target selection, test coverage, and publication details.

## Importing Hugo 0.18 content

`scripts/import_hugo_018.py` converts an old Hugo content directory into the
modern structure used by this site. It converts each `section.md` plus
`section/` pair into `section/_index.md`, converts the version's `index.md` into
the root `_index.md`, discards the obsolete root `_index.md` search page when
both old index files are present, and promotes legacy menu labels and weights
to `linkTitle` and `weight` front matter. Underscore-prefixed Markdown fragments
remain in the content tree but are excluded from rendering and navigation.
Duplicate top-level YAML keys, which Hugo 0.18 accepted, are reduced to their
final value so modern Hugo can parse the page. If an export accidentally
appended a second complete copy of a page with the same title, that duplicate
document is discarded. Leading blank lines before YAML front matter are also
removed so modern Hugo recognizes the metadata. Other files are copied unchanged.

Import into a new release directory:

```sh
python3 tools/scripts/import_hugo_018.py /path/to/old/content/riak/2.1.0 \
  content/riak-kv/2.1.0-new-release
```

Validate without writing, or convert an already-copied directory:

```sh
python3 tools/scripts/import_hugo_018.py content/riak-kv/2.1.0-new-release --in-place --check
python3 tools/scripts/import_hugo_018.py content/riak-kv/2.1.0-new-release --in-place
```

The importer rejects duplicate menu identifiers, missing menu parents,
ambiguous output paths, and existing destinations. Run its tests with:

```sh
python3 tools/scripts/import_hugo_018_test.py
```

## Diátaxis content checks

The implemented page inventory is `notes/reports/diataxis-page-map.json`. Run
`node --test tools/scripts/diataxis.test.js` after moving or renaming pages to
check both versions' topic paths, related links, workflow steps, and metadata
references. `tools/scripts/diataxis.browser.test.cjs` checks the rendered tables,
workflow navigation, heading hierarchy, and mobile width using Playwright; set
`OPENRIAK_DOCS_TEST_URL` to the product root (for example,
`http://localhost:1410/docs/openriak-kv/`).

`kv-reference.json` contains supplemental API contracts and lookup tables with
release-pinned source references. Hugo mounts these files as data so changes
refresh in the development server. They supplement the deployed settings, CLI,
and package JSON; they do not replace those authoritative inputs. Regenerate
protocol definitions and metric aliases from the pinned release modules when
updating them, and review authored descriptions against that release.

After a Hugo build with drafts, run
`python3 tools/scripts/check-diataxis-links.py PATH_TO_HUGO_OUTPUT` to check
rendered modern-version article links and anchors. It fails if no complete
modern-version output is present.
