---
title: Configure and schedule fullsync
description: Schedule TicTac fullsync checks and verify that discovered differences are delivered through the replication
  queues. Prepare source queues, sink workers, and usable AAE trees first.
weight: 640
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\replication\fullsync.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\next-gen-replication\fullsync.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\performance\v2-scheduling-fullsync.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v2-multi-datacenter\scheduling-fullsync.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v3-multi-datacenter\scheduling-fullsync.md
- Legacy multi-datacenter replication terminology and commands require compatibility review.
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ReplicationGuide.html#configuration-of-all-cluster-reconciliation
- https://openriak.github.io/riak/ReplicationGuide.html#enabling-checks
- https://openriak.github.io/riak/ReplicationGuide.html#initial-configuration
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/configure-fullsync.md
related:
- how-to/replication-and-reconciliation/enable-tictac-anti-entropy
- how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- how-to/performance/tune-replication-throughput-and-lag
- reference/replication-interfaces/fullsync-requests-and-results
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
previous_page: how-to/replication-and-reconciliation/enable-real-time-replication
---

Schedule TicTac fullsync checks and verify that discovered differences are delivered through the replication queues. Prepare source queues, sink workers, and usable AAE trees first.

## Configure one peer relationship per node

Set the scope to `all`, the local source queue, the remote peer's address and protocol, and both clusters' actual `n_val`. For bidirectional repair, also set the remote queue that the local consumers read. A manager has one peer configuration; distribute additional relationships across nodes deliberately.

{{< configuration-reference-table >}}
^ttaaefs_
{{< /configuration-reference-table >}}

Use different cluster slices for opposing clusters. Set an autocheck rate appropriate to the total number of participating nodes: a per-node schedule multiplies across the deployment. Prefer autochecks over overlapping fixed hour/day/range schedules unless you have a measured reason.

## Prompt and observe a check

After applying the configuration and restarting as needed, open a remote console and submit:

{{< cli-example key="erlang:riak_client:ttaaefs_fullsync" args="all_check" >}}

Follow the exchange to completion in logs. A returned submission result is not proof of convergence. Allow discovered repairs to flow through the sink, then repeat until the relevant completed exchange reports `in_sync=true`.

## Tune only from evidence

Track exchange duration, timeouts, worker backlog, and repair counts. If jobs overlap or time out in queues, reduce scheduling pressure before increasing work limits. For a known large gap, seed the affected range using [Re-replicate a key range or time window]({{< product-version-root >}}how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window/) rather than repeatedly widening every fullsync request.
