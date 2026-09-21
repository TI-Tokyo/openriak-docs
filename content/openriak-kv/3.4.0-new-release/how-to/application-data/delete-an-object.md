---
title: Delete an object
description: Delete an object using the context of the version the application intends to remove. Deletion can retain
  a tombstone for replication and repair.
weight: 420
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\deleting-objects.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#example-delete-request
- https://openriak.github.io/riak/ObjectAPI.html#http-api-definition---delete
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/delete-object.md
related:
- how-to/application-data/update-an-object-with-causal-context
- how-to/data-inspection-and-repair/locate-tombstones
- how-to/data-inspection-and-repair/reap-eligible-tombstones
- reference/http-api/delete-object
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/bucket-types-and-data-policies
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Delete an object using the context of the version the application intends to remove. Deletion can retain a tombstone for replication and repair.

## Fetch the current context

Read the object and retain `X-Riak-Vclock` as in [Update an object with causal context]({{< product-version-root >}}how-to/application-data/update-an-object-with-causal-context/). If siblings exist, decide whether the operation should remove their combined state or resolve them first. Do not silently treat an authentication or timeout error as a missing key.

## Delete and verify

```sh
curl --fail -i -X DELETE "$RIAK_HTTP/buckets/customers/keys/aiko" -H "X-Riak-Vclock: $VCLOCK"
curl -i "$RIAK_HTTP/buckets/customers/keys/aiko"
```

Expect a successful delete followed by a missing-object response once the deletion is visible. Repeat the check at replication destinations when they are part of the requirement. A delete does not immediately reclaim every byte on disk.

If a value reappears, inspect concurrent writes and retained deletion context before issuing repeated deletes. Use [Reap eligible tombstones]({{< product-version-root >}}how-to/data-inspection-and-repair/reap-eligible-tombstones/) for controlled tombstone reclamation after replicas and destinations have observed the deletion.
