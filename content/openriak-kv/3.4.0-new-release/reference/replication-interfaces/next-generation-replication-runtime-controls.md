---
title: Next-generation replication runtime controls
description: Next-generation replication has source-queue, sink-consumer, and TicTac fullsync controls. These Erlang
  entry points are release-sensitive operational interfaces; they are separate from legacy `riak repl` commands.
weight: 960
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\v2-multi-datacenter.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\v3-multi-datacenter.md
- Legacy multi-datacenter replication terminology and commands require compatibility review.
source_material:
- legacy-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ReplicationGuide.html#configure-and-monitor-work-queues
- https://openriak.github.io/riak/ReplicationGuide.html#making-runtime-changes-to-the-sink
- https://openriak.github.io/riak/ReplicationGuide.html#making-runtime-changes-to-the-source
- https://openriak.github.io/riak/ReplicationGuide.html#monitoring-and-runtime-changes
- https://openriak.github.io/riak/ReplicationGuide.html#overriding-the-range
- https://openriak.github.io/riak/ReplicationGuide.html#participate-in-coverage
- https://openriak.github.io/riak/ReplicationGuide.html#prompting-a-reconciliation-check
- https://openriak.github.io/riak/ReplicationGuide.html#re-sync-a-bucket
- https://openriak.github.io/riak/ReplicationGuide.html#suspend-full-sync
- https://openriak.github.io/riak/ReplicationGuide.html#trigger-tree-repairs
- https://openriak.github.io/riak/ReplicationGuide.html#tuning-checks---the-maximum-results-limit
- https://openriak.github.io/riak/ReplicationGuide.html#update-the-request-limits
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/replication-api/runtime-controls.md
related:
- reference/configuration/next-generation-replication-settings
- reference/replication-interfaces/fullsync-requests-and-results
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
---

Next-generation replication has source-queue, sink-consumer, and TicTac fullsync controls. These Erlang entry points are release-sensitive operational interfaces; they are separate from legacy `riak repl` commands.

## Source queues

{{< cli-command-index prefix="erlang/riak-kv-replrtq-src" >}}

## Sink consumers

{{< cli-command-index prefix="erlang/riak-kv-replrtq-snk" >}}

## Reconciliation

{{< cli-command-index prefix="erlang/riak-kv-ttaaefs-manager" >}}

Runtime changes act on the scope described by each function. Record persistent configuration separately: changing a live process does not necessarily update what is restored after a restart.
