---
title: Storage backend trade-offs
description: A storage backend manages each vnode's local data. Its design determines memory use, persistence behaviour,
  index support, and the maintenance work that competes with requests.
weight: 270
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- architects
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\backends\index.md
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\plan\Choosing-a-backend\index.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\backend.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#database-backend
- https://openriak.github.io/riak/RiakTheoryGuide.html#backend-design
tags:
- diataxis
- kv
- explanation
editorial_review: required
technical_review: complete
last_reviewed: '2026-09-24'
review_scope: content changes
review-by: TI Tokyo/JOM
restructured_from:
- foundations/storage/choosing-backend.md
related:
- foundations/storage-and-performance/how-bitcask-stores-data
- foundations/storage-and-performance/how-leveled-stores-data
- reference/orientation-and-compatibility/backend-capability-matrix
- reference/orientation-and-compatibility/feature-status-and-deprecations
- how-to/planning-a-deployment/choose-a-storage-backend
- how-to/storage-maintenance/migrate-to-another-storage-backend
---

A storage backend manages each vnode's local data. Its design determines memory use, persistence behaviour, index support, and the maintenance work that competes with requests.

## Bitcask and Leveled

Bitcask appends values to data files and keeps a key directory in memory. Its fit depends on the size of the keyspace and available memory. It is a natural option for direct key/value access when that directory can be accommodated.

Leveled separates journaled values from indexed state and supports workloads requiring secondary indexes. Caches, compaction, and snapshots affect its resource use and operational behaviour.

## Other backend names

LevelDB, the memory backend, and multi-backend routing appear in historical and specialist deployments. Their presence in the configuration schema does not make them equivalent choices for a new deployment. The release-specific capability and feature-status references describe applicability.

## A choice persists with the data

Changing a backend setting does not convert existing backend files. Migration must preserve objects, metadata, indexes, and the required recovery path. You should benchmark the intended workload and include startup, compaction, and replica recovery before selecting an engine.
