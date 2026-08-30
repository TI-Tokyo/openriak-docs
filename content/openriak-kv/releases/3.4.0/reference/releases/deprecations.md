---
title: 'Deprecated features in OpenRiak KV 3.4.0'
description: 'List deprecated 3.4.0 features, preferred alternatives, compatibility implications, and possible future removal.'
weight: 6
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
  - 'developers'
source_material:
  - 'legacy-3.2.5'
  - 'source-code-release-notes-3.4'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\deprecated\riak-search.md'
  - 'Deprecated or historical feature material is retained for context and must not imply current support.'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

List deprecated 3.4.0 features, preferred alternatives, compatibility implications, and possible future removal.

## Details

### Riak Search

[riak 2.9.10]: https://www.tiot.jp/riak-docs/riak/kv/2.9.10/
[config 2.9.10-search]: https://www.tiot.jp/riak-docs/riak/kv/2.9.10/configuring/search/

Riak Search (aka Yokozuna) using Solr is deprecated in this version. The last version with support was OpenRiak KV 2.9.10. Check out [OpenRiak KV 2.9.10][riak 2.9.10], and it's [Riak Search config page][config 2.9.10-search].

The recommended method of performing searches in Riak is to use secondary indexes (2i) and map-reduce with regex.
