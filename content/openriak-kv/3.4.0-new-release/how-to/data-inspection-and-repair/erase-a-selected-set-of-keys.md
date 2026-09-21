---
title: Erase a selected set of keys
description: Erase a selected set of live keys through the bounded AAE eraser workflow.
weight: 1020
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\erase-keys.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#erase_keys
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/aae-fold/erase-keys.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- reference/aae-fold-api/erase-keys
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/data-and-consistency/deletion-tombstones-and-expiration
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Erase a selected set of live keys through the bounded AAE eraser workflow.

## Prepare the scope

Enable TicTac AAE and wait for its initial stores and trees. Open the node's remote console using [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). First run the exact same scope with the final method `count`, inspect representative keys, and preserve any required recovery copy. The example below changes data: `local` queues erasure on the participating nodes. Avoid broad `all` ranges until the scope has been reviewed.

## Run the fold

{{< cli-example key="erlang:riak_client:aae_fold:erase_keys" args=`{erase_keys, <<"events">>, {<<"expired-001">>, <<"expired-099">>}, all, all, local}` >}}

The bucket and range in this example are placeholders for your reviewed scope. For a long-running operation or a large result, use the CLI file-output workflow in [Run and retrieve a long-running AAE fold]({{< product-version-root >}}how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold/). See [Erase keys]({{< product-version-root >}}reference/aae-fold-api/erase-keys/) for the complete argument and result contract.

## Verify

Wait for eraser work and required replication to complete. Read selected keys to confirm deletion and check client latency. Tombstone reclamation is a separate later operation.
