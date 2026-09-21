---
title: Limits and behavioural constraints
description: The Query API operates over supported binary secondary indexes and partition-local snapshots. Supported
  field combinations are validated by the release's query implementation.
weight: 820
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
- operators
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/QueryAPI.html#aggregation-of-combination-queries
- https://openriak.github.io/riak/QueryAPI.html#buffering
- https://openriak.github.io/riak/QueryAPI.html#central-collation-of-query-results
- https://openriak.github.io/riak/QueryAPI.html#filtering
- https://openriak.github.io/riak/QueryAPI.html#notes-on-implementation
- https://openriak.github.io/riak/QueryAPI.html#performance-and-efficiency
- https://openriak.github.io/riak/QueryAPI.html#scanning
- https://openriak.github.io/riak/QueryAPI.html#setup-and-distribute-the-query
- https://openriak.github.io/riak/QueryAPI.html#transformation-of-results
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/query-api/limits.md
related:
- reference/configuration/query-execution-settings
- reference/query-api/endpoints-and-request-schema
- reference/query-api/accumulation-modes
- reference/query-api/continuations-and-result-delivery
- how-to/performance/reduce-query-api-cost
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-consistency-and-snapshots
---

The Query API operates over supported binary secondary indexes and partition-local snapshots. Supported field combinations are validated by the release's query implementation.

## Behavioural limits

- A combination query requires numbered constituent queries and a valid aggregation expression.
- Accumulation and pagination combinations are restricted; consult the mode and delivery references.
- Returned keys do not reserve object versions for a later fetch.
- A query does not establish an atomic snapshot across vnodes or clusters.
- A timeout or terminated result queue is an error condition, not a successful empty answer.

## Resource limits

Query execution competes for backend, worker, memory, and network resources. Returning a small result does not bound the number of entries scanned. Use a bounded range and an explicit result-delivery strategy when the possible result is large.

The generated query settings catalogue lists published configuration controls. Avoid relying on an internal application environment variable as a stable public setting unless it is documented for the selected release.
