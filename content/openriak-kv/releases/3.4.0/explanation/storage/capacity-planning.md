---
title: 'Storage capacity planning'
description: 'Explain storage capacity planning, its constraints, and the workloads for which it is appropriate.'
weight: 3
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\bitcask-capacity-calc.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\cluster-capacity.md'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain storage capacity planning, its constraints, and the workloads for which it is appropriate.

## Overview

### Bitcask Capacity Calculator

[plan backend bitcask]: {{< product-version-root >}}explanation/storage/bitcask/

These calculators will assist you in sizing your cluster if you plan to
use the default [Bitcask][plan backend bitcask] storage back end.

This page is designed to give you a rough estimate when sizing your
cluster.  The calculations are a _best guess_, and they tend to be a bit
on the conservative side. It's important to include a bit of head room
as well as room for unexpected growth so that if demand exceeds
expectations you'll be able to add more nodes to the cluster and stay
ahead of your requirements.

<div id="node_info" class="calc_info"></div>
<div class="calculator">
   <ul>
     <li>
       <label for="n_total_keys">Total Number of Keys:</label>
       <input id="n_total_keys"  type="text" size="12" name="n_total_keys" value="" class="calc_input" />
       <span class="error_span" id="n_total_keys_error"></span>
     </li>
     <li>
       <label for="n_bucket_size">Average Bucket Size (Bytes):</label>
       <input id="n_bucket_size"type="text" size="7" name="n_bucket_size" value="" class="calc_input" />
       <span class="error_span"id="n_bucket_size_error"></span>
     </li>
     <li>
       <label for="n_key_size">Average Key Size (Bytes):</label>
       <input type="text" size="2" name="n_key_size" id="n_key_size" value="" class="calc_input" />
       <span class="error_span" id="n_key_size_error"></span>
     </li>
     <li>
       <label for="n_record_size">Average Value Size (Bytes):</label>
       <input id="n_record_size"type="text" size="7" name="n_record_size" value="" class="calc_input" />
       <span class="error_span"id="n_record_size_error"></span>
     </li>
     <li>
       <label for="n_ram">RAM Per Node (in GB):</label>
       <input type="text" size="4" name="n_ram" id="n_ram" value="" class="calc_input" />
       <span class="error_span" id="n_ram_error"></span>
     </li>
     <li>
       <label for="n_nval"><i>N</i> (Number of Write Copies):</label>
       <input type="text" size="2" name="n_nval" id="n_nval" value="" class="calc_input" />
       <span class="error_span" id="n_nval_error"></span>
     </li>
</ul>
</div>

#### Recommendations

<span id="recommend"></span>

#### Details on Bitcask RAM Calculation

With the above information in mind, the following variables will factor
into your RAM calculation:

Variable | Description
:--------|:-----------
Static Bitcask per-key overhead | 44.5 bytes per key
Estimated average bucket-plus-key length | The combined number of characters your bucket + keynames will require (on average). We'll assume 1 byte per character.
Estimated total objects | The total number of key/value pairs your cluster will have when started
Replication Value (`n_val`) | The number of times each key will be replicated when written to Riak (the default is 3)

#### The actual equation

Approximate RAM Needed for Bitcask = (static bitcask per key overhead +
estimated average bucket+key length in bytes) * estimate total number of
keys * `n_val`

Example:

* 50,000,000 keys in your cluster to start
* approximately 30 bytes for each bucket+key name
* default `n_val` of 3

The amount of RAM you would need for Bitcask is about **9.78 GBs across
your entire cluster.**

Additionally, Bitcask relies on your operating system's filesystem cache
to deliver high performance reads. So when sizing your cluster, take
this into account and plan on having several more gigabytes of RAM
available for your filesystem cache.

### Cluster Capacity Planning

