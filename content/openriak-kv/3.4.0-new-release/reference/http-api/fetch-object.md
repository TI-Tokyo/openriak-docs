---
title: Fetch object
description: Fetch an ordinary object by its type, bucket, and key. The response includes its value and metadata,
  or identifies a missing value, siblings, or a failed request.
weight: 420
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\fetch-object.md
source_material:
- legacy-3.2.5
- live-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#accessing-legacy-objects
- https://openriak.github.io/riak/ObjectAPI.html#http-api-definition---fetch
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/fetch-object.md
related:
- how-to/application-data/read-an-object-and-handle-missing-values
- how-to/application-data/resolve-concurrent-object-updates
- reference/data-model-contracts/object-metadata
- reference/data-model-contracts/causal-context-and-version-vector-representations
- reference/http-api/object-request-options
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

Fetch an ordinary object by its type, bucket, and key. The response includes its value and metadata, or identifies a missing value, siblings, or a failed request.

## Request

`GET /types/TYPE/buckets/BUCKET/keys/KEY`

For the untyped namespace, omit `/types/TYPE`. `HEAD` requests representation metadata without the value body. Common request options are defined in [Object request options]({{< product-version-root >}}reference/http-api/object-request-options/).

## Response

A normal `200` response carries the content type, value, and `X-Riak-Vclock`. Preserve that context for an update. `404` denotes a missing object for the read; deletion context can be requested where supported.

When siblings exist, request `Accept: multipart/mixed` to receive their individual content and metadata. A `300` response can otherwise list sibling identifiers; a `vtag` request selects a specific sibling representation. Selecting one sibling is not itself a resolution of the conflict.

## Conditional reads

Use standard read validators only for cache validation and handle `304` without expecting a new body. Conditional write semantics are specified separately in [Conditional requests and latch objects]({{< product-version-root >}}reference/http-api/conditional-requests-and-latch-objects/).

## Example

```sh
curl -i -H 'Accept: multipart/mixed' "$RIAK_HTTP/buckets/customers/keys/aiko"
```
