---
title: Schedule Bitcask merges
description: Schedule Bitcask merges so obsolete data can be reclaimed without overwhelming the application's I/O
  budget.
weight: 320
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
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#bitcask-merge-window
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/backends/bitcask-merge-window.md
related:
- how-to/storage-maintenance/configure-bitcask
- how-to/performance/reduce-request-latency
- reference/configuration/bitcask-settings
- foundations/storage-and-performance/how-bitcask-stores-data
---

Schedule Bitcask merges so obsolete data can be reclaimed without overwhelming the application's I/O budget.

## Measure the need

Record disk growth, mutation rate, and merge-related latency over a representative period. Immutable append-only data has a different maintenance profile from frequently overwritten values. See [How Bitcask stores data]({{< product-version-root >}}foundations/storage-and-performance/how-bitcask-stores-data/) for the storage model.

## Configure the window

Choose a low-traffic window or stagger windows across nodes so replicas are not all merging together. Review the available policy, window, triggers, and thresholds:

{{< configuration-reference-table >}}
^bitcask\.merge
^bitcask\.max_merge_size$
{{< /configuration-reference-table >}}

Check the node's timezone when defining hour-based windows. Give the window enough time and disk headroom to clear accumulated work. Validate and deploy the configuration through a rolling change.

## Verify over a full cycle

Observe merge start and completion logs, free disk space, device latency, and request percentiles. If obsolete data continues accumulating, enlarge the maintenance capacity or reduce the workload; repeatedly delaying merges can exhaust disk space.
