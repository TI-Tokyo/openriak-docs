---
title: 'Reap tombstones operation'
description: 'Document parameters, filters, response fields, limits, and risks for the reap tombstones operation.'
weight: 10
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
  - 'https://openriak.github.io/riak/OtherAPI.html#reap_tombs'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document parameters, filters, response fields, limits, and risks for the reap tombstones operation.

## Details

### reap_tombs

Prompts for a list of matching tombstones in the bucket to be erased via the `riak_kv_reaper`, potentially limited by key range or modified date range.

- Uses the `riak_kv_reaper` queue, and consumption from that queue is constrained by having a single process per node handling queued repairs, and by the configuration of the `tombstone_pause` within riak.conf.
- The queue has a small in-memory part but a large on-disk part.  The size of the on-disk component is controlled in `riak.conf` via `reaper_overflow_limit`.
- Uses the AF4 queue when running node worker pools in `dscp` mode.
