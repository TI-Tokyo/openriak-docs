---
title: Read repair and TicTac anti-entropy
description: Read repair and TicTac active anti-entropy both help replicas converge. Read repair reacts to replica
  differences found while serving a read; TicTac compares replica state independently of client reads.
weight: 210
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- architects
- operators
source_material:
- source-code-release-notes-3.4
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/RiakTheoryGuide.html#anti-entropy
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
- foundations/replication/tictac-aae.md
- foundations/replication/active-anti-entropy.md
related:
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- how-to/replication-and-reconciliation/enable-tictac-anti-entropy
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- reference/configuration/tictac-anti-entropy-settings
---

Read repair and TicTac active anti-entropy both help replicas converge. Read repair reacts to replica differences found while serving a read; TicTac compares replica state independently of client reads.

## Finding differences efficiently

TicTac uses trees summarising keys and version information. Matching summaries can establish that the compared scope agrees without exchanging every object. A mismatch narrows the search to branches, segments, and eventually keys whose versions need comparison.

Repairing a difference costs more than confirming agreement: it requires locating versions and transferring objects. Throttling and worker limits balance convergence against the resources needed by application traffic.

## Trees and stores

Cached summaries must themselves remain consistent with stored data. Rebuilds and targeted refreshes correct stale tree state. Backend integration determines whether anti-entropy can use a native store or needs a parallel store, with different storage and rebuild costs.

## Limits of repair

Repair can copy surviving data and reconcile known versions. It cannot reconstruct a value when every usable copy and backup has been lost. Nor does it decide an application's business meaning when two updates are concurrent.

Inter-cluster reconciliation uses related comparison principles but compares cluster-wide coverage rather than assuming identical vnode layouts. Legacy active anti-entropy is a separate implementation with different settings.
