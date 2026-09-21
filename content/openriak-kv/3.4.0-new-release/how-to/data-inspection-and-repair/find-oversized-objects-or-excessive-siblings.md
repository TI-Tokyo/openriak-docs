---
title: Find oversized objects or excessive siblings
description: Find keys whose object size or sibling count exceeds a chosen threshold.
weight: 960
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\find-keys.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#find_keys
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/aae-fold/find-keys.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- reference/aae-fold-api/find-keys
- reference/aae-fold-api/fold-filters
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
---

Find keys whose object size or sibling count exceeds a chosen threshold.

## Prepare the scope

Enable TicTac AAE and wait for its initial stores and trees. Open the node's remote console using [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). Choose a small bucket or key/time interval first. The example finds objects with more than two siblings; use `{object_size, BYTES}` for a size threshold. Large matches can consume substantial result memory.

## Run the fold

{{< cli-example key="erlang:riak_client:aae_fold:find_keys" args=`{find_keys, <<"events">>, all, all, {sibling_count, 2}}` >}}

The bucket and range in this example are placeholders for your reviewed scope. For a long-running operation or a large result, use the CLI file-output workflow in [Run and retrieve a long-running AAE fold]({{< product-version-root >}}how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold/). See [Find keys]({{< product-version-root >}}reference/aae-fold-api/find-keys/) for the complete argument and result contract.

## Verify

Fetch a small sample and confirm its values and metadata. Fix the application's object growth or conflict policy before attempting repeated broad repairs.
