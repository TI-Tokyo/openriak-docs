# OpenRiak KV Markdown integration review

Generated: 2026-08-28 (Asia/Tokyo)

## Result

The destination is a Hugo-compatible, renderer-independent Markdown content tree.

- Markdown pages and unique routes: 776
- OpenRiak KV 3.4.0 pages: 385
- OpenRiak KV 3.4.1 pages: 390
- Cross-version selector pages: 1
- Hugo section branch bundles using _index.md: 87
- Internal page and anchor links checked: 5,290
- External source links observed: 1,449
- Referenced static image assets: 49
- Structural errors: 0
- Review warnings: 0

## Markdown and front matter

Every page uses Markdown with YAML front matter. Section ordering uses Hugo's weight field. Section landing pages use _index.md, and the three explicit version-root destinations use Hugo url fields. No Docusaurus packages, configuration, directives, imports, sidebar fields, or pagination fields are present in the destination.

The remaining custom fields, such as diataxis, product_version, audience, status, technical_review, and source provenance, are ordinary YAML data and do not require a particular renderer.

## Repairs made during integration review

- Normalized 457 heading levels across 361 pages where mixed source documents skipped a level or introduced a body-level title.
- Replaced 206 obsolete or missing section fragments across 78 pages with valid page-level destinations.
- Corrected two malformed bucket-namespace links to target the existing Buckets as Namespaces section.
- Copied 49 referenced image assets from the read-only WSL source into static/images.

## Version structure

OpenRiak KV 3.4.0 has no page that is absent from 3.4.1. Five capability pages occur only in 3.4.1:

- explanation/replication/accelerated-reconciliation.md
- how-to/develop/consume-queued-query-results.md
- how-to/operate/monitor-vm-statistics.md
- how-to/operate/resync-bucket.md
- reference/query-api/queued-results.md

## Editorial state

- 649 pages contain substantive migrated material rewritten into a unified page body.
- 127 source-free pages contain substantial, Diataxis-specific content specifications.
- All pages remain draft: true and technical_review: required until their version-specific technical claims are tested.

## Hugo build boundary

No Hugo configuration, module, or theme was supplied, so this review does not assume a theme or claim a rendered Hugo build. The content tree is ready to mount under a Hugo project's content/kv directory, with the accompanying static/images directory mounted under the project's static directory. A final Hugo build should be run once the site's URL policy, theme, menus, taxonomies, and Markdown renderer settings are defined.

## Issues

No structural errors or review warnings remain.