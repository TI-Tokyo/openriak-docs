---
title: Enable real-time replication
description: Enable real-time replication for newly coordinated writes after the source queues and destination consumers
  are prepared.
weight: 610
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\replication\real-time.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\next-gen-replication\realtime.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ReplicationGuide.html#configuration-of-real-time-replication
- https://openriak.github.io/riak/ReplicationGuide.html#enable-a-real-time-sink
- https://openriak.github.io/riak/ReplicationGuide.html#enable-a-real-time-source
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/configure-real-time-replication.md
related:
- how-to/replication-and-reconciliation/configure-replication-queues-and-filters
- how-to/replication-and-reconciliation/configure-sink-nodes-and-consumers
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window
- reference/configuration/next-generation-replication-settings
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
previous_page: how-to/replication-and-reconciliation/configure-sink-nodes-and-consumers
next_page: how-to/replication-and-reconciliation/configure-and-schedule-fullsync
---

Enable real-time replication for newly coordinated writes after the source queues and destination consumers are prepared.

## Enable source queuing

On every source node, configure a queue for the intended destination. This example sends all eligible writes to `cluster_b`:

{{< settings-example >}}
replrtq_enablesrc = enabled
replrtq_srcqueue = cluster_b:any
{{< /settings-example >}}

The filter name and queue name have different roles; use [Configure replication queues and filters]({{< product-version-root >}}how-to/replication-and-reconciliation/configure-replication-queues-and-filters/) for narrower filters. Apply the persistent configuration in a controlled restart sequence. A write can be coordinated on a node other than the one that accepted the client connection, so configuring only the client-facing node is insufficient.

## Enable destination consumers

Follow [Configure sink nodes and consumers]({{< product-version-root >}}how-to/replication-and-reconciliation/configure-sink-nodes-and-consumers/) using the same queue name. Ensure the destination has matching bucket types and permissions, and configure retained tombstones and reaping consistently with [Choose a deletion and retention policy]({{< product-version-root >}}how-to/planning-a-deployment/choose-a-deletion-and-retention-policy/).

## Verify a change

Write a unique sample key at the source, read it at the destination, update it with its causal context, then delete it. Wait for each asynchronous transition and inspect sink errors if delivery stalls. Existing objects written before source queuing was enabled require seeding; use [Re-replicate a key range or time window]({{< product-version-root >}}how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window/).

Finally configure reconciliation with [Configure and schedule fullsync]({{< product-version-root >}}how-to/replication-and-reconciliation/configure-and-schedule-fullsync/) so missed real-time references can be recovered.
