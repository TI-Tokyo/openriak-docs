---
title: Store object
description: Store an ordinary object's value and metadata at a supplied or server-assigned key. Supply causal context
  when replacing an observed version.
weight: 430
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\store-object.md
source_material:
- legacy-3.2.5
- live-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#http-api-definition---store
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/store-object.md
related:
- how-to/application-data/create-and-store-an-object
- how-to/application-data/update-an-object-with-causal-context
- reference/data-model-contracts/object-metadata
- reference/data-model-contracts/causal-context-and-version-vector-representations
- reference/http-api/conditional-requests-and-latch-objects
- reference/http-api/object-request-options
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

Store an ordinary object's value and metadata at a supplied or server-assigned key. Supply causal context when replacing an observed version.

## Requests

`PUT /types/TYPE/buckets/BUCKET/keys/KEY`

`POST /types/TYPE/buckets/BUCKET/keys`

Omit `/types/TYPE` for the untyped namespace. PUT selects the key; POST to the collection asks the server to assign it. The request body is the value, with content type and optional user/index metadata in headers.

## Context and conditions

`X-Riak-Vclock` carries the state observed by the writer. Without that context, a write can be concurrent with existing versions. Creation-only and version-conditional writes use [Conditional requests and latch objects]({{< product-version-root >}}reference/http-api/conditional-requests-and-latch-objects/). Request-level acknowledgement options are in [Object request options]({{< product-version-root >}}reference/http-api/object-request-options/).

## Responses

A normal successful store without a returned body acknowledges with `204`. A server-assigned key is reported with `201` and a `Location` header. `returnbody=true` requests the resulting object representation where applicable. A failed condition returns `412`; a timeout leaves the outcome potentially uncertain.

## Example

```sh
curl -i -X PUT "$RIAK_HTTP/buckets/customers/keys/aiko" -H 'Content-Type: application/json' --data-binary '{"name":"Aiko"}'
```
