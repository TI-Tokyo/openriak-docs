---
title: Failure and recovery
description: A node failure changes which replicas are reachable and which work the surviving cluster must perform.
  Recovery is complete only when service, data, and replica placement have been checked.
weight: 340
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- architects
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\failure-recovery.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#replace-repair-and-recover
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/operations/node-failure-and-recovery.md
related:
- how-to/troubleshooting/recover-a-failed-node-or-choose-replacement
- how-to/cluster-lifecycle/replace-a-failed-node
- how-to/cluster-lifecycle/recover-a-cluster-after-a-widespread-failure
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
---

A node failure changes which replicas are reachable and which work the surviving cluster must perform. Recovery is complete only when service, data, and replica placement have been checked.

## Temporary loss

During a short interruption, eligible requests may use available primaries and fallbacks. Whether they succeed depends on their acknowledgement requirements. Restoring connectivity does not immediately establish that all copies agree; hinted handoff, read repair, and anti-entropy still have work to do.

## Permanent loss

A failed host may require replacement and reconstruction from surviving replicas. The decision depends on the state of its disks and identity, the remaining copies, and the current membership plan. Reusing a name or clearing a data directory without understanding that state can complicate recovery.

## Widespread failure

If surviving copies cannot supply the dataset, recovery needs a suitable backup or another independently recoverable source. Replication does not recover information that has been lost everywhere.

## What to verify

Check membership agreement, ownership transfers, backend health, representative reads and writes, and repair progress. An available HTTP listener proves only one part of recovery. Retain evidence of the original failure until the cause and the recovered state are understood.
