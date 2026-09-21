---
title: List buckets
description: List bucket identifiers encountered by an AAE coverage plan.
weight: 850
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
- https://openriak.github.io/riak/OtherAPI.html#list_buckets
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/aae-fold-api/list-buckets.md
related:
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/inventory-buckets-using-aae-folds
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

List bucket identifiers encountered by an AAE coverage plan.

## Invocation

{{< cli-example key="erlang:riak_client:aae_fold:list_buckets" >}}

The linked command page supplies all arities and the complete tuple/type contract from the release metadata. Filters are described in [Fold filters]({{< product-version-root >}}reference/aae-fold-api/fold-filters/).

## Behaviour

The input replica value controls coverage. Empty buckets need not appear, and buckets with a smaller replica value can be missed by an unsuitable plan. Preserve type and bucket components in the result.
