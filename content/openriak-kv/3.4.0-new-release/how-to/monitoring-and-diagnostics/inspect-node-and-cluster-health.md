---
title: Inspect node and cluster health
description: Inspect a node's reported state and compare it with the cluster's view when investigating availability
  or performance.
weight: 850
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\node-control.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\inspecting-node.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/inspect-node-and-cluster.md
related:
- how-to/monitoring-and-diagnostics/inspect-vnode-and-backend-status
- how-to/monitoring-and-diagnostics/inspect-worker-queues-and-saturation
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console
- reference/operations-and-observability/node-and-cluster-metrics
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Inspect a node's reported state and compare it with the cluster's view when investigating availability or performance.

## Capture status

{{< cli-example key="shell:riak ping" >}}
{{< cli-example key="shell:riak admin status" >}}
{{< cli-example key="shell:riak admin cluster status" >}}

Collect the same observations from another healthy member. Distinguish a down process from a network partition, an administrative down state, or a process that responds but is overloaded.

## Correlate with the workload

Compare request-rate and latency metrics with CPU, memory, disk I/O, open files, and logs for the same interval. Use [Node and cluster metrics]({{< product-version-root >}}reference/operations-and-observability/node-and-cluster-metrics/) for metric definitions. Take repeated samples; cumulative counters need a time delta and may reset when a node restarts.

## Narrow the investigation

Use vnode status for a local partition problem, worker-queue inspection for delayed background work, and the remote console only when ordinary metrics are insufficient. Preserve the initial evidence before restarting a failing node. Verify improvement through the original client request, not only through a changed status line.
