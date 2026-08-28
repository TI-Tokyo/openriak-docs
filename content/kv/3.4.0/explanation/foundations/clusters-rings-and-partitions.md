---
title: 'Clusters, rings, and partitions'
description: 'Explain clusters, rings, and partitions and why it matters when designing or operating OpenRiak systems.'
weight: 4
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
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\clusters.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\architecture.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#ring-size'
  - 'https://openriak.github.io/riak/RiakTheoryGuide.html#the-ring---the-distribution-of-vnodes'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain clusters, rings, and partitions and why it matters when designing or operating OpenRiak systems.

## Overview

### Clusters

[concept buckets]: /kv/3.4.0/explanation/data-model/keys-objects-and-buckets/
[concept keys objects]: /kv/3.4.0/explanation/data-model/keys-objects-and-buckets/
[concept replication]: /kv/3.4.0/explanation/replication/
[glossary node]: /kv/3.4.0/explanation/foundations/glossary/#node
[glossary vnode]: /kv/3.4.0/explanation/foundations/glossary/#vnode
[learn dynamo]: /kv/3.4.0/explanation/foundations/dynamo-model/
[usage bucket types]: /kv/3.4.0/how-to/develop/use-bucket-types/
[usage conflict resolution]: /kv/3.4.0/how-to/develop/resolve-conflicts/
[usage replication]: /kv/3.4.0/explanation/replication/

OpenRiak's default mode of operation is to work as a cluster consisting of
multiple [nodes][glossary node], i.e. multiple well-connected data
hosts.

Each host in the cluster runs a single instance of Riak, referred to as
an OpenRiak node. Each OpenRiak node manages a set of virtual nodes, or
[vnodes][glossary vnode], that are responsible for storing a
separate portion of the keys stored in the cluster.

In contrast to some high-availability systems, Riak nodes are _not_
clones of one another, and they do not all participate in fulfilling
every request. Instead, you can configure, at runtime or at request
time, the number of nodes on which data is to be replicated, as well as
when [replication][concept replication] occurs and which [merge strategy][usage conflict resolution] and failure model are to be followed.

#### The Ring

Though much of this section is discussed in our annotated discussion of
the Amazon [Dynamo paper][learn dynamo], it nonetheless provides a summary of
how Riak implements the distribution of data throughout a cluster.

Any client interface to Riak interacts with objects in terms of the
[bucket][concept buckets] and [key][concept keys objects] in which a value is
stored, as well as the [bucket type][usage bucket types] that is used
to set the bucket's properties.

Internally, Riak computes a 160-bit binary hash of each bucket/key pair
and maps this value to a position on an ordered **ring** of all such
values. This ring is divided into partitions, with each Riak vnode
responsible for one of these partitions (we say that each vnode
_claims_ that partition).

Below is a visual representation of a Riak ring:

![A Riak Ring](/images/riak-ring.png)

The nodes of an OpenRiak cluster each attempt to run a roughly equal number
of vnodes at any given time. In the general case, this means that each
node in the cluster is responsible for 1/(number of nodes) of the ring,
or (number of partitions)/(number of nodes) vnodes.

If two nodes define a 16-partition cluster, for example, then each node
will run 8 vnodes. Nodes attempt to claim their partitions at intervals
around the ring such that there is an even distribution amongst the
member nodes and that no node is responsible for more than one replica
of a key.

#### Intelligent Replication

When an object is being stored in the cluster, any node may participate
as the **coordinating node** for the request. The coordinating node
consults the ring state to determine which vnode owns the partition in
which the value's key belongs, then sends the write request to that
vnode as well as to the vnodes responsible for the next N-1 partitions
in the ring (where N is a [configurable parameter][usage replication] that describes how many copies of the value to store). The
write request may also specify that at least W (=< N) of those vnodes
reply with success, and that DW (=< W) reply with success only after
durably storing the value.

A read, or GET, request operates similarly, sending requests to the
vnode  that "claims" the partition in which the key resides, as well as
to the next N-1 partitions. The request also specifies R (=< N), the
number of vnodes that must reply before a response is returned.

Here is an illustration of this process:

![A Riak Ring](/images/riak-data-distribution.png)

When N is set to 3, the value `REM` is stored in the key `artist`. That
key is assigned to 3 partitions out of 32 available partitions. When a
read request is made to Riak, the ring state will be used to determine
which partitions are responsible. From there, a variety of
[configurable parameters][usage replication] determine how Riak
will behave in case the value is not immediately found.

#### Gossiping

The ring state is shared around the cluster by means of a "gossip
protocol." Whenever a node changes its claim on the ring, it announces,
i.e. "gossips," this change to other nodes so that the other nodes can
respond appropriately. Nodes also periodically re-announce what they
know about ring in case any nodes happened to miss previous updates.

### Architecture Reference

<!-- TODO: Content -->

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
