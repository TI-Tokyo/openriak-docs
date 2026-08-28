---
title: 'Downloads'
description: 'List supported OpenRiak packages, checksums, repositories, and source archives by platform and version.'
weight: 2
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\use\download.md'
migration_review:
  - 'Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.0 and require technical verification.'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#download-riak'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

List supported OpenRiak packages, checksums, repositories, and source archives by platform and version.

## Details

### Download Riak

Riak is [available to clone on GitHub](https://github.com/OpenRiak/riak).

Each major release has an associated branch which represents current development activity.  For Riak 3.2 this is `openriak-3.2`, For Riak 3.4 this is `openriak-3.4`.  Building from these branches may contain unreleased changes.

[Tagged versions for recent releases are available](https://github.com/OpenRiak/riak/releases), and described in the [release notes](https://github.com/OpenRiak/riak/blob/openriak-3.4/RELEASE-NOTES.md).  [Earlier releases are also available](https://github.com/OpenRiak/riak-forked/releases); and for the pre-OpenRiak era, [releases can be found on the basho github site](https://github.com/basho/riak/releases).

> Tagged releases contain a `rebar.lock` file which ensures all major dependencies are fetched from the precise commit made at the point of release.

> [!WARNING]
> Migration review required: Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.0 and require technical verification.
