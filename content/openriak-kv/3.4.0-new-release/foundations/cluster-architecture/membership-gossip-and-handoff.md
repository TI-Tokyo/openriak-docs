---
title: Membership, gossip, and handoff
description: Cluster membership records which nodes participate and how partitions are owned. Gossip spreads ring
  information between nodes; handoff moves the data needed when ownership changes.
weight: 70
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: reviewed
draft: true
audience:
- operators
- architects
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/RiakTheoryGuide.html#riak-core-cluster-management
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-24'
review-by: TI Tokyo/JOM
review_scope: Editorial & technical
restructured_from:
- foundations/operations/ring-changes-and-handoffs.md
related:
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
- how-to/cluster-lifecycle/monitor-and-control-handoffs
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
- reference/operations-and-observability/handoff-states-and-transfer-records
---

Cluster membership records which nodes participate and how partitions are owned. Gossip spreads ring information between nodes; handoff moves the data needed when ownership changes.

## Agreement and movement are separate

A planned join, leave, or replacement changes the intended ownership. Reviewing and committing the plan establishes the transition to perform. Data still has to move, so membership state and handoff progress must both be checked before treating the operation as complete.

## Handoff during normal changes and failures

Ownership handoff transfers a partition to its new permanent owner. Hinted handoff returns work held by a fallback node after a primary node recovers. Repair transfers can reconstruct data from surviving replicas. These activities share resources with application requests, even though their purposes differ.

## Why one change affects other work

Moving partitions consumes disk and network capacity and changes the set of processes serving the affected data. Overlapping maintenance can remove copies that are still needed for a previous recovery. Pausing or limiting transfers can protect client latency, but it also extends the period before placement settles.
