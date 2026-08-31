---
title: 'Build a replicated two-cluster environment'
description: 'Guide an operator through enabling TicTac AAE and replicating test data between two disposable clusters.'
weight: 2
diataxis: 'tutorial'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'new-operators'
source_material:
  - 'legacy-3.2.5'
  - 'proposed-kv'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\tutorials\clusterTicTac.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v2-multi-datacenter\quick-start.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v3-multi-datacenter\quick-start.md'
  - 'Legacy multi-datacenter replication terminology and commands require compatibility review.'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide an operator through enabling TicTac AAE and replicating test data between two disposable clusters.

## Overview

### Quickstart

**Deprecation Warning**
v2 Multi-Datacenter Replication is deprecated and will be removed in a future version. Please use [v3]({{< product-version-root >}}tutorials/replication/two-cluster-replication/) instead.

The Riak Multi-Datacenter Replication Quick Start will walk you through
the process of configuring OpenRiak's version 2 Replication to perform
replication between two sample Riak clusters in separate networks. This
guide will also cover bidirectional replication, which is accomplished
by setting up unidirectional replication in both directions between the
clusters.

#### Prerequisites

This Guide assumes that you have completed the following steps:

* [Installing Riak][install index]
* [Performing system tuning|System Performance Tuning][perf index]
* [Reviewing configuration][config v2 mdc]

#### Scenario

Configure Riak MDC to perform replication, given the following
3-node Riak clusters:

##### Cluster 1

Name  | IP          | Node name
:-----|:------------|:----------------
`node1` | `172.16.1.11` | `riak@172.16.1.11`
`node2` | `172.16.1.12` | `riak@172.16.1.12`
`node3` | `172.16.1.13` | `riak@172.16.1.13`

###### Cluster 2

Name  | IP          | Node name
:-----|-------------|-----------------
`node4` | `192.168.1.21` | `riak@192.168.1.21`
`node5` | `192.168.1.22` | `riak@192.168.1.22`
`node6` | `192.168.1.23` | `riak@192.168.1.23`

**Note**: The addresses used in these example clusters are contrived,
non-routable addresses. In real-world applications, however, these
addresses would need to be routable over the public Internet.

#### Set Up Cluster1 &rarr; Cluster2 Replication

##### Set Up the Listeners on Cluster1 (Source cluster)

On a node in Cluster1, `node1` for example, identify the nodes that will
be listening to connections from replication clients with `riak repl
add-listener <nodename> <listen_ip> <port>` for each node that will be
listening for replication clients.

```bash
riak repl add-listener riak@172.16.1.11 172.16.1.11 9010
riak repl add-listener riak@172.16.1.12 172.16.1.12 9010
riak repl add-listener riak@172.16.1.13 172.16.1.13 9010
```

##### Set Up the Site on Cluster2 (Site cluster)

On a node in Cluster2, `node4` for example, inform the replication
clients where the Source Listeners are located with `riak repl add-site
<ipaddr> <port> <sitename>`. Use the IP address(es) and port(s) you
configured in the earlier step. For `sitename` enter `Cluster1`.

```bash
riak repl add-site 172.16.1.11 9010 Cluster1
```

**Note**: While a Listener needs to be added to each node, only a single
Site needs to be added on the Site cluster. Once connected to the Source
cluster, it will get the locations of the rest of the Listeners in the
Source cluster.

##### Verify the Replication Configuration

Verify the replication configuration using `riak repl status` on both a
Cluster1 node and a Cluster2 node. A full description of the `riak repl
status` command's output can be found in the documentation for
`riak repl`'s [status output][cluster ops v2 mdc#status].

On the Cluster1 node, verify that there are `listener_<nodename>`s for
each listening node, and that `leader` and `server_stats` are populated.
They should look similar to the following:

```
listener_riak@172.16.1.11: "172.16.1.11:9010"
listener_riak@172.16.1.12: "172.16.1.12:9010"
listener_riak@172.16.1.13: "172.16.1.13:9010"
leader: 'riak@172.16.1.11'
server_stats: [{<8051.3939.0>,
               {message_queue_len,0},
               {status,[{site,"Cluster2"},
                        {strategy,riak_repl_keylist_server},
                        {fullsync_worker,<8051.3940.0>},
                        {dropped_count,0},
                        {queue_length,0},
                        {queue_byte_size,0},
                        {state,wait_for_partition}]}}]
```

