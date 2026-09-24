---
title: Multi-cluster topologies and behaviour
description: A multi-cluster topology defines where writes originate, which clusters receive them, and how applications
  behave when a site or connection fails.
weight: 240
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- architects
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\multi-datacenter.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v2-multi-datacenter\architecture.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v3-multi-datacenter\architecture.md
- Legacy multi-datacenter replication terminology and commands require compatibility review.
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#interconnecting-multiple-clusters
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
- foundations/replication/multi-datacenter-architecture.md
- foundations/replication/cascading-writes.md
- foundations/performance/multi-datacenter-performance.md
related:
- how-to/planning-a-deployment/choose-a-multi-cluster-topology
- foundations/data-and-consistency/resolving-concurrent-updates
- foundations/replication-and-repair/real-time-replication-and-fullsync
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
- reference/orientation-and-compatibility/replication-generation-compatibility
---

A multi-cluster topology defines where writes originate, which clusters receive them, and how applications behave when a site or connection fails.

## One-way and bidirectional paths

A one-way path is suitable when one cluster owns writes and another receives a copy. Bidirectional paths allow both clusters to originate changes, but do not supply a global transaction order. Concurrent updates made at different sites still require compatible object policies and conflict handling.

## Cascades and selective replication

A cascade forwards changes through an intermediate cluster. It can reduce direct connectivity, but the intermediate site becomes part of the delivery and recovery path. Filters and forwarding behaviour determine which changes continue beyond it; a diagram alone does not establish that every write reaches every destination.

Bucket selection and queue definitions can restrict a path to a dataset. Keep that scope consistent with reconciliation and with the application's assumptions about where data exists.

## Failure and recovery

Failover requires an application routing decision as well as replicated data. Measure replication lag and define what data loss or stale reads are acceptable before switching traffic. When the original site returns, reconcile it before assuming it is an equivalent destination.

Cross-cluster replication also replicates unwanted logical changes. Independent, recoverable backups remain a separate concern.
