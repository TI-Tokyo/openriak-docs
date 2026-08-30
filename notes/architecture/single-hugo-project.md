# Single Hugo project architecture

The homepage, product documentation, and Archived Technical Blog are rendered by one Hugo project configured at `content/hugo.yaml`. One Hugo server therefore owns every route below `/docs/`.

## Page families

- The homepage uses the homepage template.
- OpenRiak KV, CS, and TS are data-driven instances of the shared product templates. Product ID and version come from their mounted content paths and product data.
- The archive is a blog section with its own list, single-page, and base templates.

`layouts/docs-theme/` owns shared product navigation, product and version pickers, operating-system selection, search, breadcrumbs, version warnings, and metadata-aware shortcodes. `layouts/archive-technical-blog/` owns blog presentation. `layouts/homepage/` owns the homepage.

## Product content layering

Versioned sources are flat directories such as `content/openriak-kv/3.4.1/`.
There are no special `releases/` or `layers/` directories. Every version is
a sparse layer over the earlier versions in the same source product.

`tools/scripts/generate-version-mounts.js` scans `riak-kv`, `openriak-kv`,
`openriak-cs`, and `openriak-ts` before each build. For each target version
it mounts matching source versions newest first, because Hugo resolves the
first matching file. Riak KV sources publish below `content/openriak-kv/` to
preserve existing URLs, but they never inherit from or into OpenRiak KV:
`riak-kv` stops below 3.4.0 and `openriak-kv` starts at 3.4.0.

## Data ownership

Authoritative metadata lives under `content/openriak-kv/metadata/{version}/`. `tools/scripts/sync-product-metadata.js` discovers the flat OpenRiak KV version directories, validates their metadata, and writes Hugo adapters under `tools/generated/`. Build tools never write under `content/`.

Product descriptors remain with authored product content. The unified Hugo configuration mounts them into a project-wide data map keyed by product ID, avoiding product-specific template copies.

## Runtime and production

Docker Compose starts one Hugo server on port 1410. Production invokes Hugo once, writes the complete site to `public/`, and serves that output from one Nginx container.
