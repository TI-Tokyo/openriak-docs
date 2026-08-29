# OpenRiak documentation site

This repository builds the versioned OpenRiak KV documentation with Hugo 0.165.0 and plain Markdown content.

## Preview locally

Install the extended Hugo release named in `.hugo-version`, then run:

```powershell
hugo server --buildDrafts --baseURL http://localhost:1313/docs/ --appendPort=false
```

Open `http://localhost:1313/docs/`. The migrated pages are intentionally marked as drafts until their technical reviews are complete, so `--buildDrafts` is required for the working preview.

The URL prefix is not fixed. For example, use `--baseURL http://localhost:1313/openriak-docs/` to preview the same site under `/openriak-docs/`, or `--baseURL http://localhost:1313/` to preview it at the domain root.

## Base-path-safe links

The default production URL is `https://www.openriak.org/docs/`, but the same source can be built for another domain and path. Ordinary Markdown site links are written with the `baseurl` shortcode:

```markdown
[Install OpenRiak]({{< baseurl >}}kv/3.4.1/how-to/install/)
```

Use the same prefix in raw HTML attributes, such as `href="{{< baseurl >}}kv/3.4.1/"` or `src="{{< baseurl >}}images/example.png"`. The shortcode emits only the path component of the configured `baseURL`: `/docs/`, `/openriak-docs/`, or `/`. Markdown render hooks also make any remaining root-relative links and images base-path safe.

## Admonitions

The site uses [hugo-admonitions](https://github.com/KKKZOZ/hugo-admonitions), pinned to v0.12.4 in `go.mod`. Its files are committed under `_vendor`, so preview and publication builds do not require Go, GitHub access, Sass, or Node.

Write callouts using portable blockquote syntax:

```markdown
> [!NOTE]
> This information helps readers complete the task safely.

> [!WARNING] Before changing the ring
> Verify that every node reports the expected cluster state.
```

The module supports additional types including `TIP`, `IMPORTANT`, `CAUTION`, `DANGER`, `INFO`, and `SUCCESS`, plus custom titles, nesting, and foldable callouts.

## HTTP-only Docker preview

The restored Docker wrapper runs the site without installing Hugo, Ruby, or Node locally. From the repository root, run either:

```powershell
.\docker\run.local.ps1
```

```sh
sh ./docker/run.local.sh
```

Then open `http://localhost:1314/docs/`. The service binds only to `127.0.0.1`, uses plain HTTP, includes drafts, watches for changes, renders in memory, and mounts the project read-only. Running `docker compose up` from the repository root starts the same preview configuration.

Set `HUGO_BASEURL` to preview another prefix:

```powershell
$env:HUGO_BASEURL = 'http://localhost:1314/openriak-docs/'
.\docker\run.local.ps1
```

```sh
HUGO_BASEURL=http://localhost:1314/openriak-docs/ sh ./docker/run.local.sh
```

## Build and validate

On Windows:

```powershell
.\scripts\build.ps1 -BaseURL 'https://www.tiot.jp/openriak-docs/'
.\scripts\validate-links.ps1
```

On Linux or WSL:

```sh
HUGO_BASEURL=https://www.tiot.jp/openriak-docs/ INCLUDE_DRAFTS=true ./scripts/build.sh
```

Set `IncludeDrafts` or `INCLUDE_DRAFTS` to false for a publication build after reviewed pages have `draft: false` in their front matter.

For the production image, pass the target URL as a build argument. The generated files are placed under the matching URL path inside Nginx:

```sh
docker build --build-arg HUGO_BASEURL=https://docs.openriak.org/ -t openriak-docs .
```

## Content organization

Content lives under `content/kv/<version>/`. Current OpenRiak versions use the four Diátaxis sections: `tutorials`, `how-to`, `reference`, and `explanation`. The historical Riak KV 3.2.5 tree preserves its original task-oriented hierarchy so existing page relationships remain intact. Keep version-specific facts within the matching version tree; do not share a page across versions unless its output is demonstrably identical.

The site uses Hugo's current template layout (`layouts/baseof.html`, `home.html`, `page.html`, `section.html`, `_partials`, and `_markup`) with no Docusaurus, Node, Ruby, or Sass build dependency.
