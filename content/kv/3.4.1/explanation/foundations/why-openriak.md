---
title: 'Why OpenRiak KV'
description: 'Explain why openriak kv and why it matters when designing or operating OpenRiak systems.'
weight: 9
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
  - 'developers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\why-riak-kv.md'
source_material:
  - 'legacy-3.2.5'
  - 'openriak-discussions'
  - 'live-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/#what-is-riak'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain why openriak kv and why it matters when designing or operating OpenRiak systems.

## Overview

### Why OpenRiak KV?

[apps replication properties]: {{< baseurl >}}kv/3.4.1/explanation/replication/references-and-triggers/
[Basho Bench]: {{< baseurl >}}kv/3.4.1/how-to/tune/benchmark-cluster/
[cluster ops strong consistency]: {{< baseurl >}}kv/3.4.1/explanation/consistency/strong-consistency/
[concept eventual consistency]: {{< baseurl >}}kv/3.4.1/explanation/consistency/eventual-consistency/
[convergent replicated data types]: http://hal.upmc.fr/docs/00/55/55/88/PDF/techreport.pdf
[Datomic]: http://www.datomic.com/overview.html
[dev data types]: {{< baseurl >}}kv/3.4.1/reference/data/distributed-data-types/
[glossary read rep]: {{< baseurl >}}kv/3.4.1/explanation/foundations/glossary/#read-repair

#### What is Riak?

Riak is a distributed database designed to deliver maximum data
availability by distributing data across multiple servers. As long as
your Riak client can reach *one* Riak server, it should be able to write
data.

Riak is used as an **eventually consistent** system in that the data you want to read should remain available in most failure scenarios, although it may not be the most up-to-date version of that data.

##### Basho's goals for Riak

Goal | Description
-------|-------
**Availability** | Riak writes to and reads from multiple servers to offer data availability even when hardware or the network itself are experiencing failure conditions
**Operational simplicity** | Easily add new machines to your OpenRiak cluster without incurring a larger operational burden
**Scalability** | Riak automatically distributes data around the cluster and yields a near-linear performance increase as you add capacity
**Masterless** | Your requests are not held hostage to a specific server in the cluster that may or may not be available

##### When Riak makes sense

If your data does not fit on a single server and demands a distributed
database architecture, you should take a close look at Riak as a
potential solution to your data availability issues. Getting distributed
databases right is **very** difficult, and Riak was built to address the
problem of data availability with as few trade-offs and downsides as
possible.

OpenRiak's focus on availability makes it a good fit whenever downtime is
unacceptable. No one can promise 100% uptime, but Riak is designed to
survive network partitions and hardware failures that would
significantly disrupt most databases.

A less-heralded feature of Riak is its predictable latency. Because its
fundamental operations---read, write, and delete---do not involve
complex data joins or locks, it services those requests promptly. Thanks
to this capability, Riak is often selected as a data storage backend for
data management software from a variety of paradigms, such as
[Datomic].

From the standpoint of the actual content of your data, Riak might also
be a good choice if your data can be modeled as one of OpenRiak's currently
available [Data Types][dev data types]:  flags, registers, counters,
sets, or maps. These Data Types enable you to take advantage of OpenRiak's
high availability approach while simplifying application development.

##### When Riak is Less of a Good Fit

We recommend running no fewer than 5 data servers in a cluster.
This means that Riak can be overkill for small databases. If you're not
already sure that you will need a distributed database, there's a good
chance that you won't need Riak.

If explosive growth is a possibility, however, you are always highly
advised to prepare for that in advance. Scaling at Internet speeds is
sometimes compared to overhauling an airplane mid-flight. If you feel
that such a transition might be necessary in the future, then you might
want to consider Riak.

OpenRiak's simple data model, consisting of keys and values as its atomic
elements, means that your data must be denormalized if your system is to
be reasonably performant. For most applications this is not a serious
hurdle. But if your data simply cannot be effectively managed as keys
and values, Riak will most likely not be the best fit for you.

Correspondingly, if your application demands a high query load by any
means other than key/value lookup---e.g. SQL-style `SELECT * FROM table`
operations---Riak will not be as efficient as other databases. If you
wish to compare Riak with other data technologies, Basho offers a tool
called [Basho Bench] to help measure its performance, so that you can
decide whether the availability and operational benefits of Riak
outweigh its disadvantages.

#### How Does an OpenRiak cluster Work?

A OpenRiak cluster is a group of **nodes** that are in constant
communication to ensure data availability and partition tolerance.

##### What is an OpenRiak node?

A OpenRiak node is not quite the same as a server, but in a production
environment the two should be equivalent. A developer may run multiple
nodes on a single laptop, but this would never be advisable in a real
production cluster.

Each node in an OpenRiak cluster is equivalent, containing a complete,
independent copy of the whole Riak package. There is no "master" node;
no node has more responsibilities than others; and no node has special
tasks not performed by other nodes. This uniformity provides the basis
for OpenRiak's fault tolerance and scalability.

Each node is responsible for multiple data partitions, as discussed
below:

##### Riak Automatically Re-Distributes Data When Capacity is Added

