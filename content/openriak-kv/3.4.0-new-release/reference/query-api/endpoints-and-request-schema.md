---
title: Endpoints and request schema
description: Submit a Query API request as JSON to a bucket's query endpoint. The backend must support the selected
  query operation and the bucket must contain the required index entries.
weight: 770
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/QueryAPI.html#api-endpoint---the-uri
- https://openriak.github.io/riak/QueryAPI.html#continuation-optional
- https://openriak.github.io/riak/QueryAPI.html#inactivity_timeout-optional
- https://openriak.github.io/riak/QueryAPI.html#max_results-optional
- https://openriak.github.io/riak/QueryAPI.html#query_list-required
- https://openriak.github.io/riak/QueryAPI.html#query---definition
- https://openriak.github.io/riak/QueryAPI.html#query-json---definition
- https://openriak.github.io/riak/QueryAPI.html#substitutions-optional
- https://openriak.github.io/riak/QueryAPI.html#timeout-optional
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/query-api/request.md
related:
- reference/query-api/expression-grammar-and-operators
- reference/query-api/accumulation-modes
- reference/query-api/responses-and-errors
- reference/query-api/continuations-and-result-delivery
- how-to/indexes-and-queries/run-exact-and-range-queries-with-the-query-api
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-consistency-and-snapshots
---

Submit a Query API request as JSON to a bucket's query endpoint. The backend must support the selected query operation and the bucket must contain the required index entries.

## Endpoint

```http
POST /types/{type}/buckets/{bucket}/query
Content-Type: application/json
```

The untyped form is `/buckets/{bucket}/query`. Percent-encode namespace components. When security is enabled, use the authenticated connection and the required secondary-index permissions.

## Request fields

{{< configuration-reference-table reference="query-fields" >}}{{< /configuration-reference-table >}}

Each query entry contains a binary index name and inclusive range boundaries. `aggregation_tag` identifies a constituent query in a combination. `evaluation_expression`, `filter_expression`, and `regular_expression` control candidate evaluation; use the expression reference for their grammar.

## Minimal example

These are deliberate example index names, terms, and accumulation choices:

```json
{
  "accumulation_option": "keys",
  "query_list": [{
    "index_name": "family_bin",
    "start_term": "Ng",
    "end_term": "Ng"
  }]
}
```

Malformed JSON, unknown request fields, missing required fields, or invalid combinations are rejected. Do not use older design notes that label an implemented field “not yet implemented” in preference to the release's validation contract.
