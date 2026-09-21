---
title: Reap eligible tombstones
description: Reclaim retained tombstones only after the deletion has reached all required replicas and destinations.
weight: 1030
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\reap-tombs.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#reap_tombs
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/aae-fold/reap-tombstones.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- reference/aae-fold-api/reap-tombstones
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/data-and-consistency/deletion-tombstones-and-expiration
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Reclaim retained tombstones only after the deletion has reached all required replicas and destinations.

## Prepare the scope

Enable TicTac AAE and wait for its initial stores and trees. Open the node's remote console using [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). Complete reconciliation, account for disconnected replicas, and avoid overlapping membership changes. First run the exact scope with `count`. The example below uses `local` and queues removal of deletion evidence; do not use it as an ordinary delete operation.

## Run the fold

{{< cli-example key="erlang:riak_client:aae_fold:reap_tombs" args=`{reap_tombs, <<"events">>, {<<"expired-001">>, <<"expired-099">>}, all, all, local}` >}}

The bucket and range in this example are placeholders for your reviewed scope. For a long-running operation or a large result, use the CLI file-output workflow in [Run and retrieve a long-running AAE fold]({{< product-version-root >}}how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold/). See [Reap tombstones]({{< product-version-root >}}reference/aae-fold-api/reap-tombstones/) for the complete argument and result contract.

## Verify

Monitor reaper progress and replication of reap events where configured. Check that the selected tombstones disappear without live values reappearing. Keep the retention and reconciliation record with the job.
