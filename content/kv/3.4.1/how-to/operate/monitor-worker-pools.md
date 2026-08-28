---
title: 'Monitor node worker pools'
description: 'Show operators how to inspect worker-pool utilization, backlogs, and saturation symptoms.'
weight: 25
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-node-worker-pools'
  - 'https://openriak.github.io/riak/OtherAPI.html#node-worker-pools'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#concepts---queues-and-workers'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#configure-and-monitor-work-queues'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to inspect worker-pool utilization, backlogs, and saturation symptoms.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Monitoring node worker pools

Each worker pool will regularly log its current queue length and last checkout time (when it last picked up a new piece of work).  There are also riak stats for each pool, giving the average queue time (how long work is waiting in the queue), and work time (how long each piece of work takes).

#### Node worker pools

Riak API requests are generally not subject to constraints on the resources they use.  If there exists contention over available CPU cores within a busy cluster, the contention is managed by the Erlang scheduler, and the database backends are designed to degrade gradually - to slow smoothly as available resources are restricted.

In contrast, the AAE Fold API has specific constraints on throughput, governed by the node worker pools.  These pools are defined to constrain concurrency for operational queries, to provide an upper limit on how many CPU cores may be used by different classes of operational work.  There is no guarantee that worker pools will be able to use their limit - use of each core is still managed fairly by the erlang scheduler for that core.

The node worker pool can be configured via the `worker_pool_strategy` in riak.conf, and can be set to three different modes:

- `none`; do not use node worker pools.
  - aae_folds and other operational work will be fairly scheduled by the erlang scheduler alongside other activity.
  - the folds will share the `vnode_worker_pool` used by folds for the Query API.
- `single`; use a single pool of work for all operational work.
  - This means the whole bandwidth for operational work can be consumed by any operational work.
  - No segmentation, so one set of jobs may prevent other work from finding available capacity.
- `dscp`; divides pools up into categories based on the network pooling strategy of differentiated services.
  - There is no Expedited Forwarding queue, this is assumed to be the `vnode_worker_pool`.
  - There are four Assured Forwarding queues: AF1 (cached tree rebuilds, hot backups); AF2 (legacy key-listing); AF3 (AAE folds); AF4 (AAE folds).
  - There is a single Best Endeavours queue, this is used only for parallel aae store rebuilds.

When queueing items via a fold (e.g. `repl_keys_range`, `repair_keys_range`, `find_tombs` and `reap_tombs`), if a smaller node worker pool is used, then items will be added to the queue in batches by vnode.  When items are dequeued, this may result in phases of concentrated activity on particular preflists.

#### Concepts - Queues and Workers

Replication queues use the [disk-backed queue framework]({{< baseurl >}}kv/3.4.1/explanation/replication/queues/) common across multiple Riak services.

Replication references, which are primarily newly coordinated PUTs, are sent to the replication source queue process.  The real-time replication source then assesses which replication queues require that reference:

- Each node must be configured with a separate queue for each cluster or external service that is expected to receive replication events.
  - Each replication event will be duplicated to all queues relevant to that event, but only on one node within the cluster.
- Each queue is split by priority, so that real-time events are consumed prior to any events related to batch or reconciliation activity.
- Queues that grow beyond a configurable size are persisted to disk to manage the memory overhead of replication.
- The queues are all temporary (even when persisting to disk); replication references will be lost on node failure or on node restart.
  - Failures in real-time replication need to be recovered through reconciliation.

A Sink cluster, that is to receive replication events, must have sink workers configured to read from remote queues on Source clusters:

- Sink workers must be configured to point to at least one node in the Source cluster.
  - They may be configured to automatically discover other nodes within the cluster from that node.
- A sink worker can only be configured to read from one Source queue (by name) - but that name can exist on multiple nodes and/or clusters.  For a sink node to receive updates from multiple clusters, consistent queue names should be used across the source clusters.
  - Queue names are used to identify the entity interested in receiving the event.

The number of sink workers can be configured on the node:

- The sink workers will be distributed across the source peer nodes (either configured or discovered).
  - The number of workers will constrain the pace at which events can be pulled from a source cluster, and also the PUSH workload that a sink cluster can generate for itself.
- There is an overhead of a sink making requests on the source, so each sink worker will backoff if a request results in no replication events being discovered.
- The sink worker pool does not auto-expand.
  - Sufficient sink workers need to be configured to keep-up with real-time replication, though [this number can be adjusted at runtime]({{< baseurl >}}kv/3.4.1/reference/replication-api/runtime-controls/).
  - There is some protection from over-provisioning but not from under-provisioning.

In handling replication events, sink workers must apply the replicated change into the local cluster, and this uses a specific `PUSH` command.  The sink workers are constrained in that:

- A sink worker can fetch only one object at a time, and must `PUSH` that object into the sink cluster before returning to fetch the next available replication event.
  - Inter-cluster latency will be a factor in the replication throughput achievable by a group of sink workers.
- A sink-worker will never prompt re-replication, it will only `PUSH` that update into the local cluster;
  - The `PUSH` is configured to put an object `asis` and not to be a coordinated change, so that it will **not** be passed to the local replication source queue manager.

Configuring and enabling source queues and sink workers is sufficient to enable real-time replication.  Other replication features (such as full-sync reconciliation) depend on the queues and workers to operate, but require additional configuration to be triggered.

#### Configure and monitor work queues

The node worker pool configuration is [detailed further in the AAE fold API documentation]({{< baseurl >}}kv/3.4.1/how-to/operate/monitor-worker-pools/).

There are two per-node worker pool sizes which have particular relevance to full-sync: `af1_worker_pool_size = <size>`; `af3_worker_pool_size = <size>`.

The AF1 pool is used for rebuilds of the AAE tree cache, and the AF3 pool is used for key/clock fetches when using cluster-wide reconciliation.

If the full-sync processes are taking too long (perhaps as max_results or range_boost are set too aggressively) then the worker pools may backup.  At some stage there may develop a situation where all full-sync queries will time out as the queries will take too long to reach the front of the queue, and hence all the effort associated with the queries will be wasted.

By default there is a log prompted for every aae_fold on completion (all full-sync activity depends on aae_folds prompted on both the source and sink).  For more information on monitoring node worker pools [refer to the Operations guide]({{< baseurl >}}kv/3.4.1/how-to/operate/monitor-worker-pools/).

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
