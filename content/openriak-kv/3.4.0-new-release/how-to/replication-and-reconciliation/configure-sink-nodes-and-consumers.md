---
title: Configure sink nodes and consumers
description: Configure sink workers to consume a named source queue and apply its objects locally. Have the destination's
  bucket types ready before enabling consumption.
weight: 630
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\replication\sink.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\next-gen-replication\sink.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ReplicationGuide.html#enable-a-real-time-sink
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/configure-sink-nodes.md
related:
- how-to/replication-and-reconciliation/configure-replication-queues-and-filters
- how-to/replication-and-reconciliation/secure-next-generation-replication-connections
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- how-to/performance/tune-replication-throughput-and-lag
- reference/configuration/next-generation-replication-settings
- reference/replication-interfaces/next-generation-replication-runtime-controls
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
previous_page: how-to/replication-and-reconciliation/configure-replication-queues-and-filters
next_page: how-to/replication-and-reconciliation/enable-real-time-replication
---

Configure sink workers to consume a named source queue and apply its objects locally. Have the destination's bucket types ready before enabling consumption.

## Define peers and workers

Choose several reachable source listeners for resilience. Select PB for protected replication; peer discovery requires listeners that advertise addresses the sink can actually reach. A listener bound to an unspecified address is not a usable discovered peer address.

{{< configuration-reference-table >}}
^replrtq_(enablesink|sinkqueue|sinkpeers|sinkworkers|sinkpeerlimit|peer_discovery|vnodecheck)$
{{< /configuration-reference-table >}}

Set the sink queue name exactly as defined on the source. Start with a measured worker count and peer limit that the destination can absorb. Apply settings on the intended sink nodes, validate, and restart as required.

## Verify progress

Write a sample on the source and read it on the destination. Inspect sink fetch and push errors, source queue lengths, and application latency. More workers can increase pressure on both clusters; a larger pool is not automatically a fix for slow storage.

For a node being added to a sink cluster, suspend consumption until its membership is ready if early consumption would create unnecessary reconciliation work. Use the runtime controls in [Next-generation replication runtime controls]({{< product-version-root >}}reference/replication-interfaces/next-generation-replication-runtime-controls/) and persist any lasting changes in configuration.
