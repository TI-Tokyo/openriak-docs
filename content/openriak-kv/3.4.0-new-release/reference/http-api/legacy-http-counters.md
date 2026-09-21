---
title: Legacy HTTP counters
description: Legacy HTTP counters use a different interface from counters in an active datatype bucket type. The
  legacy interface is deprecated; new code should use [[R48]].
weight: 550
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\counters.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/counters.md
related:
- how-to/application-data/update-distributed-counters
- reference/http-api/distributed-data-type-operations
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

Legacy HTTP counters use a different interface from counters in an active datatype bucket type. The legacy interface is deprecated; new code should use [Distributed data-type operations]({{< product-version-root >}}reference/http-api/distributed-data-type-operations/).

## Endpoint

`GET /buckets/BUCKET/counters/KEY` fetches the counter.

`POST /buckets/BUCKET/counters/KEY` applies a signed integer increment in the request body.

The bucket policy must permit the legacy counter's merge behaviour. A counter increment is not a set-to-value operation, and replaying an uncertain update can increment again.

## Migration boundary

Do not assume changing the URL converts a legacy counter into a typed counter. Read and verify the old value, define the new type and initialization policy, and coordinate writers during migration.
