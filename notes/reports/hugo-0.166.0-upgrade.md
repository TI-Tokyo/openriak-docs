# Hugo 0.166.0 upgrade validation

Validated on 2026-09-16, upgrading from 0.165.0 to
[Hugo 0.166.0](https://github.com/gohugoio/hugo/releases/tag/v0.166.0).

The version pins in `.hugo-version`, `docker/Dockerfile`,
`docker/compose.yaml`, and `tools/scripts/build-architecture.ps1` now agree.
The README references were updated. No template or content migration was needed.

Official image tested:

```text
ghcr.io/gohugoio/hugo:v0.166.0
sha256:9f3cccb54b48e83a5468cd44f0372b10834b6d8418ef692d9821bb1314761829
```

## Validation

- Core release builds passed on both versions with drafts included and
  `--gc --minify --panicOnWarning --noBuildLock --cleanDestinationDir`.
  Both produced 18,212 pages, 25,645 aliases, and 658 static files.
- Both archive builds passed with the same flags: 5,879 pages,
  7 pagination pages, 50 aliases, and one static file. Release assembly
  passed its output-ownership and collision checks.
- `node tools/scripts/generate-version-mounts.test.js` passed.
- `node tools/scripts/architecture.test.js` passed its source/data checks.
  Its optional legacy fixture-output block was not activated.
- `node tools/scripts/metadata-loader.test.js` passed all five tests.
- `node tools/scripts/os-selection.test.js` passed.
- `docker compose -f docker/compose.yaml config --quiet` passed.
- `./docker/run.local.sh development -d` started the updated preview, rendering
  2,555 pages and 1,448 aliases with Hugo 0.166.0.
- `tools/scripts/search-highlight.browser.test.cjs` passed in Chromium:
  visible search matches, preserved language preferences, exact clipboard copy,
  clearing highlights, and archive/disclosure fallback.
- Additional browser checks passed for the homepage, 3.4.1 downloads and OS
  selection, the inherited 3.4.1 FAQ, and the historical 3.2.5 installation page,
  without JavaScript page errors.

The complete 0.166.0 release output was assembled into `public/`. The development
preview remains available at `http://localhost:1410/docs/`.

## Archive output comparison

All 5,937 archive output files are byte-for-byte identical between 0.165.0 and
0.166.0. No archive paths were added or removed. The detailed local result is
`build/hugo-0.166.0/archive-comparison.json`.

## Core output comparison

The same generated configuration and metadata were used to render the same
working-tree content with both official images. Each core output contains
59,707 files. All non-metadata paths are unchanged. There are 46 renamed
content-addressed metadata files and 47 changed HTML files:

- One homepage generator version label.
- Twenty-five pages referencing the renamed metadata files. Their metadata
  payloads differ only in Hugo's internal shortcode placeholder IDs.
- Two development overview pages whose heading IDs contain those placeholders.
- Eighteen legacy alias redirects with different winning destinations.
- One configuration reference page where the new Markdown renderer correctly
  excludes a closing parenthesis from an Erlang documentation URL.

No other core output differences were found. Detailed local comparisons are
under `build/hugo-0.166.0/` alongside the validation builds.

## Existing issues discovered during comparison

These issues are present in the 0.165.0 baseline and were not changed as part
of the version upgrade:

- Some code-copy JSON contains unresolved `HAHAHUGOSHORTCODE...HBHB` markers.
  The generated IDs vary between builds, changing the metadata filenames.
  The affected development overview headings also expose placeholders in IDs.
- Historical content declares conflicting aliases. For example,
  `content/riak-kv/2.0.0-new-release/using/admin/_index.md` and `commands.md`
  both claim `/openriak-kv/2.0.0/ops/running/cluster-admin`.
  Redirects to search JSON also occur in the old output. All 18 differing
  redirect targets exist, but these aliases need a separate cleanup to make
  their destinations unambiguous.

The pre-existing edits to the two OpenRiak KV release-note files were preserved
and included in both comparison builds.
