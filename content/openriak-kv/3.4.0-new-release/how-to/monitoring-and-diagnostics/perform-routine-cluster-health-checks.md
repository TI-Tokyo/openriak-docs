---
title: Perform routine cluster health checks
description: Check cluster health on a schedule and before operational changes. Compare trends with the deployment's
  normal workload rather than relying on one status snapshot.
weight: 840
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
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#operation-checklist
tags:
- diataxis
- kv
- how-to
- quickdocs
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/routine-operations-checklist.md
related:
- how-to/monitoring-and-diagnostics/inspect-node-and-cluster-health
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- how-to/monitoring-and-diagnostics/inspect-worker-queues-and-saturation
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- reference/operations-and-observability/node-and-cluster-metrics
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Check cluster health on a schedule and before operational changes. Compare trends with the deployment's normal workload rather than relying on one status snapshot.

## Check membership and movement

{{< cli-example key="shell:riak admin member-status" >}}
{{< cli-example key="shell:riak admin cluster status" >}}
{{< cli-example key="shell:riak admin transfers" >}}

Investigate unexpected members, unavailable nodes, incomplete ownership changes, and transfers that stop progressing.

## Check requests and resources

Run a read/write probe through the application endpoint with its real authentication and policy. Review request errors and latency percentiles, free disk space, device latency, memory, and file descriptors. A responsive `/ping` confirms basic liveness only.

## Check background protection

Confirm AAE exchanges and rebuilds progress. For connected clusters, check source discards, sink errors, queue growth, and completed reconciliation results. Verify that logs rotate and recent backups have a successful restore record.

Record abnormal findings with timestamps and node identities. Use the focused diagnostic guide for each symptom before changing limits or restarting processes.
