---
title: Back up node data and cluster metadata
description: Capture backend data together with the metadata needed to interpret it, then prove that it can be restored.
  A collection of node backups is not an atomic cluster-wide snapshot.
weight: 810
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\backing-up.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup---ring-folder-and-cluster-metadata
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup---the-preferred-building-block
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup-options
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#bitcask---backups
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#leveled---hot-backups
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/back-up-node.md
related:
- how-to/cluster-lifecycle/restore-node-data-from-a-backup
- tutorials/cluster-operations-and-recovery/back-up-and-restore-a-sample-dataset
- reference/operations-and-observability/runtime-files-and-backup-contents
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
next_page: how-to/cluster-lifecycle/restore-node-data-from-a-backup
---

Capture backend data together with the metadata needed to interpret it, then prove that it can be restored. A collection of node backups is not an atomic cluster-wide snapshot.

## Choose the procedure

For a stopped-state backup, drain and stop each selected node before copying its data, ring, cluster metadata, configuration, and required keys. Preserve ownership and the exact release and OTP details. For a whole-cluster recovery point, coordinate the write pause and scope explicitly.

For Leveled-only deployments, a hot backup can preserve journal state using hard links on the same filesystem. Open the remote console and use the function contract below with a backup path outside the active store and the intended replica/coverage values:

{{< cli-example key="erlang:riak_client:hotbackup" >}}

The call requires a Riak client handle. Review [Runtime files and backup contents]({{< product-version-root >}}reference/operations-and-observability/runtime-files-and-backup-contents/) and the command's argument contract before selecting coverage; partial coverage is not the same as backing up every vnode.

## Protect the captured state

Confirm the operation succeeded on every required node. Copy the completed backup to independent storage, preserving its layout and manifest. Keep configuration, node identities, bucket and security metadata, checksums, and a record of capture times alongside it. Hard links on the same failed disk are not an independent backup.

## Test restoration

Restore into an isolated environment using [Restore node data from a backup]({{< product-version-root >}}how-to/cluster-lifecycle/restore-node-data-from-a-backup/). Compare known values, metadata, indexes, and cluster state. Record the measured recovery time and any missing scope before accepting the backup procedure.
