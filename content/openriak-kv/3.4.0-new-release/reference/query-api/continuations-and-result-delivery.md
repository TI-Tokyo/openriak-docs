---
title: Continuations and result delivery
weight: 810
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: OpenRiak KV 3.4.0 supports continuation-based retrieval for supported single-query accumulations. Disk-backed
  queued result retrieval is introduced in 3.4.1 and is not a 3.4.0 HTTP contract.
related:
- reference/query-api/endpoints-and-request-schema
- reference/query-api/accumulation-modes
- reference/query-api/responses-and-errors
- how-to/indexes-and-queries/retrieve-paginated-or-asynchronous-query-results
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-consistency-and-snapshots
---

OpenRiak KV 3.4.0 supports continuation-based retrieval for supported single-query accumulations. Disk-backed queued result retrieval is introduced in 3.4.1 and is not a 3.4.0 HTTP contract.

## Continuation requests

Supply an explicit positive `max_results` with a single query using `raw_keys` or `terms`. If the response contains `X-Riak-Continuation`, retain its value unchanged and supply it as the JSON `continuation` field in the next request.

Keep the bucket, index, range, expressions, and accumulation choices consistent. The token advances from a term/key position; it is not a global transaction or a durable application cursor across arbitrary query changes.

## Completion and failures

When no continuation header is returned, there is no further continuation from that response. Treat invalid tokens and execution errors as failures, not as successful completion. A continued request observes the query implementation's snapshot boundaries and can run while writes continue.

## 3.4.0 runtime limitation

Small-page Query API requests reproduced a query-server failure on the 3.4.0 Alpine 3.24 / OTP 26 learning image when a vnode returned an empty result batch. The request timed out instead of returning its next page. For a simple index range, use [Secondary-index queries]({{< product-version-root >}}reference/http-api/secondary-index-queries/) and its JSON continuation while this release issue is investigated. See [Retrieve a larger result set]({{< product-version-root >}}tutorials/indexes-and-querying/retrieve-a-larger-result-set/) for a working exercise. Do not retry the same failing query indefinitely or treat the timeout as the end of the result set.
