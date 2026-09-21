---
title: Reap tombstones
description: Count or queue reclamation of retained tombstones.
weight: 930
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
- https://openriak.github.io/riak/OtherAPI.html#reap_tombs
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/aae-fold-api/reap-tombstones.md
related:
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/reap-eligible-tombstones
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Count or queue reclamation of retained tombstones.

## Invocation

{{< cli-example key="erlang:riak_client:aae_fold:reap_tombs" >}}

The linked command page supplies all arities and the complete tuple/type contract from the release metadata. Filters are described in [Fold filters]({{< product-version-root >}}reference/aae-fold-api/fold-filters/).

## Behaviour

`count` is non-mutating. Reaping removes deletion evidence and requires a retention and convergence policy covering unavailable replicas and connected clusters. Avoid overlap with membership changes.
