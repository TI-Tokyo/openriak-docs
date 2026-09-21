---
title: Continuations and result delivery
weight: 810
product: OpenRiak KV
product_version: 3.4.1
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: OpenRiak KV 3.4.1 provides continuation requests and disk-backed queued results. Choose the delivery
  contract explicitly; a queue reference is not a continuation token.
related:
- reference/query-api/endpoints-and-request-schema
- reference/query-api/accumulation-modes
- reference/query-api/responses-and-errors
- how-to/indexes-and-queries/retrieve-paginated-or-asynchronous-query-results
- tutorials/indexes-and-querying/retrieve-a-larger-result-set
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-consistency-and-snapshots
---

OpenRiak KV 3.4.1 provides continuation requests and disk-backed queued results. Choose the delivery contract explicitly; a queue reference is not a continuation token.

## Continuations

For a supported single-query accumulation, pass `max_results` and follow `X-Riak-Continuation` by supplying its opaque value in the next request's `continuation` field. Preserve the original query definition.

## Queued results

Submit a query using `queue_raw_keys` or `queue_raw_terms`. The response supplies `result_queue`. Retrieve a batch from the same bucket endpoint with an HTTP GET and the query parameters `result_queue` and an explicit non-negative `max_results`.

```http
GET /types/{type}/buckets/{bucket}/query?result_queue={encoded-reference}&max_results={batch-size}
```

Encode the queue reference as a query-parameter value. Multiple consumers may fetch through connected nodes; retrieval consumes results rather than replaying an immutable page.

## Progress and lifecycle

Batch responses include result data and progress fields `returned_count`, `queued_count`, and `query_complete`. An empty batch while the query is incomplete is not final completion. Continue until the query has completed and its queued results have been drained.

The queue has execution and inactivity limits and is not a durable application message broker. If the result server has terminated, retrieval returns HTTP `410`. A consumer failure after retrieval can lose results from that consumer's workflow; make downstream processing and recovery explicit.
