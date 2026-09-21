---
title: Tune replication throughput and lag
description: Adjust replication throughput while keeping both clusters' application workloads within their latency
  targets.
weight: 1230
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- performance-engineers
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\performance\multi-datacenter-tuning.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/tune/tune-multi-datacenter.md
related:
- how-to/replication-and-reconciliation/configure-sink-nodes-and-consumers
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- reference/configuration/next-generation-replication-settings
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/storage-and-performance/capacity-and-growth
---

Adjust replication throughput while keeping both clusters' application workloads within their latency targets.

## Measure the bottleneck

Record source queue growth and discards, sink fetch/push timings, delivery lag, network latency, and destination backend pressure. Separate slow real-time delivery from slow fullsync discovery.

## Adjust consumers carefully

Use the sink-worker and per-peer limits in [Next-generation replication settings]({{< product-version-root >}}reference/configuration/next-generation-replication-settings/) or the runtime controls in [Next-generation replication runtime controls]({{< product-version-root >}}reference/replication-interfaces/next-generation-replication-runtime-controls/). Increase in small steps only while both sides have spare capacity. More consumers can overload a concentrated backlog of keys on a few vnodes.

## Balance reconciliation

Reduce overlapping checks that time out before completing. For a large known gap, use a bounded seed rather than increasing every fullsync limit. Consider compression only when data is compressible and CPU headroom exists.

## Verify the full cycle

Pause and resume a consumer in a test environment, measure catch-up, and confirm a completed in-sync exchange. Persist successful settings and restore temporary runtime changes. Do not accept a lower lag measurement if discard counters increase or application latency degrades.
