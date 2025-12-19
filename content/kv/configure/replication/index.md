---
title: Replication
sidebar_label: "Replication"
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';

[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

[overview]: #overview
[config reference]: #configuration-reference
[verify settings]: #verify-settings
[what is replicated]: #what-is-and-is-not-replicated
[queing system]: #queuing-system
[fullsync replication]: #fullsync-replication
[sink nodes]: #sink-nodes

NextGenRepl provides a considerable improvement over the legacy replication engines. It is faster, more efficient and more reliable. NextGenRepl is the recommended replication engine to use.

## Overview

>[!NOTE]Note on Replication configuration
>The configuration is now kept in the `riak.conf` configuration file. The CLI cannot be used to configure NextGenRepl.
>
>All management is now done via `riak attach` and not through the CLI like before.

NextGenRepl comprises of four main parts.

On the source cluster:
    * A queuing system holding multiple queues with references to changed objects
        ** FullSync to populate the queuing system with Riak objects that are different from the sink cluster
        ** Realtime to populate the queuing system on each change of a Riak object
    * On the sink cluster:
        ** A consumer process that reads the queue from any source clusters and updates the sink cluster

Best performance with lowest overheads is provided by using the ProtocolBuffer API instead of the HTTP API. Security (TLS and certificate authentication) will only work with ProtocolBuffer API.

>[!NOTE]
>NextGenRepl relies on TicTac AAE, so this must be enabled.

## Configuration Reference

A configuration reference is available for quick reference [here]((: ../../configure/replication/reference))

## Verify Settings

Once your configuration is set, you can verify its correctness by running the riak command-line tool:

    ```bash
        riak chkconfig
    ```

## What is and is not replicated

Only Riak objects are replicated, not bucket properties or bucket types. Please create the bucket types and set any custom bucket properties before replicating.

These will be replicated:

* Riak objects
* Riak Tombstones
* 2i indexes

These will not be replicated:

* Bucket types
* Bucket properties

## Queuing System

The heart of the NextGenRepl system is the queuing system.

You can have as many queues as you like with different filters on each queue.

Each queue has 3 levels of priority:

* RealTime changes - these are normally copies of the Riak object, but can be references to the Riak object if the queue gets too large. These are populated automatically when a PUT (which includes inserts, updates and deletes) occurs.
* FullSync changes - these are references to Riak objects and are populated on the source cluster when the FullSync manager finds differences between the source cluster and the sink cluster.
* Admin changes - these are references to Riak objects and are populated when the administrator performs actions via the TicTac AAE Fold commands.

The sink side replication manager will connect to its list of replication sources and replicate objects using these priorities - so RealTime changes first, FullSync differences second, and finally the admin changes.

The queuing system is always active.

[Learn More >>](: ../../configure/replication/queue))

## FullSync replication

NextGenRepl’s FullSync works on an automated schedule whereupon a source cluster node checks for changes with a predefined sink cluster node (or load balancer). It then pushes any changes found to a specific preconfigured queue in the queuing system.

A source node can connect to 1 sink node using an IP address or FQDN to check for differences. This can be the IP or FQDN of a load balancer for the sink cluster. Each source node can have the the same FullSync settings as the other source cluster nodes, or entirely different FullSync settings per node if needed.

A source node will sync data from all nodes in the source cluster.

A source node will run FullSync according to the schedule on that specific source node. The source nodes will co-ordinate to ensure that only one FullSync task runs at a time.

If a source node or sink peer is offline for any reason, Riak will wait until the node is repaired before continuing. You should ensure that sufficient redundancies are in place to ensure uptime. This can be done by having multiple source nodes connecting to the same sink cluster, and by using a load balancer in front of the sink cluster.

The number of different clusters you can FullSync to is defined by the number of Riak KV nodes in the source cluster.

[Learn More >>](: ../../configure/replication/fullsync))

## RealTime replication

As changes occur on the source cluster, NextGenRepl’s RealTime replication system will add them to one or more configurable queues within the replication queuing system.

A source node can be the source for multiple sink clusters by using multiple queues.

[Learn More >>](: ../../configure/replication/real-time))

## Sink Nodes

Each sink node will automatically pull changes on a pseudo-realtime basis from a single configurable queue held by one or more source nodes.

A sink node can pull updates from one or more source nodes but is limited to a single configurable queue name per sink node. It is better to directly list multiple source nodes in a source cluster than to point to a load balancer in front of the source cluster. You can list as many source nodes from as many clusters as you like for a given sink node, but they must all use the same queue name.

If a specific source node is offline for any reason, the sink node will automatically change how often it checks that specifc source node for updates. So if a source node is taken down for admin or hardware failure reasons, the sink node will adapt automatically to the failure and the subsequent recovery.

[Learn More >>](: ../../configure/replication/sink))