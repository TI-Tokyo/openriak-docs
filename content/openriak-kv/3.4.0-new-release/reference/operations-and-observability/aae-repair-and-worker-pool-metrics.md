---
title: AAE, repair, and worker-pool metrics
weight: 1030
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: AAE and reconciliation metrics report work and timing on the responding node. Compare all participating
  nodes and the same time interval when diagnosing convergence.
related:
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- how-to/monitoring-and-diagnostics/inspect-worker-queues-and-saturation
- reference/operations-and-observability/node-and-cluster-metrics
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

AAE and reconciliation metrics report work and timing on the responding node. Compare all participating nodes and the same time interval when diagnosing convergence.

## Registered metrics

{{< configuration-reference-table reference="aae-metrics" >}}{{< /configuration-reference-table >}}

## Scope and interpretation

Event totals and timing distributions are different measurements. A count of scheduled checks is not a count of repaired objects, and the maximum recorded duration is not a service-level latency guarantee. Node restarts and metric resets can change the observation history.

Worker queues and process saturation complement these metrics. Use the worker-pool diagnostic procedure to inspect active and queued work; a small queue during a failed exchange does not prove that replication is healthy.
