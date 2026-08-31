# Tools

- `scripts/` — split production builds, assembly, architecture checks, metadata synchronization, and link validation.
- `openriak-metadata/` — Python release-metadata package, CLI, and tests.
- `generated/` — generated Hugo data adapters; safe for build tools to rewrite.

The main build entry points are `tools/scripts/build.sh` and
`tools/scripts/build.ps1`. Both accept `development`, `beta-test`, or `release`.
Development builds core with one selected historical Riak KV version, beta-test
builds the complete core project, and release additionally builds the archives
before `assemble-site.sh` validates ownership and combines them into `public/`.

`tools/scripts/generate-version-mounts.js` scans the flat product/version
directories and expands their cumulative inheritance chains into
`tools/generated/hugo.yaml` before the core project starts. It also mounts the
newest release under each product's `latest` route and generates redirect-only
section roots in `tools/generated/latest-redirects/`. The legacy `riak-kv/latest`
route targets the newest `openriak-kv` release. `--include-version
SOURCE=VERSION` limits generated targets for one source family while preserving
the selected release's required inheritance layers; the development profile uses
this to select one `riak-kv` release.

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
