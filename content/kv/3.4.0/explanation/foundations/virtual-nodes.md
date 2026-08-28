---
title: 'Virtual nodes'
description: 'Explain virtual nodes and why it matters when designing or operating OpenRiak systems.'
weight: 8
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
  - 'developers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\vnodes.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/RiakTheoryGuide.html#the-ring---the-distribution-of-vnodes'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain virtual nodes and why it matters when designing or operating OpenRiak systems.

## Overview

### Vnodes

[concept causal context]: {{< baseurl >}}kv/3.4.0/explanation/data-model/causal-context/
[concept clusters ring]: {{< baseurl >}}kv/3.4.0/explanation/foundations/clusters-rings-and-partitions/#the-ring
[concept replication]: {{< baseurl >}}kv/3.4.0/explanation/replication/
[concept strong consistency]: {{< baseurl >}}kv/3.4.0/explanation/consistency/strong-consistency/
[glossary node]: {{< baseurl >}}kv/3.4.0/explanation/foundations/glossary/#node
[glossary ring]: {{< baseurl >}}kv/3.4.0/explanation/foundations/glossary/#ring
[plan backend]: {{< baseurl >}}kv/3.4.0/explanation/storage/choosing-backend/
[plan cluster capacity]: {{< baseurl >}}kv/3.4.0/explanation/storage/capacity-planning/
[use admin riak cli]: {{< baseurl >}}kv/3.4.0/reference/commands/riak/

Virtual nodes, more commonly referred to as **vnodes**, are processes
that manage partitions in the Riak [ring][glossary ring]. Each data
partition in an OpenRiak cluster has a vnode that **claims** that partition.
Vnodes perform a wide variety of operations, from K/V storage operations
to guaranteeing [strong consistency][concept strong consistency] if you choose to use that
feature.

#### The Number of Vnodes in a Cluster

The term [node][glossary node] refers to a full instance of Riak,
be it on its own physical machine or alongside others on a single
machine, as in a development cluster on your laptop. Each OpenRiak node
contains multiple vnodes. The number per node is the [ring
size][concept clusters ring] divided by the number of nodes in the cluster.

This means that in some clusters different nodes will have different
numbers of data partitions (and hence a different number of vnodes),
because (ring size / number of nodes) will not produce an even integer.
If the ring size of your cluster is 64 and you are running three nodes,
two of your nodes will have 21 vnodes, while the third node holds 22
vnodes.

The output of the [`riak admin member-status`][use admin riak cli]
command shows this:

```
================================= Membership ==================================
Status     Ring    Pending    Node
-------------------------------------------------------------------------------
valid      34.4%      --      'dev1@127.0.0.1'
valid      32.8%      --      'dev2@127.0.0.1'
valid      32.8%      --      'dev3@127.0.0.1'
-------------------------------------------------------------------------------
Valid: 3 / Leaving:0 / Exiting:0 / Joining:0 / Down:0
```

In this cluster, one node accounts for 34.4% of the ring, i.e. 22 out of
64 partitions, while the other two nodes account for 32.8%, i.e. 21 out
of 64 partitions. This is normal and expected behavior in Riak.

We strongly recommend setting the appropriate ring size, and by
extension the number of vnodes, prior to building a cluster. A full
guide can be found in our [cluster planning][plan cluster capacity] documentation.

#### The Role of Vnodes

Vnodes essentially watch over a designated subset of a cluster's key
space. Riak computes a 160-bit binary hash of each bucket/key pair and
maps this value to a position on an ordered [ring][concept clusters ring]
of all such values. The illustration below provides a visual
representation of the Riak ring:

![The Riak
Ring]({{< baseurl >}}images/shared/riak-ring.png)

