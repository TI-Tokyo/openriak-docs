---
title: Erase keys
description: Count or queue deletion of live keys in a selected scope.
weight: 920
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
- https://openriak.github.io/riak/OtherAPI.html#erase_keys
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/aae-fold-api/erase-keys.md
related:
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/erase-a-selected-set-of-keys
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Count or queue deletion of live keys in a selected scope.

## Invocation

{{< cli-example key="erlang:riak_client:aae_fold:erase_keys" >}}

The linked command page supplies all arities and the complete tuple/type contract from the release metadata. Filters are described in [Fold filters]({{< product-version-root >}}reference/aae-fold-api/fold-filters/).

## Behaviour

`count` is a non-mutating candidate count. A mutating change method feeds the eraser; deletion and subsequent tombstone reclamation are separate operations. Verify retention and the exact scope before submitting work.
