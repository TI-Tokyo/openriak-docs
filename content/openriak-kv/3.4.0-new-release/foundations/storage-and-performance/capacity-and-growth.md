---
title: Capacity and growth
description: Cluster capacity must cover live data, replicated copies, indexes, retained history, and the temporary
  work needed to grow or recover. Steady-state disk occupancy alone is an incomplete sizing measure.
weight: 330
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\bitcask-capacity-calc.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\cluster-capacity.md
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/storage/capacity-planning.md
related:
- how-to/planning-a-deployment/size-a-cluster-and-reserve-recovery-headroom
- how-to/planning-a-deployment/check-production-readiness
- foundations/cluster-architecture/replica-placement-and-failure-domains
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
- how-to/performance/benchmark-a-representative-workload
---

Cluster capacity must cover live data, replicated copies, indexes, retained history, and the temporary work needed to grow or recover. Steady-state disk occupancy alone is an incomplete sizing measure.

## What consumes resources

Object count and key size affect per-key metadata. Value size affects transfer and storage. Index terms add write and query work. Siblings, tombstones, and obsolete backend records can make stored data larger than the application's current logical dataset.

Memory needs depend on the backend as well as on caches, concurrent requests, and background processes. CPU and network needs depend on access patterns, replication, and repair, not only on stored bytes.

## Headroom is part of usable capacity

When a node fails, survivors must absorb work and help restore redundancy. Membership changes also move partitions and can temporarily retain both old and new copies. A cluster that fits only when every node is healthy cannot necessarily complete its own recovery.

## Growth over time

Measure distributions as well as averages: hot keys, uneven bucket sizes, and a few large objects can concentrate work. Forecast growth to the next expansion window, then test that expansion and a representative failure while application traffic continues.
