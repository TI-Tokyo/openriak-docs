---
title: 'Ring changes and handoffs'
description: 'Explain ring changes and handoffs, including relevant state transitions, risks, and recovery assumptions.'
weight: 5
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
  - 'architects'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/RiakTheoryGuide.html#riak-core-cluster-management'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain ring changes and handoffs, including relevant state transitions, risks, and recovery assumptions.

## Overview

### Riak Core cluster management

The OpenRiak KV store is built on top of a generic platform for building distributed systems called `riak_core`.  The `riak_core` system provides the underlying components for controlling and managing a clustered application:

- `riak_core_ring`
  - An implementation of [the ring](/kv/3.4.1/explanation/foundations/clusters-rings-and-partitions/), the distribution function in Riak.
- `riak_core_ring_manager`
  - A process that marshals updates to the ring, and ensures that stable versions of the ring are available to database processes via a low latency cache.
- `riak_core_vnode`
  - The behaviour which the `riak_kv_vnode` implements, defining the callback functions necessary for the vnode to handle requests and also changes to the ring (e.g. handoffs).
- `riak_core_vnode_proxy`
  - Every vnode has a proxy that forwards requests to the vnode, whilst tracking the size of the message queue on the vnode.
  - The proxy is responsible for blocking access to the vnode when the message queue (also known as the mailbox) is overloaded.
  - All vnode requests are forwarded through the proxy, but responses bypass the proxy and are sent directly back to the requesting process.
- `riak_core_vnode_manager`
  - Responsible for starting local vnodes when required by the ring, and stopping those vnodes no longer required.
    - The receipt of a request for a vnode that is not started locally, will also prompt the starting of a vnode - there is no wait for periodic ring checks to detect the change of topology.
  - Also triggers handoffs for vnodes in response to cluster changes, through the `riak_core_handoff_manager`.
  - The initial trigger for a handoff is a vnode timeout, when a vnode sees a period of inactivity beyond the timeout, it will contact the `riak_core_vnode_manager` to see if a handoff is required.
- `riak_core_handoff_manager`
  - Manages handoffs required for cluster topology changes or vnode repairs.
  - Applies concurrency controls, tracking progress and the success or failure of transfers
- `riak_core_capability`
  - A mechanism for registering the capability of a node, and then discovering the "lowest capability" for a given feature supported by all nodes in the cluster.
  - Required to manage functional changes dependent on the availability of updated features, in the presence of rolling upgrades.
- `riak_core_metadata_manager`
  - Stores a node-specific copy of cluster-wide metadata, detecting and resolving differences in metadata between nodes in the cluster.
  - The cluster metadata is used for information about bucket types, and security controls.
- `riak_core_claimant`
  - A cluster node through which cluster administration changes are prompted.

For further information on `riak_core`, there is a lightweight version of `riak_core` called `riak_core-lite` [for which there are helpful tutorials](https://riak-core-lite.github.io/).