[plan backend leveldb]: {{< product-version-root >}}explanation/storage/leveldb/
[plan bitcask capacity]: {{< product-version-root >}}explanation/storage/capacity-planning/
[plan index]: {{< product-version-root >}}how-to/plan/
[concept replication]: {{< product-version-root >}}explanation/replication/
[use admin riak admin#cluster]: {{< product-version-root >}}reference/commands/riak-admin/#cluster
[config reference]: {{< product-version-root >}}reference/configuration/
[perf benchmark]: {{< product-version-root >}}how-to/tune/benchmark-cluster/
[LVM]: http://en.wikipedia.org/wiki/Logical_Volume_Manager_(Linux)

This document outlines the various elements and variables to keep in mind when planning your OpenRiak cluster. Your use case and environment variables will be specific to what you're building, but this document should set you on the right path when planning and launching an OpenRiak cluster.

#### RAM

[RAM](http://en.wikipedia.org/wiki/Random-access_memory) is the most important resource when sizing your OpenRiak cluster. Memory keeps data closer to your users. Memory is essential for running complex MapReduce queries or caching data to provide low-latency request times.

##### Bitcask and Memory Requirements

Your choice of local storage backend for Riak impacts your RAM
needs. Though Riak has pluggable backend storage, Bitcask is the
default.  Why? Because it's built for:

* low-latency request times
* high throughput
* the ability to handle data sets much larger than RAM w/o degradation

Bitcask's one major requirement, however, is that it must keep the
entire **keydir** in memory. The keydir is a hash table that maps each
concatenated bucket + key name in a Bitcask (“a Bitcask” is the name for
each file contained within each Bitcask backend) to a fixed-size
structure giving the file, offset, and size of the most recently written
entry for that bucket + key on disk.

To learn about Bitcask see [Hello Bitcask](http://basho.com/hello-bitcask/) on the Basho blog as well as the [Introduction to Bitcask](http://basho.com/assets/bitcask-intro.pdf) paper.

If your calculated RAM needs will exceed your hardware resources--in other words, if you can't afford the RAM to use Bitcask---we recommend that you use LevelDB.

Check out [Bitcask Capacity Planning][plan bitcask capacity] for more details on designing a Bitcask-backed cluster.

##### LevelDB

If RAM requirements for Bitcask are prohibitive, we recommend use of
the LevelDB backend. While LevelDB doesn't require a large amount of RAM
to operate, supplying it with the maximum amount of memory available leads to higher performance.

For more information see [LevelDB][plan backend leveldb].

#### Disk

Now that you have an idea of how much RAM you'll need, it's time to think about disk space. Disk space needs are much easier to calculate. Below is an equation to help you calculate disk space needs:

##### Estimated Total Objects * Average Object Size * n_val

For example:

* 50,000,000 objects
* an average object size of two kilobytes (2,048 bytes)
* the default `n_val` of 3

Then you would need just over approximately **286 GB** of disk space in the entire cluster to accommodate your data.

We believe that databases should be durable out of the box. When we
built Riak, we did so in a way that you could write to disk while
keeping response times below your users' expectations. So this
calculation assumes that you'll be keeping the entire data set on disk.

Many of the considerations taken when configuring a machine to serve a
database apply to configuring a node for Riak as well. Mounting
disks with noatime and having separate disks for your OS and Riak data
lead to much better performance. See [Planning for a
Riak System]({{< product-version-root >}}explanation/storage/) for more information.

##### Disk Space Planning and Ownership Handoff

When Riak nodes fail or leave the cluster, other nodes in the cluster start the **ownership handoff** process. Ownership handoff is when remaining nodes take ownership of the data partitions handled by an absent node. One side effect of this process is that the other nodes require more intensive disk space usage; in rare cases filling the disk of one or more of those nodes.

When making disk space planning decisions, we recommend that you:

* assume that one or more nodes may be down at any time
* monitor your disk space usage and add additional space when usage
  exceeds 50-60% of available space.

Another possibility worth considering is using Riak with a filesystem
that allows for growth, for example
[LVM],
[RAID](http://en.wikipedia.org/wiki/RAID), or
[ZFS](http://en.wikipedia.org/wiki/ZFS).

#### Read/Write Profile

Read/write ratios, as well as the distribution of key access, should
influence the configuration and design of your cluster. If your use case
is write heavy, you will need less RAM for caching, and if only a
certain portion of keys is accessed regularly, such as a [Pareto
distribution](http://en.wikipedia.org/wiki/Pareto_distribution), you
won't need as much RAM available to cache those keys' values.

#### Number of Nodes

The number of nodes (i.e. physical servers) in your OpenRiak cluster depends
on the number of times data is [replicated][concept replication] across the
cluster.  To ensure that the cluster is always available to respond to
read and write requests, we recommend a "sane default" of N=3
replicas.  This requirement can be met with a 3 or 4-node
cluster.

For production deployments, however, we recommend using no fewer than 5
nodes, as node failures in smaller clusters can compromise the
fault-tolerance of the system.  Additionally, in clusters smaller than 5
nodes, a high percentage of the nodes (75-100% of them) will need to
respond to each request, putting undue load on the cluster that may
degrade performance.  For more details on this recommendation, see our
blog post on [Why Your OpenRiak cluster Should Have at Least Five
Nodes](http://basho.com/posts/technical/Why-Your-Riak-Cluster-Should-Have-At-Least-Five-Nodes/).

#### Scaling

Riak can be scaled in two ways: vertically, via improved hardware, and
horizontally, by adding more nodes. Both ways can provide performance
and capacity benefits, but should be used in different circumstances.
The [riak admin cluster command][use admin riak admin#cluster] can
assist scaling in both directions.

##### Vertical Scaling

Vertical scaling, or improving the capabilities of a node/server,
provides greater capacity to the node but does not decrease the overall
load on existing members of the cluster. That is, the ability of the
improved node to handle existing load is increased but the load itself
is unchanged. Reasons to scale vertically include increasing IOPS (I/O
Operations Per Second), increasing CPU/RAM capacity, and increasing disk
capacity.

###### Horizontal Scaling

Horizontal scaling, or increasing the number of nodes in the cluster,
reduces the responsibilities of each member node by reducing the number
of partitions and providing additional endpoints for client connections.
That is, the capacity of each individual node does not change but its
load is decreased. Reasons to scale horizontally include increasing I/O
concurrency, reducing the load on existing nodes, and increasing disk
capacity.

> **Note on horizontal scaling**
>
> When scaling horizontally, it's best to add all planned nodes at once
with multiple `riak admin cluster join` commands followed by
a `riak admin cluster plan` and `riak admin cluster commit`. This will help reduce the amount of data transferred between nodes in the cluster.

###### Reducing Horizontal Scale

If an OpenRiak cluster is over provisioned, or in response to seasonal usage decreases, the horizontal scale of an OpenRiak cluster can be decreased using the `riak admin cluster leave` command.

#### Ring Size/Number of Partitions

Ring size is the number of partitions that make up your OpenRiak cluster. Ring sizes must be a power of 2. Ring size is configured before your cluster is started, and is set in your [configuration files][config reference].

The default number of partitions in an OpenRiak cluster is 64. This works for smaller clusters, but if you plan to grow your cluster past 5 nodes we recommend a larger ring size.

The minimum number of partitions recommended per node is 10. You can determine the number of partitions allocated per node by dividing the number of partitions by the number of nodes.

There are no absolute rules for the ideal partitions-per-node ratio. This depends on your particular use case and what features the OpenRiak cluster uses. We recommend between 10 and 50 data partitions per node.

So if you're running a 3-node development cluster, a ring size of 64 or 128 should work just fine. While a 10-node cluster should work well with a ring size of 128 or 256 (64 is too small while 512 is likely too large).

The table below provides some suggested combinations:

Number of nodes | Number of data partitions
:---------------|:-------------------------
3, 4, 5 | 64, 128
5 | 64, 128
6 | 64, 128, 256
7, 8, 9, 10 | 128, 256
11, 12 | 128, 256, 512

By extension, a ring size of 1024 is advisable only in clusters with
more than 20 nodes, 2048 in clusters with more than 40 nodes, etc.

If you're unsure about the best number of partitions to use, consult the
[Riak mailing
list](http://lists.basho.com/mailman/listinfo/riak-users_lists.basho.com)
for suggestions from the Riak community.

#### Other Factors

Riak is built to run in a clustered environment, and while it will
compensate for network partitions, they do cause increased load on the
system. In addition, running in a virtualized environment that lacks
low-latency IO access can drastically decrease performance. Before
putting your OpenRiak cluster in production is recommended that you gain a
full understanding of your environment's behavior so that you know how
your cluster performs under load for an extended period of time. Doing
so will help you size your cluster for future growth and lead to optimal
performance.

We recommend using [Basho Bench][perf benchmark] for benchmarking the performance of your cluster.

##### Bandwidth

Riak uses Erlang's built-in distribution capabilities to provide
reliable access to data. A OpenRiak cluster can be deployed in many
different network environments. We recommend that you produce as
little latency between nodes as possible, as high latency leads to
sub-optimal performance.

Deploying a single OpenRiak cluster across two datacenters is not recommended. If your use case requires this capability, Riak offers a [Multi Data Center Replication: Architecture]({{< product-version-root >}}explanation/replication/multi-datacenter-architecture/) option that is built to keep multiple Riak clusters in
sync across several geographically diverse deployments.

##### I/O

In general, the biggest bottleneck for Riak will be the amount of I/O
available to it, especially in the case of write-heavy workloads. Riak
functions much like any other database and the design of your disk
access should take this into account. Because Riak is clustered and your
data is stored on multiple physical nodes, you should consider forgoing
a traditional RAID setup for redundancy and focus on providing the least
latency possible using SATA Drives or SSDs, for example.
