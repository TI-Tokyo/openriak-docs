---
title: Tree and clock exchange operations
weight: 950
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Tree and clock exchange folds expose anti-entropy comparison data. They are release-sensitive interfaces
  used by reconciliation, not ordinary application object queries.
related:
- reference/aae-fold-api/fold-invocation-and-result-conventions
- reference/aae-fold-api/fold-filters
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Tree and clock exchange folds expose anti-entropy comparison data. They are release-sensitive interfaces used by reconciliation, not ordinary application object queries.

## Cached-tree comparisons

- {{< cli key="erlang:riak_client:aae_fold:merge_root_nval" >}}
- {{< cli key="erlang:riak_client:aae_fold:merge_branch_nval" >}}
- {{< cli key="erlang:riak_client:aae_fold:fetch_clocks_nval" >}}

These operations use the replica-count scope required by the cached-tree exchange.

## Range comparisons

- {{< cli key="erlang:riak_client:aae_fold:merge_tree_range" >}}
- {{< cli key="erlang:riak_client:aae_fold:fetch_clocks_range" >}}

The linked entries define the exact tuple forms, filters, and exported argument types. Tree sizes, segments, key ranges, and hashing choices must be interpreted as one compatible exchange protocol; combining fields from unrelated exchanges does not produce a meaningful comparison.
