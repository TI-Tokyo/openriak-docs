---
title: 'List buckets operation'
description: 'Document parameters, filters, response fields, limits, and risks for the list buckets operation.'
weight: 8
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
  - 'developers'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#list_buckets'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document parameters, filters, response fields, limits, and risks for the list buckets operation.

## Details

### list_buckets

Returns a list of buckets, assuming the given n_val.

- The list may be incomplete if the passed n_val is greater than the configured n_val of some buckets.
- will only return buckets that contain objects.
- Uses a skipping cursor in both `native` and the `leveled_ko` type of parallel store, so that the fold is much more efficient than folding over all keys.
- Uses the AF4 queue when running node worker pools in `dscp` mode.
