---
title: Replicate keys in a range
weight: 940
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Queue current object versions for consumers of a named source queue.
related:
- reference/aae-fold-api/fold-filters
- how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Queue current object versions for consumers of a named source queue.

## Invocation

{{< cli-example key="erlang:riak_client:aae_fold:repl_keys_range" >}}

The linked command page supplies all arities and the complete tuple/type contract from the release metadata. Filters are described in [Fold filters]({{< product-version-root >}}reference/aae-fold-api/fold-filters/).

## Behaviour

The queue must exist on source nodes and have the intended sink consumers. Returned counts describe references queued, not destination writes completed. Current values matching a modified-time range are sent; historical versions are not reconstructed.
