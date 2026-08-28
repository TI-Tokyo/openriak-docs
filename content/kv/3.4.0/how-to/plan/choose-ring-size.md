---
title: 'Choose a ring size'
description: 'Show architects how to select a ring size from node count, CPU capacity, query workload, and expected growth.'
weight: 26
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#ring-size'
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#ring-size---making-a-choice'
tags: ['diataxis', 'kv', 'how-to', 'quickdocs']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show architects how to select a ring size from node count, CPU capacity, query workload, and expected growth.

## Before you begin

Access to the affected OpenRiak KV environment, the exact product version, a record of the current state, and a safe rollback plan.

## Overview

### Ring size - making a choice

A OpenRiak cluster distributes data across individual databases (known as vnodes), and those databases are then distributed across the physical nodes and locations of the cluster.  The distribution of data within Riak is referred to as [the ring](/kv/3.4.0/explanation/foundations/clusters-rings-and-partitions/). The number of vnodes in the databases is required to be a factor of 2, and bigger than the total number of nodes in the database cluster.  This number is known as the ring size.

Starting with a large ring size is helpful as:

- It provides greater potential for future scalability of the cluster, as for efficient use of hardware there should always be at least one vnode per CPU core within the cluster (and preferably multiple vnodes per CPU core).
- It provides for more even distribution of load, as if `RingSize div NodeCount = K` each node will have either `K` or `K + 1` vnodes - and the relative delta between the size of `K` and `K + 1` decreases as the RingSize increases (e.g. with a node count of 6, there is a 10% difference between the resource required for a busy vs quiet node with a Ring Size of 64, but just a 2.3% difference with a Ring Size of 256).
- Background database activity is split by vnode, so increasing the number of vnodes has a smoothing impact on that load making it more predictable.

Starting with a smaller ring size is helpful as:

- Index queries, where a small number of results (i.e. < 10K) are returned are more efficient with a smaller ring size.  If 1% of the overall database throughput is such queries, then a shift up in ring size can reduce efficiency by up to 10% - but with less load of such queries, the impact is less.
- There is a lower per-node memory footprint (with the leveled backend) if the vnode count per node is lower - although that footprint can be addressed through other means (e.g. reducing the `penciller_cache_size`).
- Background database activity is split by vnode, so decreasing the number of vnodes reduces the overall volume of such activity.

> A ring size of `512` is a reasonable starting configuration for production clusters; unless there is a short-term goal to scale to much more than 1 billion objects.

A ring-size of `16` is a reasonable starting configuration for a single-node non-production Riak system; unless there is a short-term goal to scale-up the use of a high number of CPU cores on the node.

## Verify the result

Confirm the requested outcome, inspect cluster health and logs, and test the relevant client or operational path.
