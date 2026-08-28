---
title: 'Find tombstones operation'
description: 'Document parameters, filters, response fields, limits, and risks for the find tombstones operation.'
weight: 7
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
  - 'https://openriak.github.io/riak/OtherAPI.html#find_tombs'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document parameters, filters, response fields, limits, and risks for the find tombstones operation.

## Details

### find_tombs

Outputs a list of tombstone keys (deleted keys where the tombstone has not been reaped) in the bucket, potentially limited by key range or modified date range.

- Uses the AF4 queue when running node worker pools in `dscp` mode.
