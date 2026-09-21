---
title: Node and cluster metrics
weight: 1010
product: OpenRiak KV
product_version: 3.4.1
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Node statistics report request activity, latency, storage, and runtime state. Collect them per node
  with a timestamp and release identifier before deriving cluster-wide views.
related:
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- how-to/monitoring-and-diagnostics/inspect-node-and-cluster-health
- how-to/troubleshooting/diagnose-a-slow-or-overloaded-cluster
- reference/http-api/status-and-statistics
- reference/operations-and-observability/replication-metrics
- reference/operations-and-observability/aae-repair-and-worker-pool-metrics
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Node statistics report request activity, latency, storage, and runtime state. Collect them per node with a timestamp and release identifier before deriving cluster-wide views.

## Retrieval

Use the HTTP endpoint in [Status and statistics]({{< product-version-root >}}reference/http-api/status-and-statistics/) or the command metadata below:

{{< cli-example key="shell:riak admin status" >}}

## Metric interpretation

Request counts and operation rates describe different intervals; cumulative counters can reset on restart. Latency samples and percentiles cannot be summed across nodes. Object and sibling counts, process memory, open files, queue depths, and backend bytes measure different resources and should retain their units.

Compare request metrics with the same interval's host CPU, memory, disk, and network observations. Runtime and backend metric availability can vary by release and enabled components; absent metrics are not automatically zero.

## Related metric families

Current-generation replication metrics are defined in [Replication metrics]({{< product-version-root >}}reference/operations-and-observability/replication-metrics/). TicTac, repair, and worker-pool metrics are in [AAE, repair, and worker-pool metrics]({{< product-version-root >}}reference/operations-and-observability/aae-repair-and-worker-pool-metrics/). Legacy replication statistics belong to the legacy control interface rather than the current replication health model.


## VM statistics in 3.4.1

The statistics endpoint adds runtime usage and limit observations, including process and port counts. Compare each count with its corresponding limit when identifying resource pressure; a large absolute value alone does not establish saturation.

## Exported KV metric names

Search the operation path or exact exported name below. These are the explicit aliases registered by the KV component; backend, operating-system, dynamically created per-bucket, and other application metrics can add fields to a running node's response. Request latency measurements use microseconds; object-size measurements use bytes and sibling measurements are counts.

{{< configuration-reference-table reference="node-metrics" >}}{{< /configuration-reference-table >}}
