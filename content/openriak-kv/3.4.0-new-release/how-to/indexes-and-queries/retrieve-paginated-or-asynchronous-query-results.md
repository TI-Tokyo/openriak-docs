---
title: Retrieve paginated or asynchronous query results
weight: 580
product: OpenRiak KV
product_version: 3.4.0
diataxis: how-to
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Retrieve a larger query result using the delivery mechanism supported by the selected release. Keep
  the query definition and namespace stable between requests.
related:
- reference/query-api/continuations-and-result-delivery
- reference/query-api/accumulation-modes
- tutorials/indexes-and-querying/retrieve-a-larger-result-set
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-cost-and-result-delivery
---

Retrieve a larger query result using the delivery mechanism supported by the selected release. Keep the query definition and namespace stable between requests.

## Continuation-based retrieval

1. Submit a supported single query with an explicit `max_results` and compatible accumulation mode.
2. Save the response body and inspect the `X-Riak-Continuation` header.
3. If present, submit the same query with that opaque value as the JSON `continuation` field.
4. Continue until the response has no continuation header. Treat HTTP and JSON errors separately from an empty successful result.

Do not create or decode a continuation token yourself. Check results against a known dataset, including multiple entries for the same key, before using the loop in an application.

## Queued retrieval in 3.4.1

For releases supporting `queue_raw_keys` and `queue_raw_terms`, save `result_queue` from the initial response and retrieve batches with GET on the same bucket's query endpoint. URL-encode the queue reference and supply an explicit batch limit.

Track query completion and remaining queued results. An empty batch while the query is incomplete is not the end. Queue retrieval consumes results; define recovery for a consumer that fails after fetching a batch. Handle a terminated queue as an error requiring an application decision, not as a completed result.
