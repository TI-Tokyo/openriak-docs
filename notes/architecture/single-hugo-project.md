# Single Hugo project architecture

The homepage, product documentation, and Archived Technical Blog are rendered by one Hugo project configured at `content/hugo.yaml`. One Hugo server therefore owns every route below `/docs/`.

## Page families

- The homepage uses the portal home template.
- OpenRiak KV, CS, and TS are data-driven instances of the shared product templates. Product ID and version come from their mounted content paths and product data.
- The archive is a blog section with its own list, single-page, and base templates.

`layouts/docs-theme/` owns shared product navigation, product and version pickers, operating-system selection, search, breadcrumbs, version warnings, and metadata-aware shortcodes. `layouts/archive-technical-blog/` owns blog presentation. `layouts/portal/` owns the homepage.

## Product content layering

Hugo mounts product releases directly below their product/version URL. The OpenRiak KV 3.4.1 tree layers its changed pages over the 3.4.0 baseline; unchanged pages are inherited without source duplication. Historical releases use the same product templates and product-keyed data model.

## Data ownership

Authoritative metadata lives under `content/openriak-kv/metadata/{version}/`. `tools/scripts/sync-product-metadata.js` validates it and writes Hugo adapters under `tools/generated/`. Build tools never write under `content/`.

Product descriptors remain with authored product content. The unified Hugo configuration mounts them into a project-wide data map keyed by product ID, avoiding product-specific template copies.

## Runtime and production

Docker Compose starts one Hugo server on port 1410. Production invokes Hugo once, writes the complete site to `public/`, and serves that output from one Nginx container.
