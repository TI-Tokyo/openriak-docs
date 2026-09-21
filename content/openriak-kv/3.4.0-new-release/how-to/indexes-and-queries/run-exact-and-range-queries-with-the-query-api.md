---
title: Run exact and range queries with the Query API
description: Run exact and inclusive range queries through the Query API on a Leveled-backed bucket. The API queries
  stored index terms; it does not infer indexes from JSON fields.
weight: 550
diataxis: how-to
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
- https://openriak.github.io/riak/QueryAPI.html#secondary-indexes---querying-index-entries-overview
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/query-with-query-api.md
related:
- how-to/indexes-and-queries/filter-queries-using-projected-attributes
- how-to/indexes-and-queries/combine-queries-and-accumulate-results
- how-to/indexes-and-queries/retrieve-paginated-or-asynchronous-query-results
- reference/query-api/endpoints-and-request-schema
- reference/query-api/responses-and-errors
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-cost-and-result-delivery
---

Run exact and inclusive range queries through the Query API on a Leveled-backed bucket. The API queries stored index terms; it does not infer indexes from JSON fields.

## Prepare indexed data

Use [Add and query secondary indexes]({{< product-version-root >}}how-to/indexes-and-queries/add-and-query-secondary-indexes/) to write a `city_bin` term or load the small fixture in [Build and query a people-search index]({{< product-version-root >}}tutorials/indexes-and-querying/build-and-query-a-people-search-index/). Set `RIAK_HTTP` to the intended endpoint.

## Submit an exact query

```sh
curl --fail -X POST "$RIAK_HTTP/buckets/people/query" -H 'Content-Type: application/json' --data-binary '{"accumulation_option":"keys","query_list":[{"index_name":"city_bin","start_term":"Tokyo","end_term":"Tokyo"}]}'
```

Use different `start_term` and `end_term` values for an inclusive range, matching the index's integer or binary type. See [Endpoints and request schema]({{< product-version-root >}}reference/query-api/endpoints-and-request-schema/) for the exact request schema.

## Check the result

Confirm the returned keys match a known fixture before using a larger range. A query result is not an atomic snapshot of every object subsequently fetched. Handle errors and continuations explicitly, and limit expensive ranges or accumulated output using [Retrieve paginated or asynchronous query results]({{< product-version-root >}}how-to/indexes-and-queries/retrieve-paginated-or-asynchronous-query-results/) and [Reduce Query API cost]({{< product-version-root >}}how-to/performance/reduce-query-api-cost/).
