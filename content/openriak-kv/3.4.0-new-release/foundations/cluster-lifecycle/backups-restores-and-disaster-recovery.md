---
title: Backups, restores, and disaster recovery
description: A backup preserves a recoverable state independently of the current cluster. Replication maintains
  another evolving copy; it can also carry accidental updates and deletions.
weight: 350
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- operators
- architects
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup-options
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-22'
review-by: TI Tokyo/JOM
review_scope: editorial & technical
restructured_from:
- foundations/operations/backups-and-restores.md
related:
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- how-to/cluster-lifecycle/restore-node-data-from-a-backup
- how-to/cluster-lifecycle/recover-a-cluster-after-a-widespread-failure
- foundations/data-and-consistency/deletion-tombstones-and-expiration
- reference/operations-and-observability/runtime-files-and-backup-contents
---

A backup preserves a recoverable state independently of the current cluster. Replication maintains another evolving copy; it can also carry accidental updates and deletions.

## Match the backup to the backend

Backend files, ring state, configuration, and cluster metadata have different consistency requirements. Copying a changing directory is not the same as a usable backup. The supported procedure depends on whether the node or backend can provide a consistent view for the copy.

## Define the recovery target

Restoring one node into a surviving cluster differs from reconstructing a whole cluster. In the first case, later surviving versions may need to repair the restored copy. In the second, the available backups determine which data and history can be recovered.

Older backups can contain values whose deletion markers have since been reaped. Reintroducing them without a reconciliation plan can resurrect deleted data.

## Test the restore

A completed backup job is evidence that a copy was made, not that applications can recover from it. Test restoration in an isolated environment and check object content, metadata, indexes, security configuration, and required cluster identity information. Record the recovery duration and the data interval that would be lost.
