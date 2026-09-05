# OpenRiak documentation site

This repository produces one static OpenRiak website from two independently
cacheable Hugo 0.165.0 projects.

- The **core** project contains the homepage, Community, and versioned product documentation.
- The **archives** project contains the immutable Archived Technical Blog and Archived Mailing List.
- An assembly step combines both outputs into `public/` for rsync deployment.

Shared layouts, navigation data, and assets remain under `layouts/` and
`content/static/`. The core build is the only owner of shared static output;
the archive build may emit files only below its two archive URL directories.

GitHub-style Markdown alerts are supported by the vendored admonition module in
both Hugo projects and in every build profile:

```markdown
> [!NOTE]
> Tagged releases contain a `rebar.lock` file.
```

Product documentation can insert the version being browsed with the text-only
`{{</* current-version */>}}` shortcode. It can be used as ordinary text, inside
inline code, or inside a fenced code block. Use
`{{</* current-version format="major-minor" */>}}` when only the major and minor
components are needed. For example:

````markdown
Version {{</* current-version */>}}

Release line {{</* current-version format="major-minor" */>}}

`riak-{{</* current-version */>}}`

```text
riak-{{</* current-version */>}}
```
````

Consecutive fenced code blocks with different language labels become language
tabs in product documentation. Text between blocks, unlabelled blocks, and
repeated languages end a tab group. The selected language is remembered in the
browser and selected in other groups where available. Code controls remain
available for each example; printing or disabling JavaScript shows every block.

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

## Build profiles

The same source tree supports three explicit profiles:

- `development` builds only core and mounts one historical Riak KV release. It defaults to `3.2.5`; set `OPENRIAK_DOCS_RIAK_KV_VERSION` to work on another imported release.
- `beta-test` builds only core, with every Riak KV and OpenRiak product release mounted.
- `release` builds all core releases and both archive projects, then assembles one deployment tree.

Docker static builds are selected by the first argument:

```sh
./docker/build.static.sh development
./docker/build.static.sh beta-test
./docker/build.static.sh release
```

All three write their selected artifact to `public/`. The release artifact is the
only one intended for rsync deployment.

## Release build

The Docker build caches the immutable archives independently from active content:

```sh
./docker/build.static.sh release
```

This writes the complete assembled site to `public/`. Product-only changes reuse
the archive image layer. A change to shared or archive templates correctly
invalidates the archive layer.

With local Hugo 0.165.0 and Node.js installed, the equivalent uncached build is:

```sh
HUGO_BASEURL=https://www.openriak.org/docs/ INCLUDE_DRAFTS=true ./tools/scripts/build.sh release
```

PowerShell users can run `tools/scripts/build.ps1`. Both entrypoints build the two
projects and assemble the same `public/` layout.

## Local preview

```sh
./docker/run.local.sh development
```

Use `./docker/run.local.sh beta-test` to preview all core releases, or
`./docker/run.local.sh release` to run core and archives together. The gateway
always listens at `http://localhost:1410/docs/`. In development and beta-test,
archive URLs use the last successful cached archive output when one exists; no
archive Hugo process is started.

## Runtime container

Build the production Nginx image with:

```sh
docker build -f docker/Dockerfile --build-arg HUGO_BASEURL=https://www.openriak.org/docs/ -t openriak-docs .
```

The image contains the same assembled static site below `/docs/`. Public servers
do not require Hugo, Node.js, or multiple containers.

### Downloads page shortcodes

OpenRiak KV Downloads pages control their section order in Markdown:

```markdown
## Recommended Downloads

{{< download-os-picker >}}
{{< package-downloads >}}
{{< docker-downloads >}}

{{< collapsable-section title="Source code" >}}
Source-code documentation goes here, including Markdown and other shortcodes.
{{< /collapsable-section >}}

{{< collapsable-section title="All Download Packages" id="all-downloads" >}}
{{< all-package-downloads >}}
{{< /collapsable-section >}}

{{< collapsable-section title="All Docker Files" id="all-docker-files" >}}
{{< all-docker-downloads >}}
{{< /collapsable-section >}}
```

The package and Docker recommendations follow the shared OS selection. Each
shortcode works independently of the all-download lists. Docker tables use only
published, passed cache data; displaying them does not run Docker tests.
Disclosures start collapsed; `title` sets the summary and optional `id` provides
an anchor. Optional `level="2"` renders the title as an `h2` (equivalent to `##`)
and includes it in “On this page”; levels 1 through 6 are supported and nested
accordingly. Without `level`, the title is not included in the table of contents.
These shortcodes use the version being viewed, including inherited pages.
