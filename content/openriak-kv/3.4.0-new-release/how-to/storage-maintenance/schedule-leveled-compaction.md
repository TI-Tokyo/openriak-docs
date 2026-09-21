---
title: Schedule Leveled compaction
description: Adjust Leveled journal compaction only after measuring its effect on disk use and application latency.
  Ledger maintenance continues independently and can throttle writes when it falls behind.
weight: 330
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
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#leveled-compaction-highlow-hour
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/backends/leveled-compaction-window.md
related:
- how-to/storage-maintenance/configure-leveled
- how-to/performance/reduce-request-latency
- reference/configuration/leveled-settings
- foundations/storage-and-performance/how-leveled-stores-data
---

Adjust Leveled journal compaction only after measuring its effect on disk use and application latency. Ledger maintenance continues independently and can throttle writes when it falls behind.

## Establish a baseline

Observe journal compaction scores, reclaimed space, device latency, and request percentiles. In the Leveled logs, `ic003` reports candidate compaction scores and `p0024` helps identify ledger backlog. See [How Leveled stores data]({{< product-version-root >}}foundations/storage-and-performance/how-leveled-stores-data/) for the journal/ledger distinction.

## Adjust scheduling

{{< configuration-reference-table >}}
^leveled\.compaction
^leveled\.max_run_length$
{{< /configuration-reference-table >}}

Choose enough runs to keep disk growth bounded. If a window is required, check the node timezone and stagger it across failure domains. Do not use a journal window as a remedy for an already saturated ledger.

## Verify the change

Validate configuration, apply the change to a pilot node, and monitor a complete workload cycle. Persistently increasing positive compaction scores indicate work is accumulating; consistently negative scores may indicate that many checks find no worthwhile work. Compare disk and request behaviour before extending the change to other nodes.
