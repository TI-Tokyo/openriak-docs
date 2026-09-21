---
title: How Leveled stores data
description: Leveled separates the journal of stored values from the ledger used to locate current objects and index
  entries. This supports indexed access without keeping the complete key directory in memory.
weight: 290
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\plan\Choosing-a-backend\leveled.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\backend\leveled.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#leveled
- https://openriak.github.io/riak/RiakTheoryGuide.html#caching-and-acceleration
- https://openriak.github.io/riak/RiakTheoryGuide.html#compaction
- https://openriak.github.io/riak/RiakTheoryGuide.html#data-safety-and-security
- https://openriak.github.io/riak/RiakTheoryGuide.html#file-formats
- https://openriak.github.io/riak/RiakTheoryGuide.html#head-only-mode
- https://openriak.github.io/riak/RiakTheoryGuide.html#the-leveled-backend
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/storage/leveled.md
related:
- reference/configuration/leveled-settings
- how-to/storage-maintenance/configure-leveled
- how-to/storage-maintenance/schedule-leveled-compaction
- how-to/storage-maintenance/remove-obsolete-leveled-backup-files
- how-to/storage-maintenance/repair-a-leveled-store
- foundations/indexes-and-querying/query-consistency-and-snapshots
---

Leveled separates the journal of stored values from the ledger used to locate current objects and index entries. This supports indexed access without keeping the complete key directory in memory.

## Journal and ledger

The journal records object values. Ledger structures describe keys, metadata, and indexes and are organised so that reads can locate the needed state efficiently. Caches reduce repeated work, while durable files let the store recover state across restarts.

## Snapshots and background work

Snapshots let a query or fold examine a stable local view while other work proceeds. They are local storage views, not a transaction encompassing all vnodes. Holding old views can also delay reclamation of files still needed by readers.

Compaction reorganises stored structures and removes eligible obsolete state. It consumes disk bandwidth and spare space. Increasing foreground throughput without allowing this work to keep up can transfer the cost into later latency or storage pressure.

## Recovery and maintenance

Journal, ledger, and backup artefacts have different roles. Removing a file solely because it looks old can remove state needed by an active store or recovery procedure. Use backend-specific backup, cleanup, and rebuild guidance, and verify indexes as well as object reads after a recovery.