On the Cluster2 node, verify that `Cluster1_ips`, `leader`, and
`client_stats` are populated. They should look similar to the following:

```
Cluster1_ips: "172.16.1.11:9010, 172.16.1.12:9010, 172.16.1.13:9010"
leader: 'riak@192.168.1.21'
client_stats: [{<8051.3902.0>,
               {message_queue_len,0},
               {status,[{site,"Cluster1"},
                        {strategy,riak_repl_keylist_client},
                        {fullsync_worker,<8051.3909.0>},
                        {put_pool_size,5},
                        {connected,"172.16.1.11",9010},
                        {state,wait_for_fullsync}]}}]
```

##### Testing Realtime Replication

That's all there is to it! When `PUT` requests are coordinated by
Cluster1, these operations will be replicated to Cluster2.

You can use the following example script to verify that `PUT` operations
sent to Cluster1 are being replicated to Cluster2:

```bash
#!/bin/bash

VALUE=`date`
CLUSTER_1_IP=172.16.1.11
CLUSTER_2_IP=192.168.1.21

curl -s -X PUT -d "${VALUE}" http://${CLUSTER_1_IP}:8098/riak/replCheck/c1

CHECKPUT_C1=`curl -s http://${CLUSTER_1_IP}:8098/riak/replCheck/c1`

if [ "${VALUE}" = "${CHECKPUT_C1}" ]; then
  echo "C1 PUT Successful"
else
  echo "C1 PUT Failed"
  exit 1
fi

CHECKREPL_C1_TO_C2=`curl -s http://${CLUSTER_2_IP}:8098/riak/replCheck/c1`

if [ "${VALUE}" = "${CHECKREPL_C1_TO_C2}" ]; then
  echo "C1 to C2 consistent"
else
  echo "C1 to C2 inconsistent
        C1:${CHECKPUT_C1}
        C2:${CHECKREPL_C1_TO_C2}"
  exit 1
fi

exit 0
```

You will have to change some of the above variables for your own
environment, such as IP addresses or ports.

If you run this script and things are working as expected, you will get
the following output:

```
C1 PUT Successful
C1 to C2 consistent
```

#### Set Up Cluster2 &rarr; Cluster1 Replication

##### About Bidirectional Replication

Multi-Datacenter support can also be configured to replicate in both
directions, ensuring eventual consistency between your two datacenters.
Setting up bidirectional replication is as simple as repeating the steps
above in the other direction, i.e. from Cluster2 to Cluster1.

##### Set Up the Listeners on Cluster2 (Source cluster)

On a node in Cluster2, `node4` for example, identify the nodes that will
be listening to connections from replication clients with `riak repl
add-listener <nodename> <listen_ip> <port>` for each node that will be
listening for replication clients.

```bash
riak repl add-listener riak@192.168.1.21 192.168.1.21 9010
riak repl add-listener riak@192.168.1.22 192.168.1.22 9010
riak repl add-listener riak@192.168.1.23 192.168.1.23 9010
```

##### Set Up the Site on Cluster1 (Site cluster)

On a node in Cluster1, `node1` for example, inform the replication
clients where the Source Listeners are with `riak repl add-site <ipaddr>
<port> <sitename>`. Use the IP address(es) and port(s) you configured in
the earlier step. For `sitename` enter **Cluster2**.

```bash
riak repl add-site 192.168.1.21 9010 Cluster2
```

Verify the replication configuration using `riak repl status` on a
Cluster1 node and a Cluster2 node. A full description of the `riak repl
status` command's output can be found in the documentation for
`riak repl`'s [status output][cluster ops v2 mdc#status].

On the Cluster1 node, verify that `Cluster2_ips`, `leader`, and
`client_stats` are populated. They should look similar to the following:

```
Cluster2_ips: "192.168.1.21:9010, 192.168.1.22:9010, 192.168.1.23:9010"
leader: 'riak@172.16.1.11'
client_stats: [{<8051.3902.0>,
               {message_queue_len,0},
               {status,[{site,"Cluster2"},
                        {strategy,riak_repl_keylist_client},
                        {fullsync_worker,<8051.3909.0>},
                        {put_pool_size,5},
                        {connected,"192.168.1.21",9010},
                        {state,wait_for_fullsync}]}}]
