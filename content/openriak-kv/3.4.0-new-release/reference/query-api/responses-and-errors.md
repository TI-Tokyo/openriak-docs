---
title: Responses and errors
description: 'A successful synchronous query returns JSON whose field corresponds to its accumulation mode: keys,
  terms, counts, or grouped counts. A continuation, when present, is returned in the `X-Riak-Continuation` response
  header'
weight: 800
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
- openriak-discussions
quickdocs_sources:
- https://openriak.github.io/riak/QueryAPI.html#query-responses
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/query-api/responses.md
related:
- reference/query-api/accumulation-modes
- reference/query-api/continuations-and-result-delivery
- reference/http-api/http-conventions-authentication-and-errors
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-consistency-and-snapshots
---

A successful synchronous query returns JSON whose field corresponds to its accumulation mode: keys, terms, counts, or grouped counts. A continuation, when present, is returned in the `X-Riak-Continuation` response header.

## Results

Key results contain object identifiers, not complete object bodies. Term results associate terms with keys. Count results are numbers; grouped counts associate an accumulation term with its count. Fetching a returned object is a separate request that may observe newer state.

## Errors

The HTTP resource returns JSON error information for request validation and execution failures. An invalid request is rejected before execution. A query timeout returns HTTP `503`; other execution failures can return HTTP `500` with an error description. Authentication and authorization failures follow the shared HTTP security contract.

A timeout is not an empty result and should not be stored as a successful zero count. Preserve the request and response when diagnosing a failure.

## Ordering and completion

Use the continuation contract to retrieve another page. Do not infer that another page exists from the response length alone, or treat a returned key list as a cross-cluster snapshot.
