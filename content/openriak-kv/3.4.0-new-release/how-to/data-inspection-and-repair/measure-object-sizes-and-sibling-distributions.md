---
title: Measure object sizes and sibling distributions
description: Measure object counts, sizes, and sibling distributions for a selected bucket.
weight: 980
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\object-stats.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#object_stats
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/aae-fold/object-statistics.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- reference/aae-fold-api/object-statistics
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
---

Measure object counts, sizes, and sibling distributions for a selected bucket.

## Prepare the scope

Enable TicTac AAE and wait for its initial stores and trees. Open the node's remote console using [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). Start with a representative bounded range. Select the same scope for comparisons over time so changes in the population do not masquerade as changes in object size.

## Run the fold

{{< cli-example key="erlang:riak_client:aae_fold:object_stats" args=`{object_stats, <<"events">>, all, all}` >}}

The bucket and range in this example are placeholders for your reviewed scope. For a long-running operation or a large result, use the CLI file-output workflow in [Run and retrieve a long-running AAE fold]({{< product-version-root >}}how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold/). See [Object statistics]({{< product-version-root >}}reference/aae-fold-api/object-statistics/) for the complete argument and result contract.

## Verify

Inspect total count, total size, size bands, and sibling bands. Investigate unexpectedly large objects or many siblings with a targeted find-keys fold.