You can think of vnodes as managers, responsible for handling incoming
requests from other nodes/vnodes, storing objects in the appropriate
storage backend, fetching objects from backends, interpreting [causal
context][concept causal context] metadata for objects, acting as [strong consistency
ensembles][concept strong consistency] and much
more.  At the system level, vnodes are Erlang processes build on top of
the [`gen_fsm`](http://www.erlang.org/doc/design_principles/fsm.html)
abstraction in Erlang, i.e. you can think of vnodes as **finite state
machines** that are constantly at work ensuring that OpenRiak's key
goals---high availability, fault tolerance, etc.---are guaranteed for
their allotted portion of the cluster's key space. Whereas nodes are
essentially a passive container for a wide variety of Riak processes,
vnodes are the true workhorses of Riak.

While each vnode has a main Erlang process undergirding it, vnodes may
also spawn new worker processes (i.e. new Erlang actors) to perform
asynchronous tasks on behalf of the vnode.

If you're navigating through the file system of an OpenRiak node, you'll
notice that each node's `/data` directory holds a variety of
subdirectories. If you're using, say, [Bitcask]({{< baseurl >}}kv/3.4.0/explanation/storage/bitcask/) as a backend, navigate
into the `/bitcask` directory (you'll also see a `/ring` directory and
several others). If you open up the `/bitcask` directory, you'll see a
wide assortment of directories with numbers as names, e.g. `0` or
`1004782375664995756265033323.0.1144576013453623296`. These directories
each house the data from a particular partition.

#### Vnodes and Replication Properties

In our documentation on [replication properties][concept replication], we make frequent
mention of users' ability to choose how many nodes store copies of
data, how many nodes must respond for a read request to succeed, and so
on. This is slightly misleading, as the fundamental units of replication
are not nodes but rather vnodes.

This can be illustrated by way of a potential user error.  If you store
an object and set N=5, this means that you want the object to be stored
on 5 different nodes. But imagine that your cluster only has 3 nodes.
Setting N=5 on a 3-node cluster is actually just fine. The data will be
managed by 5 vnodes, but some of that data may end up being stored more
than once on different nodes. A likely scenario is that two nodes will
store two copies of the data a piece, while the third node will store
only one. Absent such an error, however, nodes will not contain multiple
vnodes responsible for the same partition.

#### Vnode Status

You can check the current status of all vnodes in your cluster using the
[`riak admin vnode-status`][use admin riak cli]
command. When you run that command, you will see a series of reports on
each of the vnodes active on the local node. The output of this command
consists of a series of reports on each active vnode. The report for a
specific vnode should look something like this:

```
VNode: 1278813932664540053428224228626747642198940975104
Backend: riak_kv_bitcask_backend
Status:
[{key_count, 275},
 {status,[{"./data/bitcask/1278813932664540053428224228626747642198940975104/2.bitcask.data",
           0,0,335}]}]
Status:
{vnodeid,<<"ÅR±\vi80\f">>}
```

The meaning of each field is given in the table below.

Field | Description
:-----|:-----------
`VNode` | The ID of the vnode in question
`Backend` | The storage [backend][plan backend] utilized by the vnode
`Status` | The number of keys managed by the vnode and the file where the vnode stores its data. The other information can be ignored.

#### The Ring - The distribution of vnodes

Riak is a set of smaller databases which are distributed across physical nodes.  The smaller databases are termed vnodes, and the vnode is a set of functions that are controlling a database backend - where the backend (either leveled or bitcask) does the work to modify and fetch serialised data from disk.

The number of vnodes is the ring size, which must be a factor of 2.  It is desirable for the ring size to be much greater than the number of nodes (i.e. actual devices).  The ring size must be a factor of 2, because each key will be hashed to a given position in the ring, by taking a sha hash of the Bucket and Key, and using an equivalent function to: `Hash band (RingSize - 1)`.  This will give each key a position between `0` and `RingSize - 1`, i.e. zero-indexed position in the vnodes.

As the object should be stored in multiple places, normally 3 (which is the `n_val`).  An object is then mapped to the Position, and the `(Position + 1) mod RingSize` and `(Position + 2) mod RingSize`.  This position triple is called the preflist, or the set of primary vnodes for the key.

When a cluster is formed, a claim algorithm will distribute vnodes `0` to `RingSize - 1` around the physical nodes, so that all of these preflists fall onto 3 separate nodes, but also ensures that for every such position `(Position + 3) mod RingSize` is also on a diverse physical node to the preflist for that position.

To restore full data protection after failure, Riak must request the next node along in each preflist to start a fallback vnode.  For example, if a node holding vnode 10 fails, then this has an impact on the keys that have mapped to vnodes 8, 9 and 10 - they all now have a missing vnode.  three fallback vnodes will now be started:

- A key which hashes to vnode 8 will be stored in vnodes 8, 9 and a fallback for vnode 10 that has been started on the node which owns vnode 11.
- A key which hashes to vnode 9 will be stored in vnodes 9, 11, and a fallback for vnode 10 that has been started on the node which owns vnode 12.
- A key which hashes to vnode 10 will be stored in vnodes 11, 12 and a fallback for vnode 10 that has been started on the node which owns vnode 13.

If the distribution in claim is correct, the full divergence of `n_val` resilience is maintained even when a single node fails.  Having full resilience for greater numbers of failures is configurable (assuming there exists sufficient nodes).

Each primary vnode will store the data from three preflists, and only the data for those preflists - a vnode is never both primary and fallback.  The keys that map to itself (M), and the keys that map to `(M - 1) mod RingSize` and `(M - 2) mod RingSize` are those preflists.  Fallback vnodes will contain keys for just one preflist - so every primary failure requires the starting of three fallbacks.

In reality, the ring appears to be more confusing than it is, as it does not use simple integers `0`, `1`, `2`, `3` etc to represent the positions in the ring.  It actually uses the position from taking the hash bits from the high end of the hash not the low end i.e. for a ring size of 256 `Hash band (255 bsl 152)` is used rather than `Hash band 255`.  This causes all the vnodes to be instead named `0`, `1 bsl 152` (i.e. `5708990770823839524233143877797980545530986496`), `2 bsl 152` (i.e. `11417981541647679048466287755595961091061972992`)... etc, but the principle is still unchanged as if they were more simply `0`, `1`, `2`, `3` etc.
