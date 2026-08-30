# Tools

- `scripts/` — production builds, architecture checks, metadata synchronization,
  and link validation.
- `openriak-metadata/` — Python release-metadata package, CLI, and tests.
- `generated/` — generated Hugo data adapters; safe for build tools to rewrite.

The main build entry points are `tools/scripts/build.sh` and
`tools/scripts/build.ps1`.

`tools/scripts/generate-version-mounts.js` scans the flat product/version
directories and expands their cumulative inheritance chains into
`tools/generated/hugo.yaml` before Hugo starts.
