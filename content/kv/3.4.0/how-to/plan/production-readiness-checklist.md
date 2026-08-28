---
title: 'Check production readiness'
description: 'Provide a verifiable checklist for approving an OpenRiak cluster before production traffic arrives.'
weight: 2
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\plan\Choosing-a-backend\best-practices.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\best-practices.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\future.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#choosing-infrastructure'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Provide a verifiable checklist for approving an OpenRiak cluster before production traffic arrives.

## Before you begin

Access to the affected OpenRiak KV environment, the exact product version, a record of the current state, and a safe rollback plan.

## Overview

### Scaling and Operating Riak Best Practices

[use ref handoff]: {{< baseurl >}}kv/3.4.0/reference/operations/handoff/
[config mapreduce]: {{< baseurl >}}kv/3.4.0/how-to/configure/mapreduce/
[glossary aae]: {{< baseurl >}}kv/3.4.0/explanation/foundations/glossary/#active-anti-entropy-aae
[cluster ops add remove node]: {{< baseurl >}}kv/3.4.0/tutorials/operations/change-cluster-membership/

OpenRiak KV is a database designed for easy operation and scaling. Below are some best practices that will enable you to improve performance and reliability at all stages in the life of your OpenRiak cluster.

#### Disk Capacity

Filling up disks is a serious problem in Riak. In general, you should
add capacity under the following conditions:

* a disk becomes more than 80% full
* you have fewer than 10 days of capacity remaining at current rates of
  growth

#### RAID Levels

Riak provides resilience through its built-in redundancy.

* RAID0 can be used to increase the performance at the expense of
  single-node reliability
* RAID5/6 can be used to increase the reliability over RAID0 but still
  offers higher performance than single disks
* You should choose a RAID level (or no RAID) that you’re comfortable
  with

#### Disk Leeway

* Adding new nodes instantly increases the total capacity of the
  cluster, but you should allow enough internal network capacity that
  [handing off][use ref handoff] existing data outpaces the arrival of new
  data.
* Once you’ve reached a scale at which the amount of new data arriving
  is a small fraction of the cluster's total capacity, you can add new
  nodes when you need them. You should be aware, however, that adding
  new nodes can actually _increase_ disk usage on existing nodes in the
  short term as data is rebalanced within the cluster.
* If you are certain that you are likely to run out of capacity, we
  recommend allowing a week or two of leeway so that you have plenty of
  time to add nodes and for [handoff][use ref handoff] to occur before the disks reach
  capacity
* For large volumes of storage it's usually prudent to add more capacity
  once a disk is 80% full

#### CPU Capacity Leeway

* In a steady state, your peak CPU utilization, ignoring other
  processes, should be less than 30%
* If you provide sufficient CPU capacity leeway, you’ll have spare
  capacity to handle other processes, such as backups, [handoff][use ref handoff], and [active anti-entropy][glossary aae]

#### Network Capacity Leeway

* Network traffic tends to be “bursty,” i.e. it tends to vary both quite
  a bit and quickly
* Your normal load, as averaged over a 10-minute period, should be no
  more than 20% of maximum capacity
* Riak generates 3-5 times the amount of intra-node traffic as inbound
  traffic, so you should allow for this in your network design

#### When to Add Nodes

You should add more nodes in the following scenarios:

* you have reached 80% of storage capacity
* you have less than 10 days of leeway before you expect the cluster to
  fill up
* the current node's IO/CPU activity is higher than average for extended
  period of time, especially for [MapReduce][config mapreduce]
  operations

An alternative to adding more nodes is to add more storage to existing
nodes. However, you should do this only if:

* you’re confident that there is plenty of spare network and CPU
  capacity, _and_
* you can upgrade storage _equally across all nodes_. If storage is
  added in an unbalanced fashion, Riak will continue storing data
  equally across nodes, and the node with the smallest available storage
  space is likely to fail first. Thus, if one node uses 1 TB but the
  rest use 1.5 TB, Riak will overload the 1 TB node first.

The recommendations above should be taken only as general guidelines
because the specifics of your cluster will matter a great deal when
making capacity decisions. The following considerations are worth
bearing in mind:

* If your disks are 90% full but only filling up 1% per month, this
  might be a perfectly "safe" scenario. In cases like this, the velocity
  of adding new data is more important than any raw total.
* The burstiness of your write load is also an important consideration.
  If writes tend to come in large batches that are unpredictably timed,
  it can be more difficult to estimate when disks will become full,
  which means that you should probably over-provision storage as a
  precaution.
* If Riak shares disks with other processes or is on the system root
  mount point, i.e. `/`, we recommend leaving a little extra disk space
  in addition to the estimates discussed above, as other system
  processes might use disk space unexpectedly.

#### How to Add Nodes

* You should add as many additional nodes as you require in one
  operation
* Don’t add nodes one at a time if you’re adding multiple nodes
* You can limit the transfer rate so that priority is given to live
  customer traffic

This process is explored in more detail in [Adding and Removing Nodes][cluster ops add remove node].

#### Scaling

* All large-scale systems are bound by the availability of some
  resources
* From a stability point of view, the best state for a busy OpenRiak cluster
  to maintain is the following:
  * New network connections are limited to ensure that existing network
    connections consume most network bandwidth
  * CPU at < 30%
  * Disk IO at < 90%
* You should use HAProxy or your application servers to limit new
  network connections to keep network and IO below 90% and CPU below
  30%.

### Planning for the Future

**TODO: Add content**

#### Choosing infrastructure

Choosing the infrastructure for a distributed database requires a different approach to choosing the infrastructure for a traditional, vertically-scaled solution.

> Riak is designed as a scale-out system across __inexpensive__ computers, where Riak smoothly handles the failure of individual nodes.  Riak will run for extended periods with nodes down, so operator action can be deferred - the aim is to be highly available with minimal operator intervention required at inconvenient hours.

The infrastructure selection decision is split into three parts:

- [Node selection, including storage]({{< baseurl >}}kv/3.4.0/how-to/plan/size-cluster/);
- [Network requirements]({{< baseurl >}}kv/3.4.0/reference/configuration/networking/);
- [The use of a proxy, WAF or load-balancing gateway]({{< baseurl >}}kv/3.4.0/how-to/configure/load-balancing-proxy/).

OpenRiak KV is designed for easy operation and scaling. The following document comtains some best practices that will help you to improve the performance, reliability and life-span of your OpenRiak Cluster.

## Verify the result

Confirm the requested outcome, inspect cluster health and logs, and test the relevant client or operational path.
