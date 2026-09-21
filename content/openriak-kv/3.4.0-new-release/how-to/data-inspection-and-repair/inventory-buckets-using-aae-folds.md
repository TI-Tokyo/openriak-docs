---
title: Inventory buckets using AAE folds
description: Inventory buckets visible through AAE coverage.
weight: 950
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\list-buckets.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#list_buckets
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/aae-fold/list-buckets.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- reference/aae-fold-api/list-buckets
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
---

Inventory buckets visible through AAE coverage.

## Prepare the scope

Enable TicTac AAE and wait for its initial stores and trees. Open the node's remote console using [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). Use the actual replica value for the covered data, not an assumed cluster-wide value. If buckets use different values, plan coverage for those values and deduplicate results; a coverage value larger than a bucket's replica count can omit data.

## Run the fold

{{< cli-example key="erlang:riak_client:aae_fold:list_buckets" args=`{list_buckets, 3}` >}}

The value `3` is an example coverage value; replace it with the value selected for your data. This fold inventories buckets and does not take a bucket-name or key-range filter. For a long-running operation or a large result, use the CLI file-output workflow in [Run and retrieve a long-running AAE fold]({{< product-version-root >}}how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold/). See [List buckets]({{< product-version-root >}}reference/aae-fold-api/list-buckets/) for the complete argument and result contract.

## Verify

Compare the result with known active buckets. Empty buckets do not necessarily appear because the fold discovers stored data. Keep type and bucket together when planning a migration.
