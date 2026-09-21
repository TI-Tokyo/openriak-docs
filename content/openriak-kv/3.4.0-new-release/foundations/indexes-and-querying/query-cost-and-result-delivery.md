---
title: Query cost and result delivery
description: Query cost depends on how many index entries are examined, what work is done per entry, and how much
  data is returned. A small result does not necessarily mean a cheap query.
weight: 200
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- performance-engineers
- architects
- developers
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/QueryAPI.html#aggregation-of-combination-queries
- https://openriak.github.io/riak/QueryAPI.html#buffering
- https://openriak.github.io/riak/QueryAPI.html#central-collation-of-query-results
- https://openriak.github.io/riak/QueryAPI.html#filtering
- https://openriak.github.io/riak/QueryAPI.html#performance-and-efficiency
- https://openriak.github.io/riak/QueryAPI.html#querying---non-functional-summary
- https://openriak.github.io/riak/QueryAPI.html#scanning
- https://openriak.github.io/riak/QueryAPI.html#setup-and-distribute-the-query
- https://openriak.github.io/riak/QueryAPI.html#transformation-of-results
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/performance/query-execution.md
related:
- foundations/storage-and-performance/latency-queues-and-resource-contention
- reference/query-api/accumulation-modes
- reference/query-api/continuations-and-result-delivery
- how-to/performance/reduce-query-api-cost
- tutorials/indexes-and-querying/retrieve-a-larger-result-set
---

Query cost depends on how many index entries are examined, what work is done per entry, and how much data is returned. A small result does not necessarily mean a cheap query.

## Scanning and filtering

A narrow ordered range reduces the candidates scanned. A selective filter applied after a broad scan can return few matches while still visiting many entries. Projected attributes can save object fetches, but they increase index size and evaluation work.

## Accumulation and transport

Returning counts or grouped counts can reduce response size. Returning every key or term consumes more memory, network capacity, and client processing. Duplicate handling also changes the required work and the meaning of a count.

Pagination bounds the amount delivered per response; it should not be assumed to eliminate the cost of the underlying search. Where a release supports queued delivery, disk-backed results change how consumers retrieve work and introduce queue lifecycle and completion requirements.

## Shared resources

Queries compete with writes, compaction, repair, and other queries. Measure tail latency and background progress as well as one isolated query's elapsed time. A useful performance experiment changes one range, projection, filter, or accumulation choice and checks that the answer remains correct.
