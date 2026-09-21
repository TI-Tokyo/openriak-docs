---
title: Replication sources, queues, and sinks
description: Next-generation replication moves objects from a source cluster through named queues to consumers in
  a sink cluster. Each connection has a direction; reverse replication is a separate path.
weight: 220
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
source_material:
- legacy-3.2.5
- source-code-release-notes-3.4
- live-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\replication\index.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\next-gen-replication.md
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/replication/next-generation-replication.md
- foundations/replication/queues.md
- foundations/replication/sink-nodes.md
related:
- foundations/replication-and-repair/real-time-replication-and-fullsync
- foundations/replication-and-repair/multi-cluster-topologies-and-behaviour
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- how-to/replication-and-reconciliation/configure-replication-queues-and-filters
- how-to/replication-and-reconciliation/configure-sink-nodes-and-consumers
- reference/replication-interfaces/next-generation-replication-runtime-controls
---

Next-generation replication moves objects from a source cluster through named queues to consumers in a sink cluster. Each connection has a direction; reverse replication is a separate path.

## Sources and queues

A source selects eligible changes and offers them through a queue. Queue definitions and filters determine which dataset a consumer sees. The queue can carry references or object information according to the implementation and configuration; the sink must use the matching interface.

Queues decouple incoming writes from downstream processing, but they are bounded resources. A destination that is unavailable or slower than the source can accumulate lag. A drained queue alone does not prove that two complete datasets agree.

## Sink consumers

Sink workers fetch queued work and apply it to local replicas. Their throughput depends on network transfer, source service, sink writes, and competition with other work. More consumers can help a constrained pipeline only while the underlying resources can handle them.

## Recovery

Real-time delivery carries ongoing changes. Reconciliation checks for differences that are not represented by currently queued work, including interruptions and historical divergence. Treat queue monitoring and dataset comparison as complementary checks.

The source/sink path is independent of the legacy `riak_repl` connection model; do not mix their runtime controls.
