---
title: Count retained tombstones
description: Count retained tombstones without queuing reclamation.
weight: 1000
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\count-tombs.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/aae-fold/count-tombstones.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- reference/aae-fold-api/count-tombstones
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/data-and-consistency/deletion-tombstones-and-expiration
---

Count retained tombstones without queuing reclamation.

## Prepare the scope

Enable TicTac AAE and wait for its initial stores and trees. Open the node's remote console using [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). Keep the final method as `count`. Match the intended future reaping scope exactly, including type, key bounds, segment filter, and modified-time bounds.

## Run the fold

{{< cli-example key="erlang:riak_client:aae_fold:reap_tombs" args=`{reap_tombs, <<"events">>, all, all, all, count}` >}}

The bucket and range in this example are placeholders for your reviewed scope. For a long-running operation or a large result, use the CLI file-output workflow in [Run and retrieve a long-running AAE fold]({{< product-version-root >}}how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold/). See [Count tombstones]({{< product-version-root >}}reference/aae-fold-api/count-tombstones/) for the complete argument and result contract.

## Verify

Record the count and compare it with retention expectations. Investigate unexplained growth or missing deletions before scheduling a mutating operation.
