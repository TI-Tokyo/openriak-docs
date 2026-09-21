---
title: Reduce request latency
description: Reduce request latency by identifying where time is spent before changing database limits. Compare
  the same workload and percentile before and after each change.
weight: 1190
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\performance\latency-reduction.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/tune/reduce-latency.md
related:
- how-to/data-inspection-and-repair/find-oversized-objects-or-excessive-siblings
- how-to/storage-maintenance/schedule-bitcask-merges
- how-to/storage-maintenance/schedule-leveled-compaction
- how-to/monitoring-and-diagnostics/inspect-worker-queues-and-saturation
- how-to/performance/benchmark-a-representative-workload
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/storage-and-performance/capacity-and-growth
---

Reduce request latency by identifying where time is spent before changing database limits. Compare the same workload and percentile before and after each change.

## Localise the delay

Separate client/proxy time, network time, coordinator queues, replica response time, and backend I/O. Compare affected nodes and operations. Large values, many siblings, storage maintenance, and overloaded worker queues require different fixes.

## Choose the smallest useful change

Reduce oversized object boundaries or resolve sibling growth in the application. Stagger Bitcask maintenance when it is the measured cause. For saturated storage, reduce overlapping background work or add capacity. Change acknowledgement policies only when the application's durability and availability requirements permit it.

## Verify under load

Run the representative benchmark through the real client path, including a maintenance or recovery interval. Confirm improved tail latency without increased errors, lost protection, or an ever-growing background backlog. Keep the original configuration and revert changes that merely move the bottleneck elsewhere.
