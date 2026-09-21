---
title: Monitor replication and inter-cluster reconciliation
description: Monitor current-generation replication delivery and fullsync convergence separately. A drained source
  queue does not prove that every destination value matches.
weight: 890
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-inter-cluster-reconciliation
- https://openriak.github.io/riak/ReplicationGuide.html#monitoring-and-runtime-changes
- https://openriak.github.io/riak/ReplicationGuide.html#monitoring-real-time-replication-via-logs
- https://openriak.github.io/riak/ReplicationGuide.html#monitoring-reconciliation-exchanges-via-logs
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/monitor-reconciliation.md
related:
- how-to/troubleshooting/diagnose-stalled-or-incomplete-replication
- how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window
- how-to/performance/tune-replication-throughput-and-lag
- reference/operations-and-observability/replication-metrics
- reference/replication-interfaces/fullsync-requests-and-results
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Monitor current-generation replication delivery and fullsync convergence separately. A drained source queue does not prove that every destination value matches.

## Check delivery

Track source queue lengths, overflow discards, and sink fetch/push errors. Compare delivery lag with the application's target and the age of outstanding changes. Inspect every source and sink node involved in the relationship.

{{< cli-example key="erlang:riak_kv_replrtq_src:length_rtq" >}}

Supply the intended queue name in the remote console. Use [Replication metrics]({{< product-version-root >}}reference/operations-and-observability/replication-metrics/) for metrics and [Next-generation replication runtime controls]({{< product-version-root >}}reference/replication-interfaces/next-generation-replication-runtime-controls/) for runtime controls.

## Check reconciliation

Find completed exchange logs for the intended peer and scope. `in_sync=true` is an observed result for that comparison, not a permanent guarantee. If a check queues repairs, allow delivery and follow the next completed check. Track repeated timeouts or repair counts that do not decline.

## Investigate a gap

Verify queue names, filters, destination type definitions, peer reachability, and recent source restarts. Temporary queues can lose references; use reconciliation or a bounded re-seed to recover them. Do not clear a queue as a routine lag remedy.
