---
title: 'Object statistics operation'
description: 'Document parameters, filters, response fields, limits, and risks for the object statistics operation.'
weight: 9
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
  - 'https://openriak.github.io/riak/OtherAPI.html#object_stats'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document parameters, filters, response fields, limits, and risks for the object statistics operation.

## Details

### object_stats

Returns a summary of stats for objects within the bucket, potentially limited by key range or modified date range.

- Returns an output like `[{total_count, 1000}, {total_size, 1000000},  {sizes, [{1, 800}, {2, 180}, {3, 20}]},  {siblings, [{1, 1000}]}]`.
  - The sizes are the count of objects by order of magnitude in bytes (e.g. 1 is 10 -> 100 bytes, 2 is 100 -> 1000 bytes etc).
  - The siblings are the count of objects with that count of siblings.
- Uses the AF4 queue when running node worker pools in `dscp` mode.
