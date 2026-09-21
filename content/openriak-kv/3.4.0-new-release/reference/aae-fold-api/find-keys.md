---
title: Find keys
description: Find keys exceeding an object-size or sibling-count threshold.
weight: 860
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
- https://openriak.github.io/riak/OtherAPI.html#find_keys
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/aae-fold-api/find-keys.md
related:
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/find-oversized-objects-or-excessive-siblings
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Find keys exceeding an object-size or sibling-count threshold.

## Invocation

{{< cli-example key="erlang:riak_client:aae_fold:find_keys" >}}

The linked command page supplies all arities and the complete tuple/type contract from the release metadata. Filters are described in [Fold filters]({{< product-version-root >}}reference/aae-fold-api/fold-filters/).

## Behaviour

The threshold selects oversized objects or excessive siblings; it is not a count of all keys. Results can be large and are collected before a completed file result is emitted. Bound bucket, key, and modified-time scope.
