---
title: Choose a multi-cluster topology
description: Choose the direction and purpose of every inter-cluster replication relationship. Separate application
  availability, disaster recovery, migration, and backup requirements before configuring peers.
weight: 90
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#interconnecting-multiple-clusters
- https://openriak.github.io/riak/InitialDesignDecisions.html#interconnecting-multiple-clusters---making-a-choice
tags:
- diataxis
- kv
- how-to
- quickdocs
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/plan/choose-multi-cluster-topology.md
related:
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- how-to/replication-and-reconciliation/configure-replication-queues-and-filters
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- how-to/replication-and-reconciliation/secure-next-generation-replication-connections
- tutorials/replication-and-reconciliation/explore-bidirectional-replication
- foundations/replication-and-repair/multi-cluster-topologies-and-behaviour
- foundations/replication-and-repair/replication-sources-queues-and-sinks
---

Choose the direction and purpose of every inter-cluster replication relationship. Separate application availability, disaster recovery, migration, and backup requirements before configuring peers.

## Draw the data paths

For each cluster, list the applications allowed to write, which buckets must be received, the permitted recovery lag, and the intended failover procedure. Use one-way replication for a destination that should not originate application updates. Use bidirectional paths when both sides write and the application can resolve conflicts.

## Define direct relationships

Create a separate source queue for each independent destination. A replicated push does not automatically become a new real-time event for a third cluster, so do not assume a chain will relay updates. Configure the required direct peer relationships and matching bucket types.

## Plan reconciliation and cutover

Pair real-time delivery with reconciliation. Reserve capacity for a backlog after an outage and test the failover endpoint switch. Define how credentials, bucket properties, certificates, and other cluster metadata are provisioned separately; object replication does not copy those items.

## Verify the topology

Write a distinct sample in each permitted source and confirm its appearance only at intended destinations. Pause a consumer, create changes, and prove catch-up and reconciliation before relying on the topology.
