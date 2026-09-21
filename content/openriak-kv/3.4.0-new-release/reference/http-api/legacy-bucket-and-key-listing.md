---
title: Legacy bucket and key listing
description: Legacy bucket and key listing scans stored data and can consume substantial cluster resources. It is
  not a bounded query or a transactional inventory.
weight: 540
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\list-buckets.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/list-buckets.md
- reference/http-api/list-keys.md
related:
- how-to/data-inspection-and-repair/inventory-buckets-using-aae-folds
- reference/protocol-buffers-api/legacy-listing-messages
- reference/aae-fold-api/list-buckets
- how-to/indexes-and-queries/add-and-query-secondary-indexes
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

Legacy bucket and key listing scans stored data and can consume substantial cluster resources. It is not a bounded query or a transactional inventory.

## Endpoints

`GET /types/TYPE/buckets?buckets=true`

`GET /types/TYPE/buckets/BUCKET/keys?keys=true`

The untyped equivalents omit `/types/TYPE`. Streaming forms use the endpoint's streaming option and can return multiple chunks; consume the full response and its completion indication.

## Limits

Listings can be large, can reflect concurrent changes, and do not necessarily include empty buckets. Prefer secondary indexes for application discovery and bounded AAE inventory for operations. A listing failure is not evidence that a bucket contains no data.
