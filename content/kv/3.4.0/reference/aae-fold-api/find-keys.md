---
title: 'Find keys operation'
description: 'Document parameters, filters, response fields, limits, and risks for the find keys operation.'
weight: 6
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
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
  - 'https://openriak.github.io/riak/OtherAPI.html#find_keys'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document parameters, filters, response fields, limits, and risks for the find keys operation.

## Details

### find_keys

Outputs a list of keys in the bucket where the object has either a sibling_count or a size (in bytes) that exceeds a certain threshold, potentially limited by key range or modified date range.

- Commonly used as an operational query (e.g. "find all objects modified in the past 24 hours with more than one sibling").
- May also be used to list keys, where using a `$key` query is not supported.  It is much slower (but potentially safer) than `$key` query due to the constraints of the [node_worker_pools](/kv/3.4.0/how-to/operate/monitor-worker-pools/).
- Uses the AF4 queue when running node worker pools in `dscp` mode.
