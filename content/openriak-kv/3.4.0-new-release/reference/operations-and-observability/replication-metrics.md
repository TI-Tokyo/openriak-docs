---
title: Replication metrics
description: Current-generation replication metrics distinguish source fetches, destination delivery, and fullsync
  exchanges. Preserve node and queue/peer scope when interpreting them.
weight: 1020
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\multi-datacenter\statistics.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ReplicationGuide.html#statistics-available-via-riak-stats
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/operations/replication-statistics.md
related:
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- how-to/performance/tune-replication-throughput-and-lag
- reference/replication-interfaces/fullsync-requests-and-results
- reference/operations-and-observability/aae-repair-and-worker-pool-metrics
- reference/replication-interfaces/legacy-riak-repl-runtime-controls
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Current-generation replication metrics distinguish source fetches, destination delivery, and fullsync exchanges. Preserve node and queue/peer scope when interpreting them.

## Source and sink counters

{{< configuration-reference-table reference="replication-metrics" >}}{{< /configuration-reference-table >}}

A source queue length of zero does not prove convergence: items may have been consumed, discarded, or lost. Compare discard/error counters and known object reads with completed fullsync results.

## Fullsync outcomes

The `ttaaefs_*` families report source-ahead and sink-ahead discoveries, completed in-sync and out-of-sync exchanges, failures, duration, and check types. A submitted request is not a completed exchange. Logs provide the peer, scope, and `in_sync` result needed to interpret the counters.

Legacy `riak_repl` statistics are separate and must not be used as evidence of current-generation queue health.
