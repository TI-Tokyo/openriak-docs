---
title: Latency, queues, and resource contention
description: Latency is the time a request waits as well as the time spent doing its work. Once a shared resource
  approaches saturation, queues can grow even when the operation itself has not changed.
weight: 320
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: reviewed
draft: true
audience:
- performance-engineers
- architects
- operators
source_material:
- live-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#notes-on-implementation
- https://openriak.github.io/riak/ObjectAPI.html#performance-and-efficiency
- https://openriak.github.io/riak/ObjectAPI.html#performance-expectations
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
- foundations/performance/latency-throughput-and-capacity.md
- foundations/performance/erlang-runtime.md
related:
- how-to/monitoring-and-diagnostics/inspect-worker-queues-and-saturation
- how-to/performance/benchmark-a-representative-workload
- how-to/performance/reduce-request-latency
- how-to/performance/tune-the-erlang-vm-for-a-measured-bottleneck
- reference/operations-and-observability/aae-repair-and-worker-pool-metrics
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
---

Latency is the time a request waits as well as the time spent doing its work. Once a shared resource approaches saturation, queues can grow even when the operation itself has not changed.

## Shared resources

Foreground requests compete with compaction, queries, handoffs, replication, and repair for CPU, memory, disk, and network capacity. Erlang processes provide concurrency, but they still run on finite schedulers and physical resources.

## Follow the queue

A slow client response may reflect a backend queue, a busy worker pool, a delayed replica, network transfer, or scheduling pressure. A single average latency cannot distinguish these cases. Compare tail latency, queue length, resource utilisation, and background progress over the same interval.

## Throughput and concurrency

Increasing concurrency can improve utilisation when resources are idle. Beyond saturation, it adds waiting and memory pressure. Raising timeouts can hide a symptom while leaving the queue to grow; raising worker counts can move the bottleneck to storage.

## Testing throughput and resource usage

In testing it is recommended to change one measured constraint at a time and keep a comparable workload. Confirm that the change improves the application's target latency or throughput while repair and maintenance continue to complete. A benchmark that pauses all background work describes a different operating condition.
