---
title: Delete object
description: Delete an ordinary object identified by type, bucket, and key. The operation can retain a tombstone;
  it is not a request to immediately erase all physical storage.
weight: 440
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\delete-object.md
source_material:
- legacy-3.2.5
- live-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#http-api-definition---delete
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/delete-object.md
related:
- how-to/application-data/delete-an-object
- reference/data-model-contracts/deletion-tombstone-and-expiration-states
- reference/http-api/object-request-options
- reference/aae-fold-api/reap-tombstones
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

Delete an ordinary object identified by type, bucket, and key. The operation can retain a tombstone; it is not a request to immediately erase all physical storage.

## Request

`DELETE /types/TYPE/buckets/BUCKET/keys/KEY`

Omit `/types/TYPE` for the untyped namespace. Supply the observed `X-Riak-Vclock` when deleting a known state. Request acknowledgement options use the object-policy contract in [Object request options]({{< product-version-root >}}reference/http-api/object-request-options/).

## Response and limits

A successful delete returns an empty acknowledgement. A subsequent read normally reports missing once deletion is visible, but concurrent writes or stale replicas need the usual conflict and repair handling. A timeout is not proof that the deletion did not occur.

Reaping deletion evidence is a separate AAE operation with stronger retention preconditions.

## Example

```sh
curl -i -X DELETE "$RIAK_HTTP/buckets/customers/keys/aiko" -H "X-Riak-Vclock: $VCLOCK"
```
