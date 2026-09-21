---
title: Fold filters
description: AAE fold filters select object namespaces, key intervals, modification intervals, or tree segments.
  Each operation accepts only the subset shown in its command contract.
weight: 840
diataxis: reference
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
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\filters.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/aae-fold-api/filters.md
related:
- reference/aae-fold-api/fold-invocation-and-result-conventions
- reference/aae-fold-api/count-keys
- reference/aae-fold-api/count-tombstones
- reference/aae-fold-api/repair-keys-in-a-range
- reference/aae-fold-api/erase-keys
- reference/aae-fold-api/reap-tombstones
- reference/aae-fold-api/replicate-keys-in-a-range
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

AAE fold filters select object namespaces, key intervals, modification intervals, or tree segments. Each operation accepts only the subset shown in its command contract.

## Bucket and key scope

An untyped bucket is a binary such as `<<"events">>`. A typed bucket is `{<<"type">>, <<"events">>}`. Key intervals use `{StartKey, EndKey}` with inclusive binary boundaries, or `all` where allowed. Keep the type when reporting or reusing a bucket identifier.

## Modified time

A modified range is `{date, Low, High}` using Unix seconds in the underlying fold contract. The convenience `aae_fold/1` interface also accepts supported calendar datetime forms and translates them. These are server modification times, not arbitrary application timestamps or a request for historical versions.

## Segments and coverage

A segment filter pairs segment IDs with the tree size under which they were calculated. Do not reuse IDs with a different tree size. `n_val` coverage arguments select a coverage plan; using a value larger than the replica count of some data can omit that data.

## Change method

Where supported, `count` counts candidates without queuing mutations. `local` submits work to the local maintenance path for each participating vnode. Job forms carry the documented job identifier. Do not substitute these methods across operations that have different tuple shapes.

The exact types and arities are included in each operation's CLI metadata page below.
