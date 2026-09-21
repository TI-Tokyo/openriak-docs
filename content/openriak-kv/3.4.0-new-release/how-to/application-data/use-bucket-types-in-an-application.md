---
title: Use bucket types in an application
description: Address the intended bucket type explicitly in application requests. The same bucket and key under
  another type identify a different object.
weight: 380
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\bucket-types.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/use-bucket-types.md
related:
- how-to/application-data/create-and-activate-bucket-types
- reference/data-model-contracts/buckets-and-bucket-types
- reference/http-api/bucket-type-operations
- reference/protocol-buffers-api/bucket-type-messages
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/bucket-types-and-data-policies
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Address the intended bucket type explicitly in application requests. The same bucket and key under another type identify a different object.

## Select an active type

Confirm the type exists and has the expected policy:

{{< cli-example key="shell:riak admin bucket-type status" args="documents" >}}

Use [Create and activate bucket types]({{< product-version-root >}}how-to/application-data/create-and-activate-bucket-types/) if it has not been created and activated. Do not silently fall back to the untyped namespace when a type is unavailable.

## Include it in the request

For HTTP object operations use `/types/TYPE/buckets/BUCKET/keys/KEY`. For distributed data types use `/types/TYPE/buckets/BUCKET/datatypes/KEY`. Encode each path component separately. In Protocol Buffers, populate the request's bucket-type field using a client that supports that message.

## Verify isolation

Write a sample through the typed path, read it back through the same path, and confirm that an untyped read does not accidentally become the application's fallback. Keep type names with the application's deployment configuration, and provision matching definitions in receiving clusters.
