---
title: Bucket-type operations
weight: 480
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: HTTP exposes properties of existing bucket types. Type creation and activation are administrative operations,
  not object writes or implicit side effects of addressing a typed bucket.
related:
- reference/configuration/bucket-properties-and-defaults
- reference/data-model-contracts/buckets-and-bucket-types
- how-to/application-data/create-and-activate-bucket-types
- how-to/application-data/use-bucket-types-in-an-application
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

HTTP exposes properties of existing bucket types. Type creation and activation are administrative operations, not object writes or implicit side effects of addressing a typed bucket.

## Properties

```http
GET /types/{type}/props
PUT /types/{type}/props
Content-Type: application/json
```

A property update uses a JSON object with a `props` member. Applicable property validation and lifecycle restrictions are shared with the bucket-type administration interface. URL-encode the type name and authenticate when security is enabled.

## Creation and activation

Use the {{< cli key="shell:riak admin bucket-type create" >}} and {{< cli key="shell:riak admin bucket-type activate" >}} administrative operations. An application's normal bucket write does not create and activate a new type.

## Typed buckets

Object paths under a type include `/types/{type}/buckets/{bucket}/keys/{key}`. An untyped path refers to another namespace; it is not shorthand for an arbitrary active type.
