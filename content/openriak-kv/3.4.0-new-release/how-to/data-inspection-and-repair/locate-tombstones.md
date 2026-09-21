---
title: Locate tombstones
description: Locate retained tombstones before investigating deletion or planning reclamation.
weight: 990
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\find-tombs.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#find_tombs
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/aae-fold/find-tombstones.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- reference/aae-fold-api/find-tombstones
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/data-and-consistency/deletion-tombstones-and-expiration
---

Locate retained tombstones before investigating deletion or planning reclamation.

## Prepare the scope

Enable TicTac AAE and wait for its initial stores and trees. Open the node's remote console using [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). Select a bucket and preferably a key or modified-time interval. A tombstone result is not evidence that every remote cluster has already observed that deletion.

## Run the fold

{{< cli-example key="erlang:riak_client:aae_fold:find_tombs" args=`{find_tombs, <<"events">>, all, all, all}` >}}

The bucket and range in this example are placeholders for your reviewed scope. For a long-running operation or a large result, use the CLI file-output workflow in [Run and retrieve a long-running AAE fold]({{< product-version-root >}}how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold/). See [Find tombstones]({{< product-version-root >}}reference/aae-fold-api/find-tombstones/) for the complete argument and result contract.

## Verify

Compare known deleted keys and their context with the result. Keep the retained tombstones until replication and outage-recovery requirements are met.
