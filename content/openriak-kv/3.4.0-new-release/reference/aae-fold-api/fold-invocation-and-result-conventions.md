---
title: Fold invocation and result conventions
description: AAE folds perform cluster-wide inspection or queue bounded maintenance work. They require active TicTac
  AAE and usable native or parallel stores.
weight: 830
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- developers
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\guides\tictac-active-anti-entropy\tictac-active-anti-entropy.md
source_material:
- openriak-quickdocs-3.4
- live-3.2.5
- proposed-kv
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#aae-fold-api
- https://openriak.github.io/riak/OtherAPI.html#aae-fold-efficiency
- https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-http
- https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-pb
- https://openriak.github.io/riak/OtherAPI.html#fetch_clocks_nval
- https://openriak.github.io/riak/OtherAPI.html#fetch_clocks_range
- https://openriak.github.io/riak/OtherAPI.html#merge_branch_nval
- https://openriak.github.io/riak/OtherAPI.html#merge_root_nval
- https://openriak.github.io/riak/OtherAPI.html#merge_tree_range
- https://openriak.github.io/riak/OtherAPI.html#performance-and-efficiency
- https://openriak.github.io/riak/OtherAPI.html#repl_keys_range
- https://openriak.github.io/riak/OtherAPI.html#riak-kv---other-apis
- https://openriak.github.io/riak/OtherAPI.html#supported-fold-types
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/aae-fold-api/_index.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- reference/aae-fold-api/fold-filters
- reference/aae-fold-api/list-buckets
- reference/aae-fold-api/find-keys
- reference/aae-fold-api/object-statistics
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

AAE folds perform cluster-wide inspection or queue bounded maintenance work. They require active TicTac AAE and usable native or parallel stores.

## Invocation interfaces

The CLI writes completed JSON results to a file:

{{< cli-example key="shell:riak admin tictacaae fold" >}}

Erlang invocations use the operation-specific tuple contract. The catalogue includes every supported fold form and its argument types:

{{< cli-command-index prefix="erlang/riak-client/aae-fold" >}}

HTTP and PB transports expose corresponding operational interfaces; use the selected operation's documented request and result form rather than translating tuple positions by guesswork.

## Results and side effects

Read-only folds return collected data or counts. Repair, replication, erasure, and reaping folds can report queued work before consumers have completed it. A count method is non-mutating only for operations that explicitly support it.

Large listings can consume significant memory even when results are eventually written to a file. Key ranges, modified-time ranges, segments, and coverage values constrain different aspects of a fold; see [Fold filters]({{< product-version-root >}}reference/aae-fold-api/fold-filters/).

## Readiness and consistency

Initial or incomplete AAE stores can affect results. Concurrent application changes mean a fold is not an atomic snapshot of the whole cluster. Monitor worker pressure and use the smallest scope that answers the operational question.
