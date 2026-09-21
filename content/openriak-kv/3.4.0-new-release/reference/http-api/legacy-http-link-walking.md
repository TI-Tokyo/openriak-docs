---
title: Legacy HTTP link walking
description: Legacy link walking traverses link metadata stored on objects. It is deprecated; use explicit application
  relationships or indexes for new data models.
weight: 560
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\link-walking.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/link-walking.md
related:
- reference/data-model-contracts/object-metadata
- reference/http-api/fetch-object
- how-to/planning-a-deployment/map-application-data-to-objects-and-buckets
- how-to/indexes-and-queries/add-and-query-secondary-indexes
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

Legacy link walking traverses link metadata stored on objects. It is deprecated; use explicit application relationships or indexes for new data models.

## Request shape

A walk starts from an object path followed by one or more `BUCKET,TAG,KEEP` steps. Wildcard bucket or tag selectors broaden a step; the keep flag selects which step results are returned. Percent-encode literal path components and distinguish wildcard syntax from application data.

## Response and limits

Walk responses can be multipart and can contain multiple objects and sibling representations. Each step can increase work and response size. A traversal does not create a transaction or enforce referential integrity, and stored links are not automatically maintained when another object changes.

For ordinary object retrieval and metadata representation, use the references below.
