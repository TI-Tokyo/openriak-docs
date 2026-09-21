---
title: Benchmark a representative workload
description: Benchmark the intended workload and failure states before choosing capacity or tuning values. A short
  run against empty storage is not a reliable capacity measurement.
weight: 1180
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- performance-engineers
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\performance\benchmarking.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#volume-and-performance-testing
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/tune/benchmark-cluster.md
related:
- how-to/planning-a-deployment/size-a-cluster-and-reserve-recovery-headroom
- how-to/performance/reduce-request-latency
- how-to/performance/tune-the-erlang-vm-for-a-measured-bottleneck
- how-to/performance/tune-replication-throughput-and-lag
- how-to/performance/reduce-query-api-cost
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/storage-and-performance/capacity-and-growth
---

Benchmark the intended workload and failure states before choosing capacity or tuning values. A short run against empty storage is not a reliable capacity measurement.

## Define the workload

Record key count, object-size distribution, read/write/delete mix, concurrency, conflict rate, index/query patterns, and client retry policy. Include authentication, TLS, and the actual network path. Use a fixed seed or recorded dataset when repeatability matters.

## Prepare a representative environment

Use the target package, OTP, backend, filesystem, and replica policies. Load enough data to exercise normal memory and disk behaviour, then allow maintenance to reach a steady cycle. Keep the load generator separate and verify it is not the bottleneck.

## Run and measure

Increase load in controlled steps while recording achieved throughput, latency percentiles, errors, CPU, memory, disk I/O, queues, and maintenance logs. Include a stable sustained period and a recovery period. Test a rolling restart or failed member at the intended operating load, using only disposable or approved test data.

## Compare changes

Change one relevant variable, rerun the same workload, and compare both client and recovery outcomes. Preserve tool version, dataset, commands, configuration, and raw results. Adopt a change only if it improves the target metric without violating the other operating limits.
