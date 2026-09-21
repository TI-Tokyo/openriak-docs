---
title: Repair a selected key range
description: Request read repair for a known key range without rebuilding an entire node.
weight: 1010
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\repair-keys-range.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#repair-key-ranges
- https://openriak.github.io/riak/OtherAPI.html#repair_keys_range
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/aae-fold/repair-key-range.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- reference/aae-fold-api/repair-keys-in-a-range
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
---

Request read repair for a known key range without rebuilding an entire node.

## Prepare the scope

Enable TicTac AAE and wait for its initial stores and trees. Open the node's remote console using [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). Confirm that surviving replicas hold the desired values and that the inclusive range is correct. This repairs replicas of current objects; it does not undo an application's unwanted but valid write.

## Run the fold

{{< cli-example key="erlang:riak_client:aae_fold:repair_keys_range" args=`{repair_keys_range, <<"events">>, {<<"event-001">>, <<"event-099">>}, all, all}` >}}

The bucket and range in this example are placeholders for your reviewed scope. For a long-running operation or a large result, use the CLI file-output workflow in [Run and retrieve a long-running AAE fold]({{< product-version-root >}}how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold/). See [Repair keys in a range]({{< product-version-root >}}reference/aae-fold-api/repair-keys-in-a-range/) for the complete argument and result contract.

## Verify

Monitor reader queues and completion logs, then reread known keys and compare AAE observations. The submission count is not proof that all repairs have finished.
