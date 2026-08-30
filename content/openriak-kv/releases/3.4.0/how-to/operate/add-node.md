---
title: 'Add a node to a cluster'
description: 'Show operators how to add a node to a cluster with prechecks, verification, and recovery guidance.'
weight: 2
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#forming-and-expanding-a-riak-cluster'
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---staging-a-change'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to add a node to a cluster with prechecks, verification, and recovery guidance.

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

- [staging changes]({{< product-version-root >}}how-to/operate/add-node/);
- [plan the change]({{< product-version-root >}}how-to/operate/plan-and-commit-cluster-change/);
- [verify the plan]({{< product-version-root >}}how-to/operate/plan-and-commit-cluster-change/);
- [commit the change]({{< product-version-root >}}how-to/operate/plan-and-commit-cluster-change/);
- [await handoffs]({{< product-version-root >}}how-to/operate/manage-handoffs/).

#### Join process - staging a change

There must first be the staging of a `join`, an act that simply informs the cluster of the intention to make a change.  To perform the join the joining node must be started and be configured with the same `ring_size` as the existing cluster, and must have its location set (if a location-aware cluster is required).  The join command is issued on the joining node.

Only nodes configured with the same `ring_size` as the cluster, can be joined into the cluster.

If [locations are to be used]({{< product-version-root >}}reference/operations/cluster-claim-algorithms/) within the cluster, then location changes must also be staged:

```console
riak admin cluster location --help
```

There is no ability to learn a location (e.g. by detecting a placement group).  Allocating a node to a location, and tracking those mappings is a manual process.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
