---
title: 'Replication queues'
description: 'Explain replication queues, its data flow, failure behavior, and operational trade-offs.'
weight: 7
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#concepts---queues-and-workers'
  - 'https://openriak.github.io/riak/RiakTheoryGuide.html#disk-backed-queues'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain replication queues, its data flow, failure behavior, and operational trade-offs.

## Overview

### Concepts - Queues and Workers

Replication queues use the [disk-backed queue framework]({{< baseurl >}}kv/3.4.0/explanation/replication/queues/) common across multiple Riak services.

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
  - Sufficient sink workers need to be configured to keep-up with real-time replication, though [this number can be adjusted at runtime]({{< baseurl >}}kv/3.4.0/reference/replication-api/runtime-controls/).
  - There is some protection from over-provisioning but not from under-provisioning.

In handling replication events, sink workers must apply the replicated change into the local cluster, and this uses a specific `PUSH` command.  The sink workers are constrained in that:

- A sink worker can fetch only one object at a time, and must `PUSH` that object into the sink cluster before returning to fetch the next available replication event.
  - Inter-cluster latency will be a factor in the replication throughput achievable by a group of sink workers.
- A sink-worker will never prompt re-replication, it will only `PUSH` that update into the local cluster;
  - The `PUSH` is configured to put an object `asis` and not to be a coordinated change, so that it will **not** be passed to the local replication source queue manager.

Configuring and enabling source queues and sink workers is sufficient to enable real-time replication.  Other replication features (such as full-sync reconciliation) depend on the queues and workers to operate, but require additional configuration to be triggered.

#### Disk-backed Queues

There are four internal Riak services that are built on a common queue behaviour: real-time replication, the reaper, the eraser and the reader.

These queues have a small in-memory portion, but once the queues grow beyond that minimal size they are written to disk using the internal Erlang `disk_log` facility.  The use of disk for the queue is solely to control the amount of memory consumed by the queue, as Riak has no protection against the overuse of memory within a node.  When a node is restarted, the disk-based queues will be erased.  This prevents a situation where a restart due to corruption of a queue, leads to a continuous cycle of reboots as the same corruption is reprocessed.

Each queue has multiple priorities, and an item added to the queue is assigned a priority.  Higher priority items are always consumed before lower priority items.
