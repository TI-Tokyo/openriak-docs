---
title: 'Configure real-time replication'
description: 'Show operators how to configure real-time replication and validate data movement.'
weight: 5
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\replication\real-time.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\next-gen-replication\realtime.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#configuration-of-real-time-replication'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#enable-a-real-time-sink'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#enable-a-real-time-source'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure real-time replication and validate data movement.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### RealTime

[configure tictacaae]: {{< product-version-root >}}foundations/replication/tictac-aae/
[configure nextgenrepl fullsync]: ../fullsync/
[configure nextgenrepl realtime]: ../realtime/
[configure nextgenrepl queuing]: {{< product-version-root >}}foundations/replication/queues/
[configure nextgenrepl queue filters]: {{< product-version-root >}}foundations/replication/queues/#queue-filters

NextGenRepl's RealTime feature provides a considerable improvement over the legacy realtime engines. It is faster, more efficient, and more reliable. NextGenRepl is the recommended replication engine to use.

RealTime will ensure that the data in the sink cluster is updated as quickly as possible from the source clusters.

**Note:**
NextGenRepl relies on [TicTac AAE]({{< product-version-root >}}foundations/replication/tictac-aae/), so this must be enabled.

#### Overview

As changes occur on the source cluster, NextGenRepl's RealTime replication system will add them to one or more configurable queues within the [replication queuing system][configure nextgenrepl queuing].

A source node can be the source for multiple sink clusters by using multiple queues.

**Note:**
Currently all changes listed in this documentation to NextGenRepl must be made by changing the values in the `riak.conf` file.

#### Enable RealTime

RealTime changes are added to the queuing system by setting:

```
replrtq_enablesrc = enabled
```

By default, RealTime is turned off (`disabled`).

#### Queues

At least one replication queue should allow RealTime objects to be added. The easiest way to do this is to have a queue filter of `any`, but [other options are available][configure nextgenrepl queue filters].

By default, there is no queue setup for RealTime. To set the default queue to also allow RealTime queues, change:

```
replrtq_srcqueue = q1_ttaaefs:block_rtq
```

to

```
replrtq_srcqueue = q1_ttaaefs:any
```

To add a new queue called `my-replication-queue` that allowed RealTime replication for any bucket, you would add `my-replication-queue:any` to the `replrtq_srcqueue` setting. For example, to keep the default FullSync-only queue and add a second queue for RealTime you would set:

```
replrtq_srcqueue = q1_ttaaefs:block_rtq|my-replication-queue:any
```

#### Enable a Real-Time Source

There are two configuration items required to set up a source for real-time replication; `replrtq_enablesrc` and `replrtq_srcqueue`.  These are both set via `riak.conf`:

- `replrtq_enablesrc = enabled`;
  - This is the basic configuration required to inform PUT coordinators to pass changes to the replication source queue on the node.
- `replrtq_srcqueue = <sink_cluster_name>:<queue_filter>|<sink_cluster_name>:<queue_filter>` ...
  - The source queue configuration is a pipe-delimited set of queue/filter pairs, where the queue and the filter are split by a `:`.
  - The queue name is normally set as a reference to the sink cluster which is expected to consume from the queue.
  - The queue filter will be `any` to enable real-time replication;
    - The queue filter may be set to `block_rtrq` if the queue is not to support real-time replication, but is only to be used for either reconciliation or seeding.
    - The queue filter may be set to `buckettype.<name_of_type>` to only replicate buckets in a certain bucket type.
    - The queue filter may be set to `bucketname.<name_of_bucket>` or `bucketprefix.<prefix_for_bucket>` to only replicate buckets with a given name or a name with a given prefix.
      - Bucket name filters will work for typed and legacy buckets, with typed buckets the type will be ignored when using a name or prefix filter.

For replication, the real-time replication source must be enabled on every node in the cluster, as a PUT may be coordinated from any vnode (on any node), regardless of which node received the PUT request.

> By convention, the name of the queues are normally aligned with the names of the cluster that is to consume from the queue i.e. `<sink_cluster_name>`.  However, the name can be anything descriptive for the context in which the queue is to be used.

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

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
