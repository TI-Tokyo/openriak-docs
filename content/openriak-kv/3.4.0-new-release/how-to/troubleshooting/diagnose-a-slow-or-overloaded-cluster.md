---
title: Diagnose a slow or overloaded cluster
description: Find the constrained part of a slow cluster before changing timeouts or concurrency.
weight: 1280
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- developers
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/troubleshoot/slow-cluster.md
related:
- how-to/monitoring-and-diagnostics/inspect-worker-queues-and-saturation
- how-to/performance/reduce-request-latency
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Find the constrained part of a slow cluster before changing timeouts or concurrency.

## Bound the symptom

Identify affected operations, nodes, buckets, and latency percentiles. Compare with a healthy interval and recent changes.

## Follow resource pressure

Correlate CPU, memory, storage latency, network use, worker queues, and backend status. Include handoff, compaction, repair, and replication work.

## Test one remedy

Reduce offered load or adjust the identified resource constraint. Keep a comparable workload and record the previous configuration.

## Verify recovery

Check tail latency, errors, backlog, and background completion. A lower request rate without a draining queue does not establish recovery.

## Diagnostic commands

{{< cli-example key="shell:riak admin status" >}}
