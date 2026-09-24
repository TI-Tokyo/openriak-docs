---
title: Rings, partitions, and virtual nodes
description: The ring divides the keyspace into partitions. A virtual node, or vnode, manages one partition on a
  physical node. Each physical node normally hosts many vnodes.
weight: 40
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- architects
- operators
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\clusters.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\architecture.md
source_material:
- legacy-3.2.5
- live-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#ring-size
- https://openriak.github.io/riak/RiakTheoryGuide.html#the-ring---the-distribution-of-vnodes
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-23'
review-by: TI Tokyo/JOM
review_scope: editorial and technical review
restructured_from:
- foundations/foundations/clusters-rings-and-partitions.md
- foundations/foundations/virtual-nodes.md
related:
- foundations/cluster-architecture/replica-placement-and-failure-domains
- foundations/cluster-architecture/membership-gossip-and-handoff
- how-to/planning-a-deployment/choose-a-ring-size
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
---

The ring divides the keyspace into partitions. A virtual node, or vnode, manages one partition on a physical node. Each physical node normally hosts many vnodes.

## From a key to responsible partitions

OpenRiak hashes an object's bucket and key to locate it on the ring. A preference list identifies the partitions responsible for replicas. Different objects spread across those partitions, distributing storage and request work across the cluster.

A vnode is an Erlang process with a backend store and partition-specific responsibilities. Adding a physical node redistributes partition ownership; it does not create a new ring for each node.

## Ring size and node count

Ring size fixes the number of partitions in the cluster. Node count determines how those partitions are shared across the nodes. More partitions can allow finer placement, but also add stores, processes, trees, and maintenance work. Ring size is therefore an initial deployment decision, not a request-level performance switch.

## Ownership changes

During a membership change, the old owner transfers partition data to the new owner through handoff. A node appearing in membership does not mean all data transfers have completed. Temporary fallback ownership during a failure is also distinct from permanent membership.

The ring is a placement structure; it does not impose a global order on object updates.