```

On the Cluster2 node, verify that there are listener entries for each
listening node, and that `leader` and `server_stats` are populated. They
should look similar to the following:

```
listener_riak@192.168.1.21: "192.168.1.21:9010"
listener_riak@192.168.1.22: "192.168.1.22:9010"
listener_riak@192.168.1.23: "192.168.1.23:9010"
leader: 'riak@192.168.1.21'
server_stats: [{<8051.3939.0>,
               {message_queue_len,0},
               {status,[{site,"Cluster1"},
                        {strategy,riak_repl_keylist_server},
                        {fullsync_worker,<8051.3940.0>},
                        {dropped_count,0},
                        {queue_length,0},
                        {queue_byte_size,0},
                        {state,wait_for_partition}]}}]
```

You can use the following script to perform `PUT`s and `GET`s on both
sides of the replication and verify that those changes are replicated to
the other side.

```bash
#!/bin/bash

curl -s -X PUT -d "${VALUE}" http://${CLUSTER_2_IP}:8098/riak/replCheck/c2
CHECKPUT_C2=`curl -s http://${CLUSTER_2_IP}:8098/riak/replCheck/c2`

if [ "${VALUE}" = "${CHECKPUT_C2}" ]; then
  echo "C2 PUT Successful"
else
  echo "C2 PUT Failed"
  exit 1
fi

CHECKREPL_C1_TO_C2=`curl -s http://${CLUSTER_2_IP}:8098/riak/replCheck/c1`
CHECKREPL_C2_TO_C1=`curl -s http://${CLUSTER_1_IP}:8098/riak/replCheck/c2`

if [ "${VALUE}" = "${CHECKREPL_C2_TO_C1}" ]; then
  echo "C2 to C1 consistent"
else
  echo "C2 to C1 inconsistent
      C2:${CHECKPUT_C2}
      C1:${CHECKREPL_C2_TO_C1}"
  exit 1
fi