When you add (or remove) machines, data is rebalanced automatically with
no downtime. New machines claim data until ownership is equally spread
around the cluster, with the resulting cluster status updates shared to
every node via a gossip protocol and used to route requests. This is
what makes it possible for any node in the cluster to receive requests.
The end result is that developers don't need to deal with the underlying
complexity of where data lives.

##### Consistent Hashing

Data is distributed across nodes using consistent hashing. Consistent
hashing ensures that data is evenly distributed around the cluster and
makes possible the automatic redistribution of data as the cluster
scales.

##### Intelligent Replication

OpenRiak's replication scheme ensures that you can still read, write, and
update data if nodes go down. Riak allows you to set a replication
variable, N (also known as the `n_val`), that specifies the number of
nodes on which a value will be replicated.

An `n_val` value of 3 (the default) means that each object is replicated
3 times. When an object's key is mapped onto a given node, Riak will
continue on and automatically replicate the data onto two more nodes.
This parameter enables you to replicate values to 7 nodes in a 10-node
cluster, 10 nodes in a 15-node cluster, and so on.

#### When Things Go Wrong

Riak retains fault tolerance, data integrity, and availability even in
failure conditions such as hardware failure and network partitions. Riak
has a number of means of addressing these scenarios and other bumps in
the road, like version conflicts in data.

##### Hinted Handoff

Hinted handoff enables Riak to handle node failure. If a node goes down,
a neighboring node will take over its storage operations. When the
failed node returns, the updates received by the neighboring node are
handed back to it. This ensures that availability for writes and updates
is maintained automatically, minimizing the operational burden of
failure conditions.

##### Version Conflicts

In any system that replicates data, conflicts can arise, for example
when two clients update the same object at the exact same time or when
not all updates have yet reached hardware that is experiencing lag.

In Riak, replicas are [eventually consistent][concept eventual consistency],
meaning that while data is always available, not all replicas may have
the most recent update at the exact same time, causing brief
periods---generally on the order of milliseconds---of inconsistency
while all state changes are synchronized.

Riak addresses data conflicts as follows: When you make a read request,
Riak looks up all replicas for that object. By default, Riak will return
the most recently updated version, determined by looking at the object's
vector clock. Vector clocks are metadata attached to each replica when
it is created. They are extended each time a replica is updated to keep
track of versions. You can also allow clients to resolve conflicts
themselves if that is a better fit for your use case.

##### Riak Data Types

If you are not interested in dealing with version conflicts on the
application side, [Riak Data Types][dev data types] offer a powerful
yet easy-to-use means of storing certain types of data while allowing
Riak to handle merge conflicts. These conflicts are resolved
automatically by Riak using Data Type-specific algorithms inspired by
research into [convergent replicated data types].

##### Read Repair

When an outdated replica is returned as part of a read request, Riak
will automatically update the out-of-sync replica to make it consistent.
[Read repair][glossary read rep], a self-healing property of
the database, will even update a replica that returns a `not_found` in
the event that a node loses the data due to physical failure.

##### Reading and Writing Data in Failure Conditions

In Riak, you can set an R value for reads and a W value for writes.
These values give you control over how many replicas must respond to a
request for it to succeed.

Let's say that you have an N value of 3 (aka `n_val=3`) for a particular
key/value pair, but one of the physical nodes responsible for a replica
is down. With an `r=2` setting, only 2 replicas must return results for
read to be deemed successful. This allows Riak to provide read
availability even when nodes are down or laggy. The same applies for the
W in writes. If this value is not specified, Riak defaults to `quorum`,
according to which the majority of nodes must respond.

There is more on [replication properties][apps replication properties] elsewhere in the
documentation.

### [OpenRiak QuickDocs 3.4](https://openriak.github.io/riak/)

#### What is Riak?

Riak is a distributed key-value store, designed to provide high-availability with predictable response times in the presence of complex failure scenarios. It can be configured to provide assurance against data loss, even where individual nodes have ephemeral storage, and groups of nodes can be concurrently impacted by failure events.

> It is a reliable system whilst running on simple, low-cost, commodity components - remaining highly available without the need for urgent operator intervention.

Riak is commonly used as a schema-free database for the storage and indexing of records, documents, objects or binaries with minimal constraints imposed by the database. In functional terms, Riak can be considered to be a hybrid combination of some of the features available within S3 and DynamoDB.

Riak fully supports multi-cluster environments (within and across physical locations), where open replication is possible not just between Riak clusters, but between Riak clusters and other database services. With Riak, reconciliation is considered as important as replication. Clusters may come in different shapes and sizes - but it is important that as well as replicating data between clusters, it is possible to do rapid and continuous verification that clusters are synchronised.

> Riak users have been running large-scale production databases in mission-critical environments on commodity hardware with more than a decade of continuous uptime.  These environments are noted not just for their high availability, but for their low operator-intervention rates.

Riak is often preferred in organisations where technology choices need to be long-lasting, and ongoing operational costs are a more important consideration than up-front developer costs.

Riak is built almost entirely using [OTP](https://www.erlang.org/), a platform designed from the start to support the next generation of reliable systems. Over the past few years Riak has been evolved to make better use of the platform, and is now supported on an ongoing basis by the OpenRiak Working Group of the [Erlang Ecosystem Foundation](https://erlef.org/).
