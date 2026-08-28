---
title: 'Plan and commit a cluster change'
description: 'Show operators how to stage, plan, verify, commit, and monitor a cluster membership change.'
weight: 18
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
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#forming-and-expanding-a-riak-cluster'
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---commit-the-plan'
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---plan-a-change'
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---verify-the-plan'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to stage, plan, verify, commit, and monitor a cluster membership change.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Forming and Expanding an OpenRiak cluster

Riak may be deployed in the style of a traditional database, with a single node primary "cluster", and a single node standby "cluster" - with the replication and reconciliation controls in Riak used to make sure that primary and secondary remain in-sync.  Such setups are commonly only found in non-production environments, the power of Riak is only truly realised when it is used as a scale-out database, and:

- `n_val` is at least 3 (there are three copies of the data stored for resilience in the cluster);
- the node count is at least 6;
- the ring_size is set so there are at least 2 vnodes for every CPU core in the cluster.

With modern hardware, a simple configuration such as this can achieve a very high throughput, whilst holding a large volume of data - a higher throughput than most small enterprises would ever require in their infrastructure.  As a consequence Riak is primarily targeted at technology companies, cloud providers, large enterprises or large public-sector organisations with nation-scale requirements.

> The largest Riak users have o(1000) nodes, but these are generally split into different clusters serving different purposes or geographies.  It is rare to have individual clusters that scale beyond 50 nodes.

A cluster is formed by joining nodes into a cluster.  When a Riak node is started, it is a cluster of one, and so the act of joining one node to another is actually the act of merging two clusters.  If the ring size is 256, a Riak node that is not part of a cluster will start 256 vnodes as it considers itself to be the whole cluster.

When nodes join a cluster, the handoff process is two-ways; the joining node is handing off vnodes it will no longer run to the cluster, and the cluster will hand off vnodes it requires the joining node to run to that node.  In Riak 3.4 each vnode consists of two vnode modules - `riak_kv_vnode` and `riak_pipe_vnode` - and both modules must handoff for a vnode handoff to complete (although generally the `riak_pipe_vnode` is empty so this handoff is immediate).

For details of the cluster management commands:

```console
riak admin cluster --help
```

The process of joining, is a five stage process:

- [staging changes](/kv/3.4.1/how-to/operate/add-node/);
- [plan the change](/kv/3.4.1/how-to/operate/plan-and-commit-cluster-change/);
- [verify the plan](/kv/3.4.1/how-to/operate/plan-and-commit-cluster-change/);
- [commit the change](/kv/3.4.1/how-to/operate/plan-and-commit-cluster-change/);
- [await handoffs](/kv/3.4.1/how-to/operate/manage-handoffs/).

#### Join process - plan a change

The second stage is a `plan`.  In the plan stage, a claimant node, which will have been elected in the cluster, takes all the pending changes (in this case the joins) - and produces a plan of how vnodes should be arranged in the cluster following the transition.

As well as the pending changes, there are four inputs to that planning process:

- The `target_n_val`; which should be greater than or equal to the `n_val`.
  - If this is set to the `n_val` this will simply guarantee that all primary locations for an object will be on separate nodes.
  - If this is set to `n_val + N`, then even after `N` failures each the object will still be stored on separate nodes.
  - The `target_n_val` is the number of [primaries and fallbacks](/kv/3.4.1/explanation/foundations/clusters-rings-and-partitions/) which must be on distinct nodes.
- The `target_location_n_val`; which defaults to `target_n_val` minus one, but the supportable value will depend greatly on the number of locations and how evenly the nodes are spread across those locations.
  - The higher the `target_location_n_val`, and the `target_n_val` the more certain the availability of data in the cluster is.
  - For experimenting with checking the validity of larger settings, there is an offline [ring calculator](https://github.com/OpenRiak/ring_calculator) which may be used before planning a cluster expansion.
- The `ring_size`; how many vnodes need to be distributed, this must be set across the cluster at the start of the cluster, changing the ring size can only be managed by replicating to a new cluster.
- The cluster claim algorithm; which algorithm should be used to generate the plan.

There are three supported cluster claim algorithms in Riak: `choose_claim_v2`, `choose_claim_v3` and `choose_claim_v4`.  The algorithm to be is configured in `riak.conf`.

#### Join process - verify the plan

The response to the plan request will be an outline of the plan.  If the plan does not contain any staged `leave` requests it will be a single transition plan.

The plan may contain a warning e.g. if the `target_n_val` has not been achieved: `WARNING: Not all replicas will be on distinct nodes`

> Detecting and responding to the warning in a plan is an operator responsibility.  The only warning returned during the cluster change process of a bad configuration, is this warning at the planning stage.

To avoid an unsafe cluster, if a warning is returned, the plan **must** be cleared and another attempt made with different inputs:

- extra nodes,
- more locations,
- alternative targets,
- a different claim algorithm.

#### Join process - commit the plan

In the commit stage, the claimant node will re-plan the change, using the same inputs as the `plan` stage.  The `plan` is deterministic, and so the same outcome is achieved - in the case of `choose_claim_v3` by passing the same random seed to the random generator as used in the `plan`.  The `plan` is not a saved entity.

On issuing the `commit` of the plan, the transfers will be triggered once certain management timeouts have occurred.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
