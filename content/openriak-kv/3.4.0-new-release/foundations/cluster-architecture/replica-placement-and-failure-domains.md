---
title: Replica placement and failure domains
description: Replica placement determines which failures can remove all copies of an object. Copies on different
  partitions are useful only to the extent that their physical nodes and failure domains remain independent.
weight: 60
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/foundations/intra-cluster-resilience.md
related:
- foundations/data-and-consistency/quorums-availability-and-durability
- foundations/storage-and-performance/capacity-and-growth
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
- reference/operations-and-observability/claim-algorithms-and-placement-constraints
- how-to/planning-a-deployment/choose-replication-and-acknowledgement-policies
---

Replica placement determines which failures can remove all copies of an object. Copies on different partitions are useful only to the extent that their physical nodes and failure domains remain independent.

## Partitions, nodes, and locations

An object's preference list identifies its replica partitions. Placement algorithms distribute ownership across nodes and can take location information into account. A location represents an operational failure boundary, such as a rack or availability zone; it must reflect the deployment's actual topology.

When a primary owner is unavailable, a fallback can temporarily accept work under the applicable policy. A fallback copy helps availability, but it is not the same as an acknowledgement from a primary replica.

## Correlated failures

Three example replicas on three machines do not protect against losing the single rack that powers all three. Similarly, replicas in one cluster do not replace off-cluster backups or a tested disaster-recovery strategy.

## Recovery needs spare resources

After a failure, the surviving nodes must continue serving clients while accepting redistributed work and rebuilding copies. Storage capacity, network bandwidth, and backend write capacity must include that recovery load. Running every node at its steady-state limit leaves no margin for repair.
