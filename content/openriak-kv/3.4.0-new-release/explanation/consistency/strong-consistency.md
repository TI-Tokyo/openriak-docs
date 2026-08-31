---
title: 'Strong consistency'
description: 'Explain strong consistency guarantees, limitations, costs, and suitable workloads.'
weight: 4
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'developers'
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\strong-consistency.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\strong-consistency.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#strong-consistency-api'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain strong consistency guarantees, limitations, costs, and suitable workloads.

## Overview

### Strong Consistency

[usage bucket types]: {{< product-version-root >}}how-to/develop/use-bucket-types/
[concept eventual consistency]: {{< product-version-root >}}explanation/consistency/eventual-consistency/

**Please Note:**
OpenRiak KV's strong consistency is an experimental feature and may be removed
from the product in the future. Strong consistency is not commercially
supported or production-ready. Strong consistency is incompatible with
Multi-Datacenter Replication, Bitcask Expiration, LevelDB
Secondary Indexes, Riak Data Types and Commit Hooks. We do not recommend its
usage in any production environment.

Riak was originally designed as an [eventually consistent]({{< product-version-root >}}explanation/consistency/eventual-consistency/) system, fundamentally geared toward providing partition
(i.e. fault) tolerance and high read and write availability.

While this focus on high availability is a great fit for many data
storage needs, there are also many use cases for which strong data
consistency is more important than availability. Basho introduced a new
strong consistency option in version 2.0 to address these use cases.
In Riak, strong consistency is applied [using bucket types][usage bucket types], which
enables developers to apply strong consistency guarantees on a per-key
basis.

Elsewhere in the documentation there are instructions for [enabling and using]({{< product-version-root >}}reference/specialized-apis/strong-consistency-api/) strong consistency, as well as a [guide for operators]({{< product-version-root >}}how-to/configure/strong-consistency/) looking to manage,
configure, and monitor strong consistency.

#### Strong vs. Eventual Consistency

If you successfully write a value to a key in a strongly consistent
system, the next successful read of that key is guaranteed to show that
write. A client will never see out-of-date values. The drawback is that
some operations may fail if an insufficient number of object replicas
are available. More on this in the section on [trade-offs]({{< product-version-root >}}explanation/consistency/strong-consistency/).

In an eventually consistent system, on the other hand, a read may return
an out-of-date value, particularly during system or network failures.
The advantage of this approach is that reads and writes can succeed even
when a cluster is experiencing significant service degradation.

##### Example

Building on the example presented in the [eventual consistency][concept eventual consistency] doc,
imagine that information about who manages Manchester United is stored
in Riak, in the key `manchester-manager`. In the eventual consistency
example, the value associated with this key was originally
`David Moyes`, meaning that that was the first successful write to that
key. But then `Louis van Gaal` became Man U's manager, and a write was
executed to change the value of `manchester-manager`.

Now imagine that this write failed on one node in a multi-node cluster.
Thus, all nodes report that the value of `manchester-manager` is `Louis
van Gaal` except for one. On the errant node, the value of the
`manchester-manager` key is still `David Moyes`. An eventually
consistent system is one in which a get request will most likely return
`Louis van Gaal` but could return the outdated value `David Moyes`.

In a strongly consistent system, conversely, any successful read on
`manchester-manager` will return `Louis van Gaal` and never `David Moyes`.
Reads will return `Louis van Gaal` every single time until Man U gets a new
manager and someone performs a successful write to `manchester-manager`
to change its value.

It might also be useful to imagine it a bit more abstractly. The
following causal sequence would characterize a strongly consistent
system:

1. The value of the key `k` is set to `v`
2. All successful reads on `k` return `v`
3. The value of `k` is changed to `v2`
4. All successful reads on `k` return `v2`
5. And so forth

At no point in time does this system return an out-of-date value.

The following sequence could characterize an eventually consistent
system:

1. A write is made that sets the value of the key `k` to `v`
2. Nearly all reads to `k` return `v`, but a small percentage return
   `not found`
