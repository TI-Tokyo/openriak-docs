---
title: Count objects in a selected scope
description: Count live keys in a selected AAE scope without erasing them.
weight: 970
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\count-keys.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/aae-fold/count-keys.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- reference/aae-fold-api/count-keys
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
---

Count live keys in a selected AAE scope without erasing them.

## Prepare the scope

Enable TicTac AAE and wait for its initial stores and trees. Open the node's remote console using [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). Keep the final change method as `count`. The operation name is shared with erasure, but count mode does not queue deletions. Use typed bucket and range filters from the reference where needed.

## Run the fold

{{< cli-example key="erlang:riak_client:aae_fold:erase_keys" args=`{erase_keys, <<"events">>, all, all, all, count}` >}}

The bucket and range in this example are placeholders for your reviewed scope. For a long-running operation or a large result, use the CLI file-output workflow in [Run and retrieve a long-running AAE fold]({{< product-version-root >}}how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold/). See [Count keys]({{< product-version-root >}}reference/aae-fold-api/count-keys/) for the complete argument and result contract.

## Verify

Inspect the completed count and compare it with a known sample. Concurrent writes and coverage readiness affect interpretation; this is not a transactional snapshot.
