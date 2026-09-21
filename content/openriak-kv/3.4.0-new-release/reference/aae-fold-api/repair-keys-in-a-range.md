---
title: Repair keys in a range
description: Queue read repair for keys in a selected bucket and range.
weight: 910
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
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#repair_keys_range
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/aae-fold-api/repair-key-range.md
related:
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/repair-a-selected-key-range
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Queue read repair for keys in a selected bucket and range.

## Invocation

{{< cli-example key="erlang:riak_client:aae_fold:repair_keys_range" >}}

The linked command page supplies all arities and the complete tuple/type contract from the release metadata. Filters are described in [Fold filters]({{< product-version-root >}}reference/aae-fold-api/fold-filters/).

## Behaviour

The reader maintenance path processes the queued keys. A submission count is not repair completion. The operation reconciles current surviving versions and cannot undo a valid application update.
