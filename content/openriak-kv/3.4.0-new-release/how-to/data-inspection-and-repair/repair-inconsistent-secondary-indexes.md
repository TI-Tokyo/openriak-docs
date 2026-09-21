---
title: Repair inconsistent secondary indexes
description: Repair secondary-index inconsistencies using the procedure supported by the affected backend. First
  distinguish a stale or incorrect application index entry from a backend index-format problem.
weight: 1080
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\2i.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\secondary-indexes.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery\secondary-indexes.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/troubleshoot/repair-secondary-indexes.md
related:
- reference/orientation-and-compatibility/backend-capability-matrix
- reference/data-model-contracts/secondary-index-terms-and-projected-attributes
- reference/commands/repair-and-recovery-commands
- how-to/storage-maintenance/repair-a-leveled-store
- how-to/indexes-and-queries/add-and-query-secondary-indexes
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
---

Repair secondary-index inconsistencies using the procedure supported by the affected backend. First distinguish a stale or incorrect application index entry from a backend index-format problem.

## Identify the scope

Fetch known objects and inspect their index metadata. Compare expected exact and range lookups. Record the backend, partitions, release, and any upgrade that preceded the inconsistency.

## Check the repair interface

{{< cli key="shell:riak admin repair-2i" >}} is a legacy index-repair interface. Inspect its help and backend applicability before starting it; it is not a general Leveled index reconstruction command.

If the application wrote incorrect index metadata, repair the application write path and rewrite affected objects with complete current index entries and preserved context. If a Leveled store is damaged, use its documented store-repair procedure and preserve the original store first.

## Verify

Repeat the same known queries and compare fetched object metadata. Check range boundaries and multiple terms for one key. Monitor repair progress and foreground latency, and retain the candidate list and pre-repair observations until correctness is established.
