---
title: Migrate to another storage backend
description: Move data to a different backend by preparing storage that uses the destination backend and copying
  data through a supported recovery or replication path. A backend setting does not convert existing files.
weight: 340
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\backend.md
source_material:
- legacy-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#database-backend---changing-the-choice
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/backends/change-backend.md
related:
- tutorials/cluster-operations-and-recovery/practise-a-backend-migration
- how-to/replication-and-reconciliation/migrate-to-another-cluster-using-replication
- how-to/planning-a-deployment/choose-a-storage-backend
- foundations/storage-and-performance/storage-backend-trade-offs
- foundations/storage-and-performance/persistence-filesystems-and-space-reclamation
---

Move data to a different backend by preparing storage that uses the destination backend and copying data through a supported recovery or replication path. A backend setting does not convert existing files.

## Choose and rehearse the migration

Check [Backend capability matrix]({{< product-version-root >}}reference/orientation-and-compatibility/backend-capability-matrix/) for destination capabilities. For a cluster-wide change, create a separate cluster with the intended backend and use [Migrate to another cluster using replication]({{< product-version-root >}}how-to/replication-and-reconciliation/migrate-to-another-cluster-using-replication/). This preserves the original data while the destination is seeded and reconciled.

## Prepare the destination

Configure the backend before loading objects. Create matching bucket types and properties, provision security separately, and check available disk and memory capacity. Establish real-time replication before seeding so writes during the copy are captured.

## Copy and verify

Seed each required bucket, observe queue delivery, and run reconciliation. Verify known objects, sibling behaviour, data types, and required indexes through the destination's application endpoint. A matching object count alone does not prove matching values and causal histories.

## Switch traffic

Quiesce or coordinate writers, complete the final catch-up, and switch the application endpoint. Retain the original cluster until the rollback window ends. If writes have reached the destination, a rollback must reconcile those writes back before returning traffic.
