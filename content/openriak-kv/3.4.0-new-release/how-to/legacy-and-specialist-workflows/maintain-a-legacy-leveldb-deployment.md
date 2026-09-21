---
title: Maintain a legacy LevelDB deployment
description: Maintain an existing deployment using LevelDB while planning its migration. These interfaces have compatibility
  and deprecation constraints; check [[R3]] before choosing them for new data.
weight: 1350
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\backends\configure-leveldb.md
source_material:
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#eleveldb-deprecated
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/backends/leveldb.md
related:
- reference/legacy-and-experimental-features/legacy-leveldb-settings
- reference/orientation-and-compatibility/feature-status-and-deprecations
- how-to/storage-maintenance/migrate-to-another-storage-backend
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Maintain an existing deployment using LevelDB while planning its migration. These interfaces have compatibility and deprecation constraints; check [Feature status and deprecations]({{< product-version-root >}}reference/orientation-and-compatibility/feature-status-and-deprecations/) before choosing them for new data.

## Inventory the current state

Record the exact release, backend configuration, affected buckets, stored-data size, and recovery method. Read the settings in [Legacy LevelDB settings]({{< product-version-root >}}reference/legacy-and-experimental-features/legacy-leveldb-settings/) and compare them with the node's effective configuration rather than assuming old defaults still apply.

## Make a controlled change

Check compaction pressure, cache memory, open files, and free space over a complete workload cycle. Keep the existing on-disk format and compression choices compatible with any planned recovery release. Back up the relevant state and test the change on representative data. Validate configuration before a rolling deployment and preserve a rollback path that does not mix incompatible store formats.

## Verify and plan migration

Check known values, indexes where supported, memory and disk behaviour, and recovery after a stopped member. Use [Migrate to another storage backend]({{< product-version-root >}}how-to/storage-maintenance/migrate-to-another-storage-backend/) to migrate to another backend through a prepared destination, then retire the old state only after application verification.
