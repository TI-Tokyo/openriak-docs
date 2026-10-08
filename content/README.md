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
user-maintained source. Build tools normally write generated Hugo inputs under `tools/generated/`.
Tag scaffolding is an exception: it creates missing draft Markdown tag pages here
without overwriting existing files.

## Feature and concept tags

Documents may declare multiple tags of each type in their YAML front matter:

```yaml
features: [handoff, cluster-management]
concepts: [partition-transfer, node-lifecycle]
```

Use lowercase identifiers with hyphens, reusing the vocabulary on
`/docs/openriak-kv/3.4.1/tags/feature/` and
`/docs/openriak-kv/3.4.1/tags/concept/` (substitute the selected product/release). Features identify capabilities;
concepts identify the ideas a document explains. Assign tags to the document's
subject, not every term it mentions. These lists are independent of legacy
untyped `tags` lists and of source repository/module annotations.

The header displays linked tags beside the reading time. Each tag page
lists only matching documents in that product and mounted release. The `tags/`
and `tags/feature/` or `tags/concept/` indexes support browsing; the entire tags
tree is excluded from sidebar menus and search results. Inherited
pages retain their tags, so tag a shared 3.4.0 source page rather than copying it
into 3.4.1. Release-specific replacements must declare their own lists.

The initial tagging covers OpenRiak KV 3.4.0 and 3.4.1. Older releases and archives
are not retrospectively tagged. Command-page regeneration preserves this model
by deriving `features` and `concepts` from the command annotations. Versioned
reference indexes also include these front-matter lists, alongside the separate
repository and module tags.

Tag pages are authored Markdown under each release's `tags/` directory. Every
referenced feature or concept must have a matching `tags/<type>/<tag>.md` (or
`tags/<type>/<tag>/_index.md`), together with `tags/_index.md` and its type index.
Inherited tag pages count as matching pages for the newer release.

Place `{{< tag-list >}}` wherever the list should appear, with explanatory text
before or after it. On a tag page this lists matching documents from the current
release; on an index page it lists its immediate child tag pages or types. The
`category` and `tag` front-matter fields identify an individual tag page.

Version mount generation collects document, command and settings tags and creates
missing Markdown pages directly in the appropriate content release directory.
New stubs use `draft: true`, include `{{< tag-list >}}`, and are excluded from sidebar
menus and search. Existing text and review status are never overwritten; inherited
pages are reused. Scaffolding does not stop the build. Draft tag pages are visible
in development and other builds using `--buildDrafts`.

All typed tags use `<product>/<version>/tags/<type>/<tag>/`, including `repository`
and `module`. Settings' original metadata tags use the separate `metadata` type.
Repository and module tags with the same name always have different pages.
