---
title: Restore node data from a backup
description: Restore a verified backup into an isolated recovery environment before returning application traffic.
  For one failed member in an otherwise healthy cluster, prefer replica-based repair using [[H105]].
weight: 820
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#leveled---restore-a-backup
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/restore-node.md
related:
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- how-to/cluster-lifecycle/recover-a-cluster-after-a-widespread-failure
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- tutorials/cluster-operations-and-recovery/back-up-and-restore-a-sample-dataset
- reference/operations-and-observability/runtime-files-and-backup-contents
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
previous_page: how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
---

Restore a verified backup into an isolated recovery environment before returning application traffic. For one failed member in an otherwise healthy cluster, prefer replica-based repair using [Repair a vnode or node from surviving replicas]({{< product-version-root >}}how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas/).

## Verify the recovery set

Check backup integrity, capture times, node identities, release and OTP versions, backend layout, and cluster metadata. Ensure the selected files cover the intended dataset. Isolate the recovery cluster from live peers and replication so old or new state cannot mix unexpectedly.

## Restore stopped nodes

Install the matching software and stop all nodes being restored. Move existing backend directories aside rather than merging them with backup files. Restore data, ring and cluster metadata, configuration, and permissions to the recorded locations.

For a Leveled hot backup, restore the saved journal layout into the intended Leveled store. Its ledger is rebuilt at startup; do not reuse an unrelated ledger from a later state. Preserve the original backup while testing.

## Start and validate

Start the isolated nodes, wait for ledger rebuilds and membership recovery, then inspect transfers and AAE. Compare a recorded sample of values, siblings, indexes, and bucket policies. Explain any writes newer than the backup that the recovery cannot contain.

## Return traffic deliberately

Reconcile the recovered state with the intended live environment under an explicit plan, then restore client routing. Keep the displaced files until the recovery is verified. A successful process start alone is not evidence that the backup was complete.
