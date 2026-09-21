---
title: Buckets and bucket types
description: A bucket type supplies a named property policy for buckets in its namespace. A bucket supplies the
  second part of the object address; it is not a separately allocated table that must be created before the first
  object.
weight: 340
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\buckets-and-types.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\bucket-types.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/data/buckets-and-bucket-types.md
related:
- reference/configuration/bucket-properties-and-defaults
- reference/http-api/bucket-property-operations
- reference/http-api/bucket-type-operations
- how-to/application-data/create-and-activate-bucket-types
- foundations/data-and-consistency/bucket-types-and-data-policies
---

A bucket type supplies a named property policy for buckets in its namespace. A bucket supplies the second part of the object address; it is not a separately allocated table that must be created before the first object.

## Namespaces

Typed operations include `TYPE`, `BUCKET`, and `KEY`. Untyped operations use the legacy/default namespace. Type definitions must be created and activated before typed operations; bucket contents are created through writes. Identical bucket and key bytes in different types do not address the same object.

## Policy and lifecycle

The settings reference lists property names, types, and defaults. Type creation, inspection, activation, and update use the command catalogue below. Some properties, including datatype and consistency choices, have lifecycle restrictions; do not assume every property can be changed on an active populated type.

{{< cli-command-index prefix="riak/admin/bucket-type" >}}

## Replication scope

Object replication does not provision the receiving cluster's bucket types or security policy. Matching definitions must exist separately at each destination. Bucket-level overrides and their reset semantics are specified in [Bucket property operations]({{< product-version-root >}}reference/http-api/bucket-property-operations/).
