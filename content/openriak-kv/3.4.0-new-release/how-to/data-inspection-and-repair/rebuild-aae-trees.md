---
title: Rebuild AAE trees
description: Prompt a TicTac AAE store or tree rebuild for selected nodes or partitions, then verify that it completes.
  Rebuild only the scope required by the diagnosis.
weight: 1050
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-and-controlling-aae---command-line
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/rebuild-aae-trees.md
related:
- how-to/replication-and-reconciliation/enable-tictac-anti-entropy
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- how-to/monitoring-and-diagnostics/inspect-worker-queues-and-saturation
- reference/configuration/tictac-anti-entropy-settings
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
---

Prompt a TicTac AAE store or tree rebuild for selected nodes or partitions, then verify that it completes. Rebuild only the scope required by the diagnosis.

## Inspect the current state

{{< cli-example key="shell:riak admin tictacaae treestatus" >}}

Record the affected partition IDs, last rebuild, next rebuild, and store mode. Native mode rebuilds from Leveled; parallel mode also has a separate keystore to rebuild.

## Schedule the rebuild

{{< cli-example key="shell:riak admin tictacaae rebuild-soon" >}}

Use the metadata options to select the node/partition and delay. To prompt the next check immediately after making a rebuild due:

{{< cli-example key="shell:riak admin tictacaae rebuild-now" >}}

`rebuild-now` prompts a rebuild tick; it does not force a rebuild that is not due. Avoid scheduling every partition concurrently when the worker pools or disks are already saturated.

## Verify completion

Follow rebuild logs and tree status until the new rebuild timestamp and usable state appear. Confirm exchanges resume and representative folds return expected data. If rebuilding repeatedly fails, preserve the backend errors and investigate the underlying store rather than continuously rescheduling it.
