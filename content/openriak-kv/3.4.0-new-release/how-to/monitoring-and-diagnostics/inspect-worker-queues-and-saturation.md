---
title: Inspect worker queues and saturation
description: Identify worker queues that delay background operations and distinguish insufficient processing capacity
  from excessive submitted work.
weight: 900
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
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-node-worker-pools
- https://openriak.github.io/riak/OtherAPI.html#node-worker-pools
- https://openriak.github.io/riak/ReplicationGuide.html#concepts---queues-and-workers
- https://openriak.github.io/riak/ReplicationGuide.html#configure-and-monitor-work-queues
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/monitor-worker-pools.md
related:
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- how-to/performance/reduce-query-api-cost
- how-to/troubleshooting/diagnose-a-slow-or-overloaded-cluster
- reference/operations-and-observability/aae-repair-and-worker-pool-metrics
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Identify worker queues that delay background operations and distinguish insufficient processing capacity from excessive submitted work.

## Collect a time series

Record queue lengths, active workers, completed operations, timeout logs, backend latency, and client request percentiles over the same interval. Use [AAE, repair, and worker-pool metrics]({{< product-version-root >}}reference/operations-and-observability/aae-repair-and-worker-pool-metrics/) for the release's metrics and [Repair and handoff settings]({{< product-version-root >}}reference/configuration/repair-and-handoff-settings/) for worker-related settings.

## Find the producer

Correlate growth with AAE rebuilds, fullsync checks, folds, handoffs, or bulk reclamation jobs. A job timing out while queued can waste backend work even after the caller has stopped waiting. Reduce overlapping schedules or narrow the submitted scope before increasing concurrency.

## Adjust one limit at a time

Change the appropriate pool or request budget on a pilot node. More workers can saturate storage and increase application latency; retain a measured recovery-progress target as well as a client latency target.

## Verify and persist

Confirm that the queue drains, useful operations complete, and request latency remains acceptable. Persist any lasting configuration change and restore temporary diagnostic overrides. If work still accumulates, address the underlying I/O or workload limit rather than repeatedly extending timeouts.
