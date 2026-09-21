---
title: Count keys
description: Count matching keys by selecting the `count` change method of the erase-keys fold. This mode counts
  the selected candidates without executing erasure; there is no separate `count_keys` fold selector.
weight: 870
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- developers
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/aae-fold-api/count-keys.md
related:
- reference/aae-fold-api/fold-invocation-and-result-conventions
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/count-objects-in-a-selected-scope
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Count matching keys by selecting the `count` change method of the erase-keys fold. This mode counts the selected candidates without executing erasure; there is no separate `count_keys` fold selector.

## Invocation

{{< cli-command key="erlang:riak_client:aae_fold:erase_keys" >}}

## Scope and completion

Preserve the bucket type, key-range boundaries, and applicable segment and modification-time filters. For count mode, use the literal `count` in the change-method position; do not substitute `local` or a job tuple. For replication, monitor the destination and verify data after dispatch.
