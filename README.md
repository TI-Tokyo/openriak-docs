# OpenRiak documentation site

This repository produces one static OpenRiak website from two independently
cacheable Hugo 0.165.0 projects.

- The **core** project contains the homepage, Community, and versioned product documentation.
- The **archives** project contains the immutable Archived Technical Blog and Archived Mailing List.
- An assembly step combines both outputs into `public/` for rsync deployment.

Shared layouts, navigation data, and assets remain under `layouts/` and
`content/static/`. The core build is the only owner of shared static output;
the archive build may emit files only below its two archive URL directories.

## Repository layout

- `content/` — authored content, the core `hugo.yaml`, and `hugo-archives.yaml`.
- `docker/` — split local preview and cacheable production builds.
- `layouts/` — shared and section-specific templates.
- `notes/` — architecture notes and retained migration or validation reports.
- `public/` — the assembled static output.
- `tools/` — build, validation, assembly, and release-metadata tooling.

## Content and metadata

Production KV Markdown uses flat version directories in two source families:

- `content/riak-kv/{version}/` contains historical Riak KV versions from 2.0.0 up to, but not including, 3.4.0.
- `content/openriak-kv/{version}/` contains OpenRiak KV versions beginning at 3.4.0.
- Earlier versions in the same source family are inherited automatically; inheritance never crosses the 3.4.0 boundary.

Release metadata under `content/openriak-kv/metadata/{version}/` is authoritative
for supported operating systems, package downloads, and replaceable configuration
values. Build tools generate browser/Hugo adapters under `tools/generated/` and
never write under `content/`.

## Build

The Docker build caches the immutable archives independently from active content:

```sh
./docker/build.static.sh
```

This writes the complete assembled site to `public/`. Product-only changes reuse
the archive image layer. A change to shared or archive templates correctly
invalidates the archive layer.

With local Hugo 0.165.0 and Node.js installed, the equivalent uncached build is:

```sh
HUGO_BASEURL=https://www.openriak.org/docs/ INCLUDE_DRAFTS=true ./tools/scripts/build.sh
```

PowerShell users can run `tools/scripts/build.ps1`. Both entrypoints build the two
projects and assemble the same `public/` layout.

## Local preview

```sh
./docker/run.local.sh
```

The gateway exposes the complete site at `http://localhost:1410/docs/`. Core and
archive Hugo servers rebuild independently behind it. Archive live reload is
disabled because the archive corpus is immutable; refresh after rebuilding it.
The archive output persists under `build/archives/`, so the archive service can
be stopped after a successful render and the gateway will continue serving it.

## Runtime container

Build the production Nginx image with:

```sh
docker build -f docker/Dockerfile --build-arg HUGO_BASEURL=https://www.openriak.org/docs/ -t openriak-docs .
```

The image contains the same assembled static site below `/docs/`. Public servers
do not require Hugo, Node.js, or multiple containers.
