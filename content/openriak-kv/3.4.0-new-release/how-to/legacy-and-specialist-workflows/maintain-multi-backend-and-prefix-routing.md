---
title: Maintain multi-backend and prefix routing
description: Maintain an existing deployment using multi-backend and prefix routing while planning its migration.
  These interfaces have compatibility and deprecation constraints; check [[R3]] before choosing them for new data.
weight: 1370
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\backends\configure-multi.md
source_material:
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#multi-backend
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/backends/multi.md
- how-to/configure/backends/prefix-multi.md
related:
- reference/legacy-and-experimental-features/multi-backend-and-prefix-routing-settings
- reference/orientation-and-compatibility/feature-status-and-deprecations
- how-to/storage-maintenance/migrate-to-another-storage-backend
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- foundations/storage-and-performance/multiple-backends-and-prefix-routing
---

Maintain an existing deployment using multi-backend and prefix routing while planning its migration. These interfaces have compatibility and deprecation constraints; check [Feature status and deprecations]({{< product-version-root >}}reference/orientation-and-compatibility/feature-status-and-deprecations/) before choosing them for new data.

## Inventory the current state

Record the exact release, backend configuration, affected buckets, stored-data size, and recovery method. Read the settings in [Multi-backend and prefix-routing settings]({{< product-version-root >}}reference/legacy-and-experimental-features/multi-backend-and-prefix-routing-settings/) and compare them with the node's effective configuration rather than assuming old defaults still apply.

## Make a controlled change

Inventory every backend name and bucket-to-backend mapping before changing routing. A mapping change does not move existing data. Verify both typed and untyped buckets and preserve the old stores until migration is complete. Back up the relevant state and test the change on representative data. Validate configuration before a rolling deployment and preserve a rollback path that does not mix incompatible store formats.

## Verify and plan migration

Check known values, indexes where supported, memory and disk behaviour, and recovery after a stopped member. Use [Migrate to another storage backend]({{< product-version-root >}}how-to/storage-maintenance/migrate-to-another-storage-backend/) to migrate to another backend through a prepared destination, then retire the old state only after application verification.
