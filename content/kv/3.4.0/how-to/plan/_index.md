---
title: 'Plan a production cluster'
description: 'Introduce planning procedures that turn workload and infrastructure requirements into deployment decisions.'
weight: 1
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
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\plan\index.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\start.md'
source_material:
  - 'legacy-3.2.5'
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
quickdocs_sources:
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#riak-kv---building-and-scaling-a-cluster'
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#riak-kv---initial-design-decisions'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce planning procedures that turn workload and infrastructure requirements into deployment decisions.

## Before you begin

Access to the affected OpenRiak KV environment, the exact product version, a record of the current state, and a safe rollback plan.

### Planning Overview

[plan start]: ./start
[plan backend]: ./backend
[plan cluster capacity]: ./cluster-capacity
[plan bitcask capacity]: ./bitcask-capacity-calc
[plan backend bitcask]: ./backend/bitcask
[plan best practices]: ./best-practices
[plan future]: ./future

#### In This Section

##### [Start Planning][plan start]

Steps and recommendations for designing and configuring an OpenRiak KV cluster.

[Learn More >>][plan start]

##### [Choosing a Backend][plan backend]

Information on choosing the right storage backend for your OpenRiak KV cluster.

[Learn More >>][plan backend]

##### [Cluster Capacity Planning][plan cluster capacity]

Outlines variables (such as memory requirements) to keep in mind when planning your OpenRiak KV cluster.

[Learn More >>][plan cluster capacity]

##### [Bitcask Capacity Calculator][plan bitcask capacity]

A calculator that will assist you in sizing your cluster if you plan to use the default ([Bitcask][plan backend bitcask]) storage back end.

[Learn More >>][plan bitcask capacity]

##### [Scaling & Operating Best Practices][plan best practices]

A set of best practices that will enable you to improve performance and reliability at all stages in the life of your OpenRiak KV cluster.

[Learn More >>][plan best practices]

### Start Planning

[plan backend]: /kv/3.4.0/explanation/storage/choosing-backend/
[plan cluster capacity]: /kv/3.4.0/explanation/storage/capacity-planning/
[plan backend bitcask]: /kv/3.4.0/explanation/storage/bitcask/
[plan bitcask capacity]: /kv/3.4.0/explanation/storage/capacity-planning/

Here are some steps and recommendations designing and configuring your
OpenRiak cluster.

#### Backend

Backends are what OpenRiak KV uses to persist data. Different backends have
strengths and weaknesses, so if you are unsure of which backend you
need, read through the [Choosing a Backend][plan backend] tutorial.

#### Capacity

[Cluster Capacity Planning][plan cluster capacity] outlines the various elements and variables that should be considered when planning your OpenRiak cluster.

If you have chosen [Bitcask][plan backend bitcask] as your backend, you will also want to run through [Bitcask Capacity Planning][plan bitcask capacity] to help you calculate a reasonable capacity.

#### Network Configuration / Load Balancing

There are at least two acceptable strategies for load-balancing requests
across your OpenRiak cluster: **virtual IPs** and **reverse-proxy**.

For **virtual IPs**, we recommend using any of the various VIP
implementations. We don't recommend VRRP behavior for the VIP because
you'll lose the benefit of spreading client query load to all nodes in a
ring.

For **reverse-proxy** configurations (HTTP interface), any one of the
following should work adequately:

* haproxy
* squid
* varnish
* nginx
* lighttpd
* Apache

#### OpenRiak KV - Building and Scaling a Cluster

This guide is split into two parts:

- [The considerations to make when choosing infrastructure for Riak](/kv/3.4.0/how-to/plan/size-cluster/)
- [The practical steps to actually make and expand a cluster](/kv/3.4.0/how-to/operate/add-node/)

#### OpenRiak KV - Initial Design Decisions

There are six initial design decisions that need to be considered at the outset of an OpenRiak KV  project.  The priority design choices are:

- [Database backend](/kv/3.4.0/how-to/plan/choose-storage-backend/)
- [Ring size](/kv/3.4.0/how-to/plan/choose-ring-size/)
- [Intra-cluster data resilience](/kv/3.4.0/how-to/plan/choose-intra-cluster-resilience/)
- [Interconnecting multiple clusters](/kv/3.4.0/how-to/plan/choose-multi-cluster-topology/)
- [Deleting data](/kv/3.4.0/how-to/plan/choose-deletion-policy/)
- [Mapping data to objects](/kv/3.4.0/how-to/plan/map-data-to-objects/)

It is not always possible to get all decisions correct first-time in the design phase.  Within this page, as well as supporting information for making the choice, there is also guidance and how to transition to an alternative configuration.

> Riak clusters commonly run for decades, dealing with significant functional and non-functional changes in applications during their lifespan.  Making good decisions up-front is helpful, but not critical.

## Planning your OpenRiak KV cluster

## Verify the result

Confirm the requested outcome, inspect cluster health and logs, and test the relevant client or operational path.
