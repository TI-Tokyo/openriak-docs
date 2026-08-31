# Content

The repository has two Hugo projects that are assembled into one static site:

- `hugo.yaml` mounts the homepage, Community, and versioned OpenRiak/Riak product content.
- `hugo-archives.yaml` mounts the Archived Technical Blog and Archived Mailing List.

Product version mounts are expanded into the generated core configuration before
each core build. Archive content is deliberately absent from that configuration,
so active documentation changes do not make Hugo process 18,642 mailing-list
messages.

The core project owns all shared and page-family web assets under `static/`.
The archive project owns only its generated content and mailing-list search index.
Both projects mount common templates and site-section data directly from
`layouts/common-docs/`; common code is not duplicated.

Each direct semantic-version product directory is a cumulative content layer over
earlier versions in that source product. Everything under `content/` is
user-maintained source. Build tools must not create or modify files here;
generated Hugo inputs belong under `tools/generated/`.
