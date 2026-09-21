---
title: Bucket property operations
description: Bucket-property endpoints inspect, override, and reset the policy for one bucket. They do not create
  or delete its object contents.
weight: 470
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\get-bucket-props.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/get-bucket-properties.md
- reference/http-api/set-bucket-properties.md
- reference/http-api/reset-bucket-properties.md
related:
- how-to/application-data/create-and-activate-bucket-types
- how-to/application-data/use-bucket-types-in-an-application
- reference/configuration/bucket-properties-and-defaults
- reference/data-model-contracts/buckets-and-bucket-types
- reference/http-api/bucket-type-operations
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

Bucket-property endpoints inspect, override, and reset the policy for one bucket. They do not create or delete its object contents.

## Endpoints

`GET /types/TYPE/buckets/BUCKET/props` returns a JSON object containing `props`.

`PUT /types/TYPE/buckets/BUCKET/props` applies a JSON `props` object with the requested changes.

`DELETE /types/TYPE/buckets/BUCKET/props` resets bucket-level overrides where supported. Omit `/types/TYPE` for the untyped namespace.

## Property contract

Property names, types, and defaults are in [Bucket properties and defaults]({{< product-version-root >}}reference/configuration/bucket-properties-and-defaults/). Type-level and bucket-level constraints still apply; not every property is mutable on every active type. Read the effective properties after a change and handle validation errors explicitly.

## Example response shape

```json
{"props":{"allow_mult":true}}
```

This abbreviated example shows the envelope, not the complete returned property set or a default policy. Type administration is specified in [Bucket-type operations]({{< product-version-root >}}reference/http-api/bucket-type-operations/).
