---
title: Multiple backends and prefix routing
description: Multi-backend routing assigns different datasets to different local storage engines. A routing layer
  selects the backend; it does not combine their files into one interchangeable format.
weight: 300
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- architects
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\plan\Choosing-a-backend\multi.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\backend\multi.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#multi-backend
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-24'
review_scope: content changes
review-by: TI Tokyo/JOM
restructured_from:
- foundations/storage/multi-backend.md
- foundations/storage/prefix-multi.md
related:
- reference/legacy-and-experimental-features/multi-backend-and-prefix-routing-settings
- how-to/legacy-and-specialist-workflows/maintain-multi-backend-and-prefix-routing
- how-to/storage-maintenance/migrate-to-another-storage-backend
- foundations/storage-and-performance/storage-backend-trade-offs
---

Multi-backend routing assigns different datasets to different local storage engines. A routing layer selects the backend; it does not combine their files into one interchangeable format.

## Policy-based routing

Different buckets can have different storage requirements. A routing configuration can associate data with named backend definitions, each with its own settings and resource use. Prefix routing selects an engine using the configured prefix rules.

## Why a route change is significant

Existing objects remain in the engine that stored them. Changing the selection rule can direct future requests elsewhere without migrating those objects, making data appear missing or separating newer writes from older state.

A migration therefore needs an explicit inventory, copy or replacement procedure, and verification. Switching back a route is not a universal rollback once writes have reached the new destination.

## Operational cost

Multiple engines share node memory, file descriptors, storage bandwidth, and recovery time. Each also brings its own compaction, persistence, and backup behaviour. A mixed deployment must account for the total resource use and for feature restrictions in each route.

Use the version specific legacy and specialist reference to check the availability and limitations of the particular routing implementation.
