---
title: 'Repair key range operation'
description: 'Document parameters, filters, response fields, limits, and risks for the repair key range operation.'
weight: 11
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
  - 'https://openriak.github.io/riak/OtherAPI.html#repair_keys_range'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document parameters, filters, response fields, limits, and risks for the repair key range operation.

## Details

### repair_keys_range

Available from Riak 3.0.8

Used to prompt read repair in a bucket, to fix an entropy problem within the cluster, potentially limited by key range or modified date range.

- Uses the `riak_kv_reader` queue, and consumption from that queue is constrained by having a single process per node handling queued repairs.
- The reader queue has a small in-memory part but a large on-disk part.  The `reader_overflow_limit` is not configurable via `riak.conf`.
- Uses the AF4 queue when running node worker pools in `dscp` mode.
