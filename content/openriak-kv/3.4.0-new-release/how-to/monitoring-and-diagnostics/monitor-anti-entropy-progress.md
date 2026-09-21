---
title: Monitor anti-entropy progress
description: Monitor whether TicTac AAE stores, trees, exchanges, and repairs are making progress. A tree being
  built is a different state from a completed exchange that found matching replicas.
weight: 870
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\active-anti-entropy.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-active-anti-entropy.md
source_material:
- legacy-3.2.5
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-aae---logs-and-statistics
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-and-controlling-aae---command-line
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-anti-entropy
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-legacy-aae
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/monitor-active-anti-entropy.md
related:
- how-to/replication-and-reconciliation/enable-tictac-anti-entropy
- how-to/data-inspection-and-repair/rebuild-aae-trees
- how-to/data-inspection-and-repair/repair-a-selected-key-range
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- how-to/monitoring-and-diagnostics/inspect-worker-queues-and-saturation
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Monitor whether TicTac AAE stores, trees, exchanges, and repairs are making progress. A tree being built is a different state from a completed exchange that found matching replicas.

## Inspect tree status

{{< cli-example key="shell:riak admin tictacaae treestatus" >}}

Compare last and next rebuild times, controller status, and native or parallel keystore state across affected partitions. Recently started nodes may need their initial rebuild before useful comparisons are available.

## Follow exchanges and repairs

Correlate AAE logs with metrics from [AAE, repair, and worker-pool metrics]({{< product-version-root >}}reference/operations-and-observability/aae-repair-and-worker-pool-metrics/). Track completed work and changing discrepancy counts over time. A recurring timeout or a queue that only grows requires investigation of worker capacity and backend I/O before increasing exchange frequency.

## Act on a specific failure

Use [Rebuild AAE trees]({{< product-version-root >}}how-to/data-inspection-and-repair/rebuild-aae-trees/) when a tree rebuild is required, [Repair a selected key range]({{< product-version-root >}}how-to/data-inspection-and-repair/repair-a-selected-key-range/) for a bounded key repair, and [Repair a vnode or node from surviving replicas]({{< product-version-root >}}how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas/) for lost vnode data. Keep token-bucket protection enabled while diagnosing pressure. After intervention, repeat the same observations and verify representative object reads.