exit 0
```

```
C1 PUT Successful
C2 PUT Successful
C1 to C2 consistent
C2 to C1 consistent
```

#### Fullsync

During realtime replication, operations coordinated by the Source
cluster will be replicated to the Site cluster. Riak Objects are placed
in a queue on the Source cluster and streamed to the Site cluster. When
the queue is full due to high traffic or a bulk loading operation, some
objects will be dropped from replication. These dropped objects can be
sent to the Site cluster by running a fullsync operation. The settings
for the realtime replication queue and their explanations are available
in the [configuration][config v2 mdc] documentation.

##### Initiating a fullsync

To start a fullsync operation, issue the following command on your
leader node:

```bash
riak repl start-fullsync
```

A fullsync operation may also be cancelled. If a partition is in
progress, synchronization will stop after that partition completes.
During cancellation, `riak repl status` will show 'cancelled' in the
status.

```bash
riak repl cancel-fullsync
```

Fullsync operations may also be paused, resumed, or scheduled for
certain times using cron jobs. A complete list of fullsync commands is
available in the [MDC Operations][cluster ops v2 mdc] documentation.

### Quickstart

[perf index]: {{< product-version-root >}}how-to/tune/
[config v3 mdc]: {{< product-version-root >}}how-to/configure/replication/configure-v3-multi-datacenter/
[cluster ops v3 mdc]: {{< product-version-root >}}reference/replication-api/runtime-controls/

This guide will walk you through the process of configuring OpenRiak's v3
Replication to perform replication between two sample Riak clusters on
separate networks. This guide will also cover bidirectional replication,
which is accomplished by setting up unidirectional replication in both
directions between the clusters.  It is important to note that both
clusters must have the same ring size, but can have a different number
of nodes.

#### Prerequisites

* Install [Riak][install index]
* Perform [System Tuning][perf index]
* Review [Configuration][config v3 mdc]

#### About v3 Replication in 1.3 and higher

In OpenRiak's v3 Replication from OpenRiak KV version 1.3 onwards, the nomenclature for Source and Site
clusters has changed. To more accurately reflect the behavior of each of
the clusters, "listeners" and "sites" are now known as "sources" and
"sinks." Data transfer now originates at the "source" and replicates to
the "sink;" initiation is always from the primary (source) to the backup
(sink) data center.

Additionally, knowledge of the state of each cluster is now managed by a
**cluster manager** process, which greatly simplifies the setup and
maintenance of Multi-Datacenter replication.

#### Scenario

Configure Riak MDC to perform replication, given the following two
Riak Clusters, each of which consists of three nodes:

##### Cluster 1

Name  | IP          | Node name
:-----|:-------------|-----------------
`node1` | `10.60.67.149` | `riak@10.60.67.149`
`node2` | `10.60.83.39`  | `riak@10.60.83.39`
`node3` | `10.60.90.252` | `riak@10.60.90.252`

##### Cluster 2

Name  | IP          | Node name
:-----|:------------|:----------------
`node4` | `10.60.77.10` | `riak@10.60.77.10`
`node5` | `10.60.84.41` | `riak@10.60.84.41`
`node6` | `10.60.92.44` | `riak@10.60.92.44`

##### Set up Cluster1 &rarr; Cluster2 Connection

###### Set up the Source on Cluster1

On a node in Cluster1, `node1` for example, initiate and name this
cluster with `riak repl clustername <name>`:

```bash
riak repl clustername Cluster1
```

###### Setup the Sink on Cluster2

On a node in Cluster2, `node4` for example, initiation and name this
cluster with `riak repl clustername <name>`:

```bash
riak repl clustername Cluster2
```

###### Connect the Source to the Sink

From Cluster1, connect to the IP and port of Cluster2 with `riak repl
connect <sink_ip>:<port>`:

```bash
riak repl connect 10.60.77.10:9080
```

> The port can be found in the `riak_core` section of the `advanced.config`
> under `cluster_mgr`.

###### View your active connections

From Cluster1, view your active connections with `riak repl
connections`:

```
Sink             Cluster Name         <Ctrl-Pid>      [Members]
----             ------------         ----------      ---------
Cluster2          Cluster2            <0.7985.0>      ["10.60.77.10:9080"] (via 10.60.77.10:9080)
```

##### Set up Cluster2 &rarr; Cluster1 Connection (if bidirectional replication is desired)

From Cluster2, connect to the IP and port of Cluster1 with `riak repl
connect <sink_ip>:<port>`:

```bash
riak repl connect 10.60.67.149:9080
```

From Cluster2, view your active connections with `riak repl
connections`:

```
Sink             Cluster Name         <Ctrl-Pid>      [Members]
----             ------------         ----------      ---------
Cluster1          Cluster1            <0.4456.0>      ["10.60.67.149:9080"] (via 10.60.67.149:9080)
```

**Note on connections**
At this point, if you do not have connections, replication will not work.
Check your IP bindings by running `netstat -a` on all nodes. You should see
`*:9080 LISTENING`. If not, you have configuration problems.

##### Enable Realtime Replication

From Cluster1, run `riak repl realtime enable <clustername>` to start
queuing updates on Cluster1 for replication:

```bash
riak repl realtime enable Cluster2
```

Also on Cluster1, run `riak repl realtime start <clustername>` to
establish connectivity from Cluster1 to Cluster2 to push queued updates:

```bash
riak repl realtime start Cluster2
```

To enable bidirectional replication, do the reverse from Cluster2.
Once this is done, bidirectional replication should be operating.

#### More information

For a full list of commands, you may enter `riak repl` to see full
instructions on usage, or check the [Operations][cluster ops v3 mdc] documentation.

[assumptions]: {{< product-version-root >}}tutorials/replication/two-cluster-replication/
[design]: {{< product-version-root >}}tutorials/replication/two-cluster-replication/
[installingg]: {{< product-version-root >}}tutorials/replication/two-cluster-replication/

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.

## Next steps

- Continue with the section index and choose the next task for your role.
