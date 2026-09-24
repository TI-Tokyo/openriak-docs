---
title: Targeted reconciliation and AAE folds
description: Targeted reconciliation limits inspection or repair to the data relevant to a question. AAE folds can
  examine bucket, key-range, time, segment, or object characteristics without requiring an unbounded client-side
  key lis
weight: 250
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- operators
- architects
source_material:
- legacy-3.2.5
- openriak-quickdocs-3.4
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery\repairs.md
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
- foundations/operations/repair-granularity.md
- foundations/replication/reconciliation-scope.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/repair-a-selected-key-range
- how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window
- reference/aae-fold-api/fold-invocation-and-result-conventions
- reference/aae-fold-api/fold-filters
---

Targeted reconciliation limits inspection or repair to the data relevant to a question. AAE folds can examine bucket, key-range, time, segment, or object characteristics without requiring an unbounded client-side key listing.

## Choose the scope of the incident

If a replication interruption affects one dataset and time window, that scope can guide a re-replication operation. If a diagnostic question concerns oversized objects, a fold can identify candidates before the application fetches their full contents.

Filters describe a selection, not proof that every relevant event lies inside it. Modification-time windows, for example, depend on the meaning of the stored modification data. Validate boundaries and include the recovery history when selecting them.

## Inspection and mutation differ

Listing, counting, and statistics observe data. Repair, erasure, reaping, and re-replication can change state or schedule substantial work. Preview candidates and check completion using the operation's actual contract.

## Cost and progress

A narrow result does not always imply a narrow backend scan. Folds use cluster coverage and available backend filtering, and compete for workers and storage resources. A timeout at the requesting console is not necessarily proof that background work stopped.

TicTac's cached comparisons and bounded folds complement each other: one detects broad disagreement efficiently, and the other inspects or acts on a selected scope.
