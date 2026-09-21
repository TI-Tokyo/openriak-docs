---
title: Object statistics
description: Return object statistics for a bucket and optional key and modified-time bounds.
weight: 900
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
- https://openriak.github.io/riak/OtherAPI.html#object_stats
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/aae-fold-api/object-statistics.md
related:
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/measure-object-sizes-and-sibling-distributions
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Return object statistics for a bucket and optional key and modified-time bounds.

## Invocation

{{< cli-example key="erlang:riak_client:aae_fold:object_stats" >}}

The linked command page supplies all arities and the complete tuple/type contract from the release metadata. Filters are described in [Fold filters]({{< product-version-root >}}reference/aae-fold-api/fold-filters/).

## Behaviour

The result includes total count, total size, size-distribution bands, and sibling-count bands. Compare the same scope over time; concurrent writes and AAE readiness affect interpretation.