3. A write to `k` changes the value to `v2`
4. Nearly all reads to `k` now return `v2`, but a small number return
   the outdated `v` (or even `not found`) because the newer value hasn't
   yet been replicated to all nodes

### Monitoring Strong Consistency

#### Monitoring Strong Consistency

Riak provides a wide variety of data related to the current operating
status of a node. This data is available by running the [`riak admin status`]({{< product-version-root >}}reference/commands/riak-admin/#status) command. That data now
includes statistics specific to strongly consistent operations.

A full listing of these stats is available in [Inspecting a Node]({{< product-version-root >}}how-to/operate/inspect-node-and-cluster/).
All strong consistency-related stats are prefixed with `consistent_`,
e.g. `consistent_gets`, `consistent_puts`, etc. Many of these stats are
so-called "one-minute stats," meaning that they reflect node activity in
the last minute.

Strong consistency stats fall into two categories: GET-related and
PUT-related stats.

##### GET-related stats

Stat | Description
:----|:-----------
`consistent_gets` | Number of strongly consistent GETs coordinated by this node in the last minute
`consistent_gets_total` | Total number of strongly consistent GETs coordinated by this node
`consistent_get_objsize_mean` | Mean object size for strongly consistent GETs on this node in the last minute
`consistent_get_objsize_median` | Median object size for strongly consistent GETs on this node in the last minute
`consistent_get_objsize_95` | 95th-percentile object size for strongly consistent GETs on this node in the last minute
`consistent_get_objsize_99` | 99th-percentile object size for strongly consistent GETs on this node in the last minute
`consistent_get_objsize_100` | 100th-percentile object size for strongly consistent GETs on this node in the last minute
`consistent_get_time_mean` | Mean time between reception of client GETs to strongly consistent keys and subsequent response
`consistent_get_time_median` | Median time between reception of client GETs to strongly consistent keys and subsequent response
`consistent_get_time_95` | 95th-percentile time between reception of client GETs to strongly consistent keys and subsequent response
`consistent_get_time_99` | 99th-percentile time between reception of client GETs to strongly consistent keys and subsequent response
`consistent_get_time_100` | 100th-percentile time between reception of client GETs to strongly consistent keys and subsequent response

##### PUT-related stats

Stat | Description
:----|:-----------
`consistent_puts` | Number of strongly consistent PUTs coordinated by this node in the last minute
`consistent_puts_total` | Total number of strongly consistent PUTs coordinated by this node
`consistent_put_objsize_mean` | Mean object size for strongly consistent PUTs on this node in the last minute
`consistent_put_objsize_median` | Median object size for strongly consistent PUTs on this node in the last minute
`consistent_put_objsize_95` | 95th-percentile object size for strongly consistent PUTs on this node in the last minute
`consistent_put_objsize_99` | 99th-percentile object size for strongly consistent PUTs on this node in the last minute
`consistent_put_objsize_100` | 100th-percentile object size for strongly consistent PUTs on this node in the last minute
`consistent_put_time_mean` | Mean time between reception of client PUTs to strongly consistent keys and subsequent response
`consistent_put_time_median` | Median time between reception of client PUTs to strongly consistent keys and subsequent response
`consistent_put_time_95` | 95th-percentile time between reception of client PUTs to strongly consistent keys and subsequent response
`consistent_put_time_99` | 99th-percentile time between reception of client PUTs to strongly consistent keys and subsequent response
`consistent_put_time_100` | 100th-percentile time between reception of client PUTs to strongly consistent keys and subsequent response

#### Strong Consistency API

The use of the strong consistency API is deprecated in Riak 3.4, and the API will be retired in Riak 4.0.

From Riak 4.0, Riak will only have support for eventual consistency, but protection for conflicts can be improved through [conditional PUTs with token-based consensus]({{< product-version-root >}}reference/http-api/conditional-requests/).

The functionality of Strong Consistency is unchanged since Riak 2.2.3, so refer to the [legacy documentation]({{<baseurl>}}openriak-kv/2.2.3/developing/app-guide/strong-consistency/index.html) for further information.
