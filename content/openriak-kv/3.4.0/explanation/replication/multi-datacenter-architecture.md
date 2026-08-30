---
title: 'Multi-datacenter replication architecture'
description: 'Explain multi-datacenter replication architecture, its data flow, failure behavior, and operational trade-offs.'
weight: 5
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\multi-datacenter.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v2-multi-datacenter\architecture.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v3-multi-datacenter\architecture.md'
  - 'Legacy multi-datacenter replication terminology and commands require compatibility review.'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#interconnecting-multiple-clusters'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain multi-datacenter replication architecture, its data flow, failure behavior, and operational trade-offs.

## Overview

### Multi-Datacenter Reference

[ref mdc stats]: {{< product-version-root >}}explanation/replication/multi-datacenter-architecture/
[ref mdc per bucket]: {{< product-version-root >}}explanation/replication/multi-datacenter-architecture/
[ref mdc monitor]: {{< product-version-root >}}explanation/replication/multi-datacenter-architecture/
[ref mdc comparison]: {{< product-version-root >}}explanation/replication/multi-datacenter-architecture/

#### In This Section

##### [Multi-Datacenter Replication Reference: Statistics][ref mdc stats]

Describes the output of `riak repl status` interface.

[Learn More >>][ref mdc stats]

###### [Multi-Datacenter Replication Reference: Per Bucket][ref mdc per bucket]

Details enabling & disabling of per bucket replication.

[Learn More >>][ref mdc per bucket]

###### [Multi-Datacenter Replication Reference: Monitoring][ref mdc monitor]

Overview of monitoring in a Multi-Datacenter environment.

[Learn More >>][ref mdc monitor]

###### [Multi-Datacenter Replication Reference: Comparison][ref mdc comparison]

Compares Version 2 and Version 3 of OpenRiak's Multi-Datacenter Replication capabilities.

[Learn More >>][ref mdc comparison]

### V2 Multi-Datacenter Replication Reference: Architecture

**Deprecation Warning**
v2 Multi-Datacenter Replication is deprecated and will be removed in a future version. Please use [v3]({{< product-version-root >}}explanation/replication/multi-datacenter-architecture/) instead.

This document provides a basic overview of the architecture undergirding
OpenRiak's Multi-Datacenter Replication capabilities.

#### How Replication Works

When Multi-Datacenter Replication is implemented, one OpenRiak cluster acts
as a **primary cluster**. The primary cluster handles replication
requests from one or more **secondary clusters** (generally located in
datacenters in other regions or countries). If the datacenter with the
primary cluster goes down, a secondary cluster can take over as the
primary cluster. In this sense, OpenRiak's multi-datacenter capabilities are
masterless.

Multi-Datacenter Replication has two primary modes of operation:
**fullsync** and **realtime**. In fullsync mode, a complete
synchronization occurs between primary and secondary cluster(s); in
realtime mode, continual, incremental synchronization occurs, i.e.
replication is triggered by new updates.

Fullsync is performed upon initial connection of a secondary cluster,
and then periodically thereafter (every 360 minutes is the default, but
this can be modified). Fullsync is also triggered if the TCP connection
between primary and secondary cluster is severed and then recovered.

Both fullsync and realtime mode are described in detail below.
But first, a few key concepts.

#### Concepts

##### Listener Nodes

Listeners, also called **servers**, are Riak nodes in the primary
cluster that listen on an external IP address for replication requests.
Any node in an OpenRiak cluster can participate as a listener. Adding more
nodes will increase the fault tolerance of the replication process in
the event of individual node failures. If a listener node goes down,
another node can take its place.

##### Site Nodes

Site nodes, also called **clients**, are Riak nodes on a secondary
cluster that connect to listener nodes and send replication initiation
requests. Site nodes are paired with a listener node when started.

##### Leadership

Only one node in each cluster will serve as the lead site (client) or
listener (server) node. Riak replication uses a leadership-election
protocol to determine which node in the cluster will participate in
replication. If a site connects to a node in the primary cluster that is
not the leader, it will be redirected to the listener node that is
currently the leader.

#### Fullsync Replication

Riak performs the following steps during fullsync
replication, as illustrated in the Figure below.

1. A TCP connection is established between the primary and secondary
   clusters
2. The site node in the secondary cluster initiates fullsync replication
   with the primary node by sending a message to the listener node in
   the primary cluster
