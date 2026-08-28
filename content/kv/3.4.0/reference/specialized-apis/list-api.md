---
title: 'List API reference'
description: 'Define List API operations, streaming behavior, limits, and errors.'
weight: 3
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
  - 'https://openriak.github.io/riak/OtherAPI.html#the-list-api'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define List API operations, streaming behavior, limits, and errors.

## Details

### The List API

The list API supports the listing of keys and buckets.  The List API is deprecated in Riak 3.4, the [AAE Fold API](/kv/3.4.0/reference/aae-fold-api/) should be used instead, with the fold functions [`list_buckets`](/kv/3.4.0/reference/aae-fold-api/list-buckets/), [`find_keys`](/kv/3.4.0/reference/aae-fold-api/find-keys/) and [`find_tombs`](/kv/3.4.0/reference/aae-fold-api/find-tombstones/).

The APIs are unchanged since Riak 2.2.3, so refer to the legacy documentation for information on [list keys](https://docs.riak.com/riak/kv/2.2.3/developing/api/http/list-keys/index.html) o [list buckets](https://docs.riak.com/riak/kv/2.2.3/developing/api/http/list-buckets/index.html).

> The use of list keys or list buckets may have a critical impact on the performance of production clusters.  The AAE Fold alternatives are safe to use on production systems as long as two copies of the result-set can be held within available memory on a single node.
