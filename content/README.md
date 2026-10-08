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

## Feature and concept tags

Documents may declare multiple tags of each type in their YAML front matter:

```yaml
features: [handoff, cluster-management]
concepts: [partition-transfer, node-lifecycle]
```

Use lowercase identifiers with hyphens, reusing the vocabulary on
`/docs/tags/feature/` and `/docs/tags/concept/`. Features identify capabilities;
concepts identify the ideas a document explains. Assign tags to the document's
subject, not every term it mentions. These lists are independent of legacy
untyped `tags` lists and of source repository/module annotations.

The header displays linked tags beside the reading time. Each shared tag page
lists matching documents grouped by product and mounted release. Inherited
pages retain their tags, so tag a shared 3.4.0 source page rather than copying it
into 3.4.1. Release-specific replacements must declare their own lists.

The initial tagging covers OpenRiak KV 3.4.0 and 3.4.1. Older releases and archives
are not retrospectively tagged. Command-page regeneration preserves this model
by deriving `features` and `concepts` from the command annotations. Versioned
reference indexes also include these front-matter lists, alongside the separate
repository and module tags.
