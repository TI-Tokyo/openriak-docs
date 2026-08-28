---
title: 'Size an OpenRiak cluster'
description: 'Show architects how to estimate capacity, node count, headroom, and growth for a production workload.'
weight: 3
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
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\plan\planning-your-cluster.md'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#choosing-infrastructure'
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#nodes'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show architects how to estimate capacity, node count, headroom, and growth for a production workload.

## Before you begin

Access to the affected OpenRiak KV environment, the exact product version, a record of the current state, and a safe rollback plan.

## Overview

### Choosing infrastructure

Choosing the infrastructure for a distributed database requires a different approach to choosing the infrastructure for a traditional, vertically-scaled solution.

> Riak is designed as a scale-out system across __inexpensive__ computers, where Riak smoothly handles the failure of individual nodes.  Riak will run for extended periods with nodes down, so operator action can be deferred - the aim is to be highly available with minimal operator intervention required at inconvenient hours.

The infrastructure selection decision is split into three parts:

- [Node selection, including storage]({{< baseurl >}}kv/3.4.0/how-to/plan/size-cluster/);
- [Network requirements]({{< baseurl >}}kv/3.4.0/reference/configuration/networking/);
- [The use of a proxy, WAF or load-balancing gateway]({{< baseurl >}}kv/3.4.0/how-to/configure/load-balancing-proxy/).

#### Nodes

A OpenRiak cluster is built up of multiple individual compute nodes.  Those nodes are expected to be distinct servers, or cloud instances; but Riak does include in-built support for handling nodes that have shared failure modes through location awareness.

> It is common for mission-critical production systems using Riak to NOT use component resilience that might be considered essential in a traditional scale-up database (e.g. RAID arrays); choose simplicity and speed of components, and expect the reliability to come from the OpenRiak cluster not the individual nodes.

When choosing server hardware or instance types, the following guidance should be considered with regards to component selection:

- There are production use cases of Riak with rigid zero-data-loss requirements that use ephemeral storage components due to the reliability and repair capability within an OpenRiak cluster, and between replicating clusters in diverse locations.
  - It is best to cost-optimise for speed and capacity with node storage, rather than for resilience.
- All the memory of the system will be used to improve performance, as any memory not used by Riak should be consumed by the file-system page cache.  The page cache will increase throughput potential by reducing the latency of disk reads, and also by keeping disk activity below IO constraints.
  - Over-provisioning memory is generally of value.
- The Erlang/OTP platform used by Riak, and the design of Riak itself, is optimised to make use of multi-core architectures; more CPU cores should generally be preferred to faster CPU cores.
  - There are production deployments of Riak on both ARM and Intel-based CPUs.
  - The Erlang VM which has JIT optimisations for both architectures.
  - Extremely high core counts per node (e.g. > 40) may require specific Erlang VM tuning to fully realise the benefits of additional capacity.

> Riak clusters tested to perform predictably at certain throughput constraints - e.g. max CPU utilisation, bandwidth or disk contention.  Running Riak close to these limits for extended periods should **not** lead to volatile outcomes.

Riak nodes may fail suddenly if space constraints are breached - i.e. available disk space, memory and at open file limits (very large clusters may require ulimit settings of 1M or more).  There is no management of activity to prevent breaches when close to these limits.

> It is critical to monitor against space limits and have additional nodes available, and scale out the cluster by adding nodes should breaching space limits become a threat.  As load is distributed evenly across nodes, space constraints may be hit concurrently on multiple nodes.

Riak spreads load evenly through the cluster, data is sharded across individual vnodes by consistent hashing, and vnodes are allocated to nodes so that each node will have either X or X + 1 vnodes.  All nodes should therefore have, wherever possible, equal capacity:

- Riak has internal mitigation to the problem of individual nodes that are temporarily running slower than other nodes in the cluster; the job of fetching data blocks is balanced so that the work is generally performed on the fastest nodes (i.e those with available resources).  Also client responses to GET requests are returned at the speed of a quorum of nodes, without waiting for the slowest response.  However, unlike GET requests, query requests will be slowed to the pace of the slowest node.
- Where individual nodes are undergoing long-running system tasks that may cause local slowness (e.g. RAID rebuild activity), it may be better for the nodes to be stopped (and therefore out of the active cluster), rather than acting as a slow node within the cluster.

The design of Riak handles failure of individual nodes, however if the design of the underlying infrastructure can cause multiple nodes to fail concurrently (e.g. in a cloud environment where multiple nodes may be provisioned on the same underlying hardware), then resilience should be provided by running multiple clusters or by identifying in the OpenRiak cluster groups of nodes with shared failure modes as "locations".  A location may be aligned in cloud environments with placement-groups or availability zones, with racks that have common network components in physical environments, or with maintenance groups where efficient operations require multiple-nodes to be updated concurrently.

- The OpenRiak cluster claim algorithm will allocate data so replicas are split across locations, so that sufficient copies of the data are always available.

Performance testing of high-intensity database operations on the leveled backend, has demonstrated situations where virtualised cloud instances have performed up to 2.7 times worse than equivalent physical hardware:

- Where possible abstraction between Riak, the Operating System and the underlying hardware should be avoided.
- It is recommended to automate operational activity on Riak nodes through scripting tools (e.g. Ansible) rather than abstraction layers (e.g. Docker).

Riak is designed to be deployed as a single package where, other than monitoring and security software, Riak is the only package present on the node; and does not share the node with volatile demands for compute resources.

- Scheduling of operational actions within an OpenRiak cluster should avoid concurrent running of resource-intensive activity e.g. array integrity checks in software RAID systems, solid-state disk trim jobs, or operational security software sweeps.
- Operating system configuration options that optimise for performance are not recommended where they present a risk of unpredictable performance during relatively rare events - such as for garbage collection or realignment.
  - It is recommended that `transparent_huge_pages` be disabled due to the risk of latency spikes.

File-system performance is important to Riak performance;

- Generally the use of an XFS file system is recommended, and thorough testing is recommended should alternatives be preferred.
- Avoid file-system scheduler settings that re-order activity;
  - normally a `noop`/`none` scheduler is preferred, but this advice may be superseded by OS or hardware-specific guidance.
- Within cloud environments the use of local disks will normally provide better return on investment than scaling-up throughput on shared storage services.

> Some cloud providers offer special instance types designed for scale-out databases (e.g. AWS im4gn family), and generally such instances should be preferred over general purpose instances.

[operating-system]: : ../../setup/install/index
[choosing-a-backend]: : ../../setup/install/plan/choosing-a-backend

## Verify the result

Confirm the requested outcome, inspect cluster health and logs, and test the relevant client or operational path.
