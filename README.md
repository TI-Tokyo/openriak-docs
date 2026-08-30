# OpenRiak documentation site

This repository builds the OpenRiak homepage, versioned product documentation, and Archived Technical Blog as one Hugo 0.165.0 project.

## Repository layout

- `content/` — the unified Hugo project, authored content, and static site assets.
- `docker/` — container build, runtime, and local-preview configuration.
- `layouts/` — shared themes, templates, Hugo modules, and vendored modules.
- `notes/` — architecture notes and retained migration or validation reports.
- `public/` — generated merged production output.
- `tools/` — build, validation, and release-metadata tooling.

## Content and metadata

Production KV Markdown is layered beneath `content/openriak-kv/`:

- `releases/3.2.5/` is the historical Riak KV baseline.
- `releases/3.4.0/` is the OpenRiak KV 3.4 baseline.
- `layers/3.4.1/` contains only pages added or changed in 3.4.1; unchanged pages are inherited from 3.4.0.

Release metadata under `content/openriak-kv/metadata/{version}/` is authoritative for supported operating systems, package downloads, and replaceable configuration values. `tools/scripts/sync-product-metadata.js` validates and generates the compact browser/Hugo adapters in `tools/generated/openriak-kv/data/versions/`. Build tools do not write under `content/`.

## Build

Install the extended Hugo release in `.hugo-version`, plus Node.js when metadata adapters need regeneration.

PowerShell:

```powershell
.\tools\scripts\build.ps1 -BaseURL 'https://www.openriak.org/docs/'
```

Linux or WSL:

```sh
HUGO_BASEURL=https://www.openriak.org/docs/ INCLUDE_DRAFTS=true ./tools/scripts/build.sh
```

The merged site is written to `public/`, with each product under its product-first URL directory.

Run the strict architecture, metadata, SemVer, fallback, missing-value, search, and layered-output checks with:

```powershell
.\tools\scripts\build-architecture.ps1
```

## Local preview

Start the complete site with one Hugo server:

```sh
./docker/run.local.sh
```

The complete site is available below `http://localhost:1410/docs/`.

## Container image

The production image regenerates metadata, builds the merged site, and serves it with Nginx:

```sh
docker build -f docker/Dockerfile --build-arg HUGO_BASEURL=https://www.openriak.org/docs/ -t openriak-docs .
```

Migrated pages remain drafts until their technical reviews are complete. Set `INCLUDE_DRAFTS=false` for publication once the relevant front matter has been approved.
