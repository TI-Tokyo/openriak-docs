---
title: 'Legacy Query API reference'
description: 'Record the legacy query interface, compatibility boundaries, and migration guidance.'
weight: 6
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#legacy-query-api'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Record the legacy query interface, compatibility boundaries, and migration guidance.

## Details

### Legacy Query API

Prior to the introduction of the [Riak Query API](/kv/3.4.0/tutorials/query-api/), there existed a simple REST-based API for querying index entries in Riak.  This API is deprecated, use of the Query API is preferred to support new queries.

The binary secondary indexes supported by the legacy index queries, are compatible with the new Query API - anything that could be queried and filtered in the old API can be achieved using the expressions in the new API.

The functionality of the legacy query API is unchanged since Riak 2.2.3, so refer to the [legacy documentation](https://docs.riak.com/riak/kv/latest/developing/usage/secondary-indexes/index.html) for further information.

> The legacy API had an undocumented feature that the query attribute `term_regex` could be used to pass regular expressions to filter terms from query results within the range.  This feature is replicated in the new Query API using the `regular_expression` option.
