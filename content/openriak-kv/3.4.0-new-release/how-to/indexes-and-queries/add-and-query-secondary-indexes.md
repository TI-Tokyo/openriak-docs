---
title: Add and query secondary indexes
description: Attach secondary-index terms to an object and query them using a backend that supports indexes. Check
  [[R5]] before changing the application.
weight: 540
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\secondary-indexes.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/query-secondary-indexes.md
related:
- how-to/application-data/update-an-object-with-causal-context
- how-to/indexes-and-queries/run-exact-and-range-queries-with-the-query-api
- tutorials/indexes-and-querying/build-and-query-a-people-search-index
- reference/http-api/secondary-index-queries
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-cost-and-result-delivery
---

Attach secondary-index terms to an object and query them using a backend that supports indexes. Check [Backend capability matrix]({{< product-version-root >}}reference/orientation-and-compatibility/backend-capability-matrix/) before changing the application.

## Write indexed metadata

```sh
curl --fail -i -X PUT "$RIAK_HTTP/buckets/people/keys/aiko" -H 'Content-Type: application/json' -H 'X-Riak-Index-city_bin: Tokyo' -H 'X-Riak-Index-age_int: 29' --data-binary '{"name":"Aiko","city":"Tokyo","age":29}'
```

Use `_bin` for binary terms and `_int` for integer terms. On updates, preserve causal context and send the full intended index metadata; changing only the JSON body does not automatically update an index from its fields.

## Run an exact or range query

```sh
curl --fail "$RIAK_HTTP/buckets/people/index/city_bin/Tokyo"
curl --fail "$RIAK_HTTP/buckets/people/index/age_int/20/39"
```

Expect `aiko` among the returned keys. Fetch the object separately when the application needs its value. Encode index terms correctly in URLs.

## Verify updates and limits

Update the object's city and index together, then confirm the key disappears from the old term and appears under the new one. Use bounded ranges and pagination for large result sets. For projection, combination, or accumulation use [Run exact and range queries with the Query API]({{< product-version-root >}}how-to/indexes-and-queries/run-exact-and-range-queries-with-the-query-api/) and the Query API.
