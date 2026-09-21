---
title: Bucket types and data policies
description: Bucket types group buckets under a named namespace and shared properties. They let an application make
  data-policy choices explicitly instead of relying on one cluster-wide policy for every object.
weight: 90
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- developers
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/data-model/bucket-types.md
related:
- how-to/application-data/create-and-activate-bucket-types
- how-to/application-data/use-bucket-types-in-an-application
- reference/configuration/bucket-properties-and-defaults
- reference/data-model-contracts/buckets-and-bucket-types
---

Bucket types group buckets under a named namespace and shared properties. They let an application make data-policy choices explicitly instead of relying on one cluster-wide policy for every object.

## Policies belong to the data model

Replica count, acknowledgement behaviour, sibling handling, and data-type selection affect the contract an application implements. A bucket for mergeable counters has different requirements from a bucket for arbitrary binary objects. Select the policy before writing application data.

## Creation and activation

A type is created, validated, and activated before clients use its namespace. Activation makes the type usable; it is not a migration of objects from an untyped bucket. Applications must include the type in subsequent requests.

Not every property can be changed safely after activation. Some combinations are constrained by the data type or backend. The bucket-property reference records the applicable fields and constraints.

## Policy changes do not rewrite history

Changing how future writes are handled does not resolve existing siblings, convert stored objects into another data type, or move data to a different backend. Such changes require an explicit data migration and verification plan.

Keep policy definitions under configuration management and test client behaviour against the effective properties of the intended namespace.
