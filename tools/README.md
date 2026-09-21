# Tools

- `scripts/` — split production builds, assembly, architecture checks, metadata synchronization, and link validation.
- `openriak-metadata/` — Python release-metadata CLI and tests. Run `kv-packages`,
  `kv-settings`, `kv-cli-commands`, `list`, then `deploy` to stage and inspect results before copying
  them into the Hugo metadata folder; see its [workflow guide](openriak-metadata/README.md).
- `openriak-docker/` — compatibility launchers for the separate runtime-image tool repository.
- `cache/openriak-docker/` — retained Dockerfiles, Compose files, JSON reports, and per-run test logs.
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

## OpenRiak KV Docker cache

Docker configurations are generated from the authoritative KV operating-system
and package metadata, then built and tested only when an operator explicitly
runs `openriak-docker refresh`. Documentation builds consume passed cached
results and never pull base images or run containers. The separate tool updates
this checkout only through `openriak-docker publish --docs-root PATH`. See
`openriak-docker/README.md` for target selection, cache layout, test coverage,
and publication details.

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
