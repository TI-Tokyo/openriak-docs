---
title: Secondary-index queries
description: The secondary-index HTTP interface returns object keys matching an exact term or an inclusive range
  on an index-capable backend.
weight: 500
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\secondary-indexes.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/secondary-indexes.md
related:
- how-to/indexes-and-queries/add-and-query-secondary-indexes
- reference/data-model-contracts/secondary-index-terms-and-projected-attributes
- reference/protocol-buffers-api/secondary-index-query-messages
- reference/query-api/endpoints-and-request-schema
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

The secondary-index HTTP interface returns object keys matching an exact term or an inclusive range on an index-capable backend.

**Deprecated since OpenRiak KV 3.4.** This legacy HTTP query interface is retained for compatibility. Use the [Query API]({{< product-version-root >}}reference/query-api/endpoints-and-request-schema/) for new binary-index queries. Secondary indexes themselves, including stored index metadata, are not deprecated. Check the Query API contract before migrating: it is not a drop-in replacement for every legacy request, including integer-index queries.

## Endpoints

`GET /types/TYPE/buckets/BUCKET/index/INDEX/TERM`

`GET /types/TYPE/buckets/BUCKET/index/INDEX/START/END`

Omit `/types/TYPE` for the untyped namespace. Encode each index term as one URL component. Binary and integer indexes use their respective term formats.

## Options and results

Results contain `keys`, or term/key results when `return_terms=true` is supported for the request. `max_results` bounds a page; a returned `continuation` is an opaque token for another request with the same query. Streaming uses the endpoint's streamed result framing rather than one ordinary JSON result.

The current Query API adds expression and combination features through a separate endpoint. Do not send its JSON schema to this legacy index path.

## Example

```sh
curl --fail "$RIAK_HTTP/buckets/people/index/age_int/20/39?max_results=100"
```