3. The site and listener nodes iterate through each [vnode]({{< product-version-root >}}explanation/foundations/glossary/#vnode) in their respective clusters and compute a hash for
   each key's object value. The site node on the secondary cluster sends
   its complete list of key/hash pairs to the listener node in the
   primary cluster. The listener node then sequentially compares its
   key/hash pairs with the primary cluster's pairs, identifying any
   missing objects or updates needed in the secondary cluster.
4. The listener node streams the missing objects/updates to the
   secondary cluster.
5. The secondary cluster replicates the updates within the cluster to
   achieve the new object values, completing the fullsync cycle

<br />
![MDC Fullsync]({{< baseurl >}}images/MDC_Full-sync-small.png)
<br />

#### Realtime Replication

Riak performs the following steps during realtime
replication, as illustrated in the Figure below.

1. The secondary cluster establishes a TCP connection to the primary
2. Realtime replication of a key/object is initiated when an update is
   sent from a client to the primary cluster
3. The primary cluster replicates the object locally
4. The listener node on the primary cluster streams an update to the
   secondary cluster
5. The site node within the secondary cluster receives and replicates
   the update

<br />
![MDC Realtime]({{< baseurl >}}images/MDC-real-time-sync-small.png)
<br />

#### Restrictions

It is important to note that both clusters must have certain attributes
in common for Multi-Datacenter Replication to work. If you are using
either fullsync or realtime replication, both clusters must have the
same [ring size]({{< product-version-root >}}explanation/foundations/clusters-rings-and-partitions/#the-ring); if you are using fullsync
replication, every bucket's [`n_val`]({{< product-version-root >}}explanation/replication/references-and-triggers/#n-value-and-replication) must be the same in both the
source and sink cluster.

### Architecture

[glossary vnode]: {{< product-version-root >}}explanation/foundations/glossary/#vnode
[concept clusters]: {{< product-version-root >}}explanation/foundations/clusters-rings-and-partitions/

#### How Version 3 Replication Works

In Multi-Datacenter (MDC) Replication, a cluster can act as either the

* **source cluster**, which sends replication data to one or
* **sink clusters**, which are generally located in datacenters in other
  regions or countries.

Bidirectional replication can easily be established by making a cluster
both a source and sink to other clusters. Riak
Multi-Datacenter Replication is considered "masterless" in that all
clusters participating will resolve replicated writes via the normal
resolution methods available in Riak.

In Multi-Datacenter Replication, there are two primary modes of
operation:

* **Fullsync** replication is a complete synchronization that occurs
  between source and sink cluster(s), which can be performed upon
  initial connection of a sink cluster if you wish
* **Realtime** replication is a continual, incremental synchronization
  triggered by successful writing of new updates on the source cluster

Fullsync and realtime replication modes are described in detail below.

#### Concepts

##### Sources

A source refers to a cluster that is the primary producer of replication
data. A source can also refer to any node that is part of the source
cluster. Source clusters push data to sink clusters.

##### Sinks

A sink refers to a cluster that is the primary consumer of replication
data. A sink can also refer to any node that is part of the sink
cluster. Sink clusters receive data from source clusters.

##### Cluster Manager

The cluster manager is a Riak service that provides
information regarding nodes and protocols supported by the sink and
source clusters. This information is primarily consumed by the
`riak repl connect` command.

##### Fullsync Coordinator

In fullsync replication, a node on the source cluster is elected to be
the *fullsync coordinator*. This node is responsible for starting and
stopping replication to the sink cluster. It also communicates with the
sink cluster to exchange key lists and ultimately transfer data across a
TCP connection. If a fullsync coordinator is terminated as the result of
an error, it will automatically restart on the current node. If the node
becomes unresponsive, a leader election will take place within 5 seconds
to select a new node from the cluster to become the coordinator. In the
event of a coordinator restart, a fullsync will have to restart.

Fullsync replication scans through the list of partitions in a Riak
cluster and determines which objects in the sink cluster need to be
updated. A source partition is synchronized to a node on the sink
cluster containing the current partition.

In realtime replication, a node in the source cluster will forward data
to the sink cluster. A node in the source cluster does not necessarily
connect to a node containing the same [vnode][glossary vnode] on
the sink cluster. This allows Riak to spread out realtime replication
across the entire cluster, thus improving throughput and making
replication more fault tolerant.

##### Initialization

Before a source cluster can begin pushing realtime updates to a sink,
the following commands must be issued:

1. `riak repl realtime enable <sink_cluster>`

After this command, the realtime queues (one for each OpenRiak node) are
    populated with updates to the source cluster, ready to be pushed to
    the sink.

2. `riak repl realtime start <sink_cluster>`

This instructs the Riak connection manager to contact the sink
    cluster.

<br />
    ![MDC fullsync]({{< baseurl >}}images/MDC-v3-realtime1.png)
    <br />

At this point realtime replication commences.

<ol start="3">
<li>Nodes with queued updates establish connections to the sink cluster
and replication begins.</li>
</ol>

<br />
![MDC fullsync]({{< baseurl >}}images/MDC-v3-realtime2.png)
<br />

##### Realtime queueing and synchronization

Once initialized, realtime replication continues to use the queues to
store data updates for synchronization.

<ol start="4">
<li>The client sends an object to store on the source cluster.</li>
<li>Riak writes N replicas on the source cluster.</li>
</ol>

<br />
![MDC fullsync]({{< baseurl >}}images/MDC-v3-realtime3.png)
<br />

<ol start="6">
<li>The new object is stored in the realtime queue.</li>
<li>The object is copied to the sink cluster.</li>
</ol>

<br />
![MDC fullsync]({{< baseurl >}}images/MDC-v3-realtime4.png)
<br />

<ol start="8">
<li>The destination node on the sink cluster writes the object to N
nodes.</li>
</ol>

<br />
![MDC fullsync]({{< baseurl >}}images/MDC-v3-realtime5.png)
<br />

<ol start="9">
<li>The successful write of the object to the sink cluster is
acknowledged and the object removed from the realtime queue.</li>
</ol>

<br />
![MDC fullsync]({{< baseurl >}}images/MDC-v3-realtime6.png)
<br />

#### Restrictions

It is important to note that both clusters must have certain attributes
in common for Multi-Datacenter Replication to work. If you are using
either fullsync or realtime replication, both clusters must have the
same [ring size][concept clusters]; if you are using fullsync
replication, every bucket's `n_val` must be the same in both the
source and sink cluster.
