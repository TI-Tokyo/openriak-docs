---
title: Real-time replication and fullsync
description: Real-time replication delivers ongoing changes, while fullsync compares datasets and repairs differences.
  A healthy multi-cluster deployment needs an understood path for both ordinary delivery and recovery after interrup
weight: 230
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- architects
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v3-multi-datacenter\aae.md
- Legacy multi-datacenter replication terminology and commands require compatibility review.
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
- foundations/replication/real-time-and-fullsync.md
related:
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- foundations/replication-and-repair/replication-generations-and-compatibility
- how-to/replication-and-reconciliation/enable-real-time-replication
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- reference/replication-interfaces/fullsync-requests-and-results
---

Real-time replication delivers ongoing changes, while fullsync compares datasets and repairs differences. A healthy multi-cluster deployment needs an understood path for both ordinary delivery and recovery after interruptions.

## The fast path

New changes enter the source queue and are consumed by the destination. This reduces the delay between a write and its arrival at the other cluster, but delivery is asynchronous. Client success at the source is not a transaction committed simultaneously in both clusters.

## Reconciliation

Fullsync compares version information for a selected dataset and identifies objects needing transfer. It can recover differences after queue loss, a long outage, or initial seeding. Its duration depends on the comparison scope, amount of divergence, transfer capacity, and repair controls.

Completion should be assessed through the exchange result and subsequent checks, not simply through an empty real-time queue. Concurrent writes can continue creating new differences while a comparison runs.

## Replication generations

For next-generation replication, use TicTac-based reconciliation and the current source/sink controls. Older instructions about a legacy AAE fullsync strategy, identical ring sizes, or `riak_repl` settings apply to their documented generation. They are not prerequisites to copy into a current deployment without checking applicability.
