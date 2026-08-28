---
title: 'Configure replication sink nodes'
description: 'Show operators how to configure replication sink nodes and validate data movement.'
weight: 8
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\replication\sink.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\next-gen-replication\sink.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#enable-a-real-time-sink'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure replication sink nodes and validate data movement.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Sink Nodes

[configure tictacaae]: ../../active-anti-entropy/tictac-aae/
[configure nextgenrepl fullsync]: ../fullsync/
[configure nextgenrepl realtime]: ../realtime/
[configure nextgenrepl queuing]: ../queuing/
[configure nextgenrepl queue filters]: ../queuing/#queue-filters

NextGenRepl's RealTime feature provides a considerable improvement over the legacy realtime engines. It is faster, more efficient, and more reliable. NextGenRepl is the recommended replication engine to use.

**Note:**
NextGenRepl relies on [TicTac AAE](../../active-anti-entropy/tictac-aae/), so this must be enabled.

#### Overview

Sink nodes pull changes from the [Queuing System][configure nextgenrepl queuing] on the source nodes. This will handle both FullSync and RealTime replication as configured on the source nodes.

**Note:**
Currently all changes listed in this documentation to NextGenRepl must be made by changing the values in the `riak.conf` file.

#### Enable sink

RealTime, FullSync and AAE fold changes will be pulled as part of the NextGenRepl sink process. This is the same process for all NextGenRepl replication types.

To turn on the NextGenRepl sink process, set this in the `riak.conf` on the sink nodes:

```
replrtq_enablesink = enabled
```

By default, NextGenRepl is turned off (`disabled`).

#### Queue name

A specific node will always pull from a specific named queue from all configured source nodes. This queue name is specified by setting `replrtq_sinkqueue`. For example, to read from the source queue called `my-replication-queue` you would set:

```
replrtq_sinkqueue = my-replication-queue
```

This value can vary between nodes in a sink cluster if you want to read from multiple queues in the source cluster(s).

#### Sink connections

A single sink node can pull changes from multiple sources. This could be for redundancy purposes (each sink node talking to every node in a source cluster) or for replication from multiple clusters (each sink node talking to a one or more nodes in several source clusters).

The queue checked on source nodes will be the queue specified in `replrtq_sinkqueue` regardless of the connection used. To use multiple queues, configure different sink nodes with different `replrtq_sinkqueue` values.

In general, do not use a load balancer as a source. Always use an actual OpenRiak KV nodes unless carefully thought out.

The list of source nodes for the sink node to connect to is specified in `replrtq_sinkpeers`. This holds a `|` deliminated list of peer connection strings. Each peer connection string is a 3-value tuple deliminated by a `:` consisting of IP/FQDN, port, and protocol.

Some examples of a single peer connection string would be:

- `node01.source-cluster.mynetwork.com:8098:http` - connect to the FQDN `node01.source-cluster.mynetwork.com` on port `8098` using the HTTP API.
- `node01.source-cluster.mynetwork.com:8087:pb` - connect to the FQDN `node01.source-cluster.mynetwork.com` on port `8087` using the Protocol Buffer API.
- `10.2.34.56:8098:http` - connect to the IP address `10.2.34.56` on port `8098` using the HTTP API.

To specify multiple peer connection strings in `replrtq_sinkpeers`, join the individual peer connection strings together with a `|`. For example, this will connect to three nodes in the same source cluster using Procotol Buffers:

```
replrtq_sinkpeers = node01.source-cluster-a.mynetwork.com:8087:pb|node02.source-cluster-a.mynetwork.com:8087:pb|node03.source-cluster-a.mynetwork.com:8087:pb
```

As another example, this will connect to one node in 3 different source clusters using Procotol Buffers:

```
replrtq_sinkpeers = node01.source-cluster-a.mynetwork.com:8087:pb|node01.source-cluster-b.mynetwork.com:8087:pb|node01.source-cluster-c.mynetwork.com:8087:pb
```

As a third example, this will connect to one node in 3 different source clusters using HTTP:

```
replrtq_sinkpeers = node01.source-cluster-a.mynetwork.com:8098:http|node01.source-cluster-b.mynetwork.com:8098:http|node01.source-cluster-c.mynetwork.com:8098:http
```

It is also possible to mix HTTP and Protocol Buffer connection strings. For example, this will connect to one node using HTTP and other nodes using Protocol Buffers:

```
replrtq_sinkpeers = node01.source-cluster-a.mynetwork.com:8098:http|node01.source-cluster-b.mynetwork.com:8087:pb|node01.source-cluster-c.mynetwork.com:8087:pb
```

For the purposes of redundancy, it is best to have replication enabled on every sink node, and to have every sink node talk to every source node. If a source node becomes unavailable, Riak will automatically reduce how often that peer is checked until the peer becomes available again.

If you need to have TLS security and certificate-based authentication then you must exclusively use the Protocol Buffer API (`pb`) for replication.

#### Tuning

There are two easily changed values for tuning.

The total number of worker processes per sink node that consume objects from the source nodes is defined in `replrtq_sinkworkers` and defaults to 24 simultaneous workers. If the queues on the source side are growing, then this value should be increased.

NextGenRepl will allocate workers to connections to each source node based on performance. A limit can be set for the maximum number of workers connected to a single node by setting `replrtq_sinkpeerlimit`. This defaults to 24 as well.

#### Enable a Real-Time Sink

There are five configuration items required to set up a sink for real-time replication: enablement, queue definition, peers, workers and peer discovery.  All elements are set via `riak.conf`:

- `replrtq_enablesink = enabled`.
- `replrtq_sinkqueue = <sink_cluster_name>`;
  - The name of the queue, on any source node or cluster from which this sink may need to consume replication events.
  - The name of the queue does not need to be the cluster name, it can be any description that is helpful in context.
- `replrtq_sinkpeers = <ip_addr>:<port>:<protocol>|<ip_addr>:<port>:<protocol>` ...
  - A pipe delimited list of peers by IP, port and protocol (`pb` or `http`).
    - For efficiency, it is recommended to use the PB protocol.
    - If TLS enablement of the replication communication is required, then PB protocol must be used.
  - The peer node must have a listener enabled for that protocol on that port.
  - If `replrtq_peer_discovery` is enabled, then the list of peers will be used to discover other peer nodes on the clusters, and the discovered list will be the peers used by the sink.
  - The list may include nodes in different clusters.
  - For resilience, always connect sink nodes to a diverse set of source peers, even when peer discovery is enabled.
- `replrtq_sinkworkers = <worker_count>`
  - The count of sink workers which will be used on this node to fetch replicated objects from the source.
  - May be limited to control the impact of a sink cluster on the source cluster, in particular when fetching a backlog from the queue.
- Available from Riak 3.0.10`replrtq_peer_discovery = enabled`
  - Enables a peer discovery process, which will use the configured peer to discover other peers in the cluster.
  - The cluster listeners on that protocol must be listening on reachable IP addresses and ports for peer discovery to work (i.e. binding a listener to `0.0.0.0` will not work).
  - If the application requires the standard Riak listener to be bound to an unreachable IP address, then the alternative protocol should be used for replication, with the alternative listener configured on a reachable address.

A backoff algorithm is used on the sink to reduce the frequency of requests to nodes returning error responses, and increase the frequency to nodes continuously having ready replication events on the queue.  This means that sink workers will automatically favour fetching from nodes with backlogs of replication activity.

[overview]: #overview
[enable sink]: #enable-sink
[queue name]: #queue-name
[sink connection]: #sink-connections
[tuning]: #tuning

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
