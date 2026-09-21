---
title: Repair a Leveled store
description: Rebuild a Leveled ledger from its intact journal when the ledger or its indexes are damaged. This procedure
  does not recover a missing or corrupt journal.
weight: 360
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
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#repair-an-individual-leveled-store
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/repair-leveled-store.md
related:
- how-to/cluster-lifecycle/start-stop-or-restart-a-node
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- how-to/data-inspection-and-repair/repair-inconsistent-secondary-indexes
- reference/operations-and-observability/runtime-files-and-backup-contents
- foundations/storage-and-performance/how-leveled-stores-data
---

Rebuild a Leveled ledger from its intact journal when the ledger or its indexes are damaged. This procedure does not recover a missing or corrupt journal.

## Confirm the recovery source

Identify the affected node and partition from logs. Preserve a backup or snapshot for investigation and confirm surviving replicas can serve the workload while the node is unavailable. Use [Repair a vnode or node from surviving replicas]({{< product-version-root >}}how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas/) if the journal itself is lost or unreliable.

## Stop and isolate the ledger

Drain client traffic and stop the node using [Start, stop, or restart a node]({{< product-version-root >}}how-to/cluster-lifecycle/start-stop-or-restart-a-node/). Under the affected partition's Leveled store, move the `ledger` directory to a separate recovery location outside the active store. Keep the journal and its manifest intact. Do not remove the whole partition directory.

## Restart and wait

Start the node. Leveled rebuilds a missing ledger from the journal before the KV application becomes available. Follow `b0006` progress messages and allow time proportional to the stored data. Avoid repeatedly restarting a rebuild that is still making progress.

## Verify

Check node health, known object reads, and secondary-index queries, then monitor anti-entropy and return the node to client traffic. Retain the old ledger until the recovered state is verified. If rebuilding fails, preserve the logs and use replica-based repair rather than repeatedly modifying the source journal.
