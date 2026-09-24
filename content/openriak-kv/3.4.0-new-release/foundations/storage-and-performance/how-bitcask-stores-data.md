---
title: How Bitcask stores data
description: Bitcask stores values in append-only data files and keeps an in-memory directory locating the current
  record for each key. A lookup uses that directory to find the corresponding value on disk.
weight: 280
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
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\plan\Choosing-a-backend\bitcask.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\backend\bitcask.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#bitcask
- https://openriak.github.io/riak/RiakTheoryGuide.html#the-bitcask-backend
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-24'
review_scope: content changes
review-by: TI Tokyo/JOM
restructured_from:
- foundations/storage/bitcask.md
related:
- reference/configuration/bitcask-settings
- reference/orientation-and-compatibility/backend-capability-matrix
- how-to/storage-maintenance/configure-bitcask
- how-to/storage-maintenance/schedule-bitcask-merges
- foundations/storage-and-performance/persistence-filesystems-and-space-reclamation
- foundations/storage-and-performance/capacity-and-growth
---

Bitcask stores values in append-only data files and keeps an in-memory directory locating the current record for each key. A lookup uses that directory to find the corresponding value on disk.

## Writes and obsolete records

Updating an object appends a new record. Older records remain physically present until a merge rewrites the live data and removes eligible obsolete files. Deleting visible objects therefore does not immediately return all of their disk space.

## Memory follows the keyspace

The key directory has an entry for each retained key. Small values do not eliminate that per-key cost, so a workload with many tiny objects can become memory-bound even when the value files are modest. Startup also needs to reconstruct the directory using the stored files and hints.

## Persistence and merging

The write path and configured synchronisation behaviours determine if acknowledged work is resilient to process or host failure. A merge consumes I/O and temporary capacity alongside foreground traffic. Scheduling merges changes when that cost is paid; it does not make obsolete records disappear for free. This does allow you to reduce the impact of these merges on regular operations however.

Bitcask's key/value design should not be assumed to provide the same secondary-index capabilities as Leveled. Choose an engine from the access pattern rather than from a throughput figure measured on another workload.
