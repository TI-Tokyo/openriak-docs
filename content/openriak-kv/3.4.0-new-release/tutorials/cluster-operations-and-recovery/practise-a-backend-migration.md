---
title: Practise a backend migration
description: Move a small dataset from a Bitcask learning cluster to a new Leveled cluster using replication. Keep
  the source intact until the destination has been checked; changing a backend name does not convert existing files.
weight: 60
diataxis: tutorial
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- new-operators
source_material:
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\tutorials\change-backend.md
tags:
- diataxis
- kv
- tutorial
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- tutorials/operations/change-storage-backend.md
related:
- how-to/storage-maintenance/migrate-to-another-storage-backend
- how-to/replication-and-reconciliation/migrate-to-another-cluster-using-replication
- reference/orientation-and-compatibility/backend-capability-matrix
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
previous_page: tutorials/cluster-operations-and-recovery/inspect-and-repair-a-bounded-data-range
---

Move a small dataset from a Bitcask learning cluster to a new Leveled cluster using replication. Keep the source intact until the destination has been checked; changing a backend name does not convert existing files.

## Prepare two disposable clusters

Use the two isolated clusters in [Replicate data between two clusters]({{< product-version-root >}}tutorials/replication-and-reconciliation/replicate-data-between-two-clusters/). Before writing data, choose Bitcask on every source node and Leveled on every destination node using the backend setting in [Backend capability matrix]({{< product-version-root >}}reference/orientation-and-compatibility/backend-capability-matrix/). Keep TicTac AAE active; Bitcask requires its parallel store. Allow its initial rebuild to complete.

Use the replication lesson's source and sink endpoints. Write three objects named `item-001`, `item-002`, and `item-003` in an untyped bucket named `migration-demo`. Record their bodies and read each one back from the source.

## Enable delivery before seeding

Follow the source-queue and sink-worker steps in [Replicate data between two clusters]({{< product-version-root >}}tutorials/replication-and-reconciliation/replicate-data-between-two-clusters/). Use a dedicated queue for this destination. Write `item-004` after enabling real-time replication and confirm it appears at the sink.

Seed the older objects from the source remote console:

{{< cli-example key="erlang:riak_client:aae_fold:repl_keys_range" args=`{repl_keys_range, <<"migration-demo">>, all, all, cluster_b}` >}}

Wait for sink delivery, then read all four known keys at the sink. A queued count is not a delivered count.

## Verify and switch the client

Enable all-cluster reconciliation as shown in [Replicate data between two clusters]({{< product-version-root >}}tutorials/replication-and-reconciliation/replicate-data-between-two-clusters/), with both clusters' actual replication values. Wait for a successful exchange showing `in_sync=true`. Stop the sample writer, compare the known values once more, and point the sample client at the destination HTTP endpoint.

Add a secondary-indexed object on Leveled and run the exact query from [Build and query a people-search index]({{< product-version-root >}}tutorials/indexes-and-querying/build-and-query-a-people-search-index/). This checks an intended destination capability as well as object preservation.

## Keep a rollback point

Keep the source stopped or read-only until the test finishes. If writes begin on the destination, reverting the endpoint alone would lose those writes; copy and reconcile them before any rollback. When finished, stop both disposable clusters and remove only their exercise files.
