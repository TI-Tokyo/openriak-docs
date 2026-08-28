---
title: 'Replication runtime control reference'
description: 'List supported source, sink, queue, reconciliation, range, and resynchronization controls.'
weight: 2
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\v2-multi-datacenter.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\v3-multi-datacenter.md'
  - 'Legacy multi-datacenter replication terminology and commands require compatibility review.'
source_material:
  - 'legacy-3.2.5'
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#configure-and-monitor-work-queues'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#making-runtime-changes-to-the-sink'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#making-runtime-changes-to-the-source'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#monitoring-and-runtime-changes'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#overriding-the-range'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#participate-in-coverage'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#prompting-a-reconciliation-check'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#re-sync-a-bucket'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#suspend-full-sync'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#trigger-tree-repairs'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#tuning-checks---the-maximum-results-limit'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#update-the-request-limits'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

List supported source, sink, queue, reconciliation, range, and resynchronization controls.

## Details

### Replication Operations

**Deprecation Warning**
v2 Multi-Datacenter Replication is deprecated and will be removed in a future version. Please use [v3]({{< baseurl >}}kv/3.4.1/reference/replication-api/runtime-controls/) instead.

OpenRiak's Multi-Datacenter Replication system is largely
controlled by the `riak repl` command. The sections below detail the
available subcommands.

#### add-listener

Adds a listener (primary) to the given node, IP address, and port.

```bash
riak repl add-listener <nodename> <listen_ip> <port>
```

Below is an example usage:

```bash
riak repl add-listener riak@10.0.1.156 10.0.1.156 9010
```

#### add-nat-listener

Adds a NAT-aware listener (primary) to the given node, IP address, port,
NAT IP, and NAT port. If a non-NAT listener already exists with the same
internal IP and port, it is "upgraded” to a NAT Listener.

```bash
riak repl add-nat-listener <nodename> <internal_ip> <internal_port> <nat_ip> <nat_port>
```

```bash
riak repl add-nat-listener riak@10.0.1.156 10.0.1.156 9010 50.16.238.123 9010
```

#### del-listener

Removes and shuts down a listener (primary) on the given node, IP
address, and port.

```bash
riak repl del-listener <nodename> <listen_ip> <port>
```

```bash
riak repl del-listener riak@10.0.1.156 10.0.1.156 9010
```

#### add-site

Adds a site (secondary) to the local node, connecting to the specified
listener.

```bash
riak repl add-site <ipaddr> <portnum> <sitename>
```

```bash
riak repl add-site 10.0.1.156 9010 newyork
```

#### del-site

Removes a site (secondary) from the local node by name.

```bash
riak repl del-site <sitename>
```

```bash
riak repl del-site newyork
```

#### status

Obtains status information about replication. Reports counts on how much
data has been transmitted, transfer rates, message queue lengths of
clients and servers, number of fullsync operations, and connection
status. This command only displays useful information on the leader
node.

```bash
riak repl status
```

#### start-fullsync

Manually initiates a fullsync operation with connected sites.

```bash
riak repl start-fullsync
```

#### cancel-fullsync

Cancels any fullsync operations in progress. If a partition is in
progress, synchronization will stop after that partition completes.
During cancellation, `riak repl status` will show `cancelled` in the
status.

```bash
riak repl cancel-fullsync
```

#### pause-fullsync

Pauses any fullsync operations in progress. If a partition is in
progress, synchronization will pause after that partition completes.
While paused, `riak repl status` will show `paused` in the status
information. Fullsync may be cancelled while paused.

```bash
riak repl pause-fullsync
```

#### resume-fullsync

Resumes any fullsync operations that were paused. If a fullsync
operation was running at the time of the pause, the next partition will
be synchronized. If not, it will wait until the next `start-fullsync`
command or `fullsync_interval`.

```bash
riak repl resume-fullsync
```

#### riak repl Status Output

The following definitions describe the output of the `riak repl status`
command. Please note that many of these statistics will only appear on
the current leader node, and that all counts will be reset to 0 upon
restarting Riak.

##### Client

Field | Description
:-----|:-----------
`client_stats` | See <a href="{{< baseurl >}}kv/3.4.1/reference/operations/replication-statistics/#client-statistics">Client Statistics</a>
`client_bytes_recv` | The total number of bytes the client has received since the server has been started
`client_bytes_sent` | The total number of bytes sent to all connected sites
`client_connect_errors` | The number of TCP/IP connection errors
`client_connects` | A count of the number of site connections made to this node
`client_redirect` | If a client connects to a non-leader node, it will be redirected to a leader node
`client_rx_kbps` | A snapshot of the client (site)-received kilobits/second taken once a minute. The past 8 snapshots are stored in this list. Newest snapshots appear on the left side of the list.
`client_tx_kbps` | A snapshot of the client (site)-sent kilobits/second taken once a minute. The past 8 snapshots are stored in this list. Newest snapshots appear on the left side of the list.

##### Server

Field | Description
:-----|:-----------
`server_bytes_recv` | The total number of bytes the server (listener) has received
`server_bytes_sent` | The total number of bytes the server (listener) has sent
`server_connect_errors` | The number of listener to site connection errors
`server_connects` | The number of times the listener connects to the client site
`server_fullsyncs` | The number of fullsync operations that have occurred since the server was started
`server_rx_kbps` | A snapshot of the server (listener) received kilobits/second taken once a minute. The past 8 snapshots are stored in this list. Newest snapshots appear on the left side of the list.
`server_tx_kbps` | A snapshot of the server (listener) sent kilobits/second taken once a minute. The past 8 snapshots are stored in this list. Newest snapshots appear on the left side of the list.
`server_stats` | See <a href="{{< baseurl >}}kv/3.4.1/reference/operations/replication-statistics/#server-statistics">Server Statistics</a>

##### Elections and Objects

Field | Description
:-----|:-----------
`elections_elected` | If the replication leader node becomes unresponsive or unavailable, a new leader node in the cluster will be elected
`elections_leader_changed` | The number of times an OpenRiak node has surrendered leadership
`objects_dropped_no_clients` | If the realtime replication work queue is full and there aren't any clients to receive objects, then objects will be dropped from the queue. These objects will be synchronized during a fullsync operation.
`objects_dropped_no_leader` | If a client (site) cannot connect to a leader, objects will be dropped during realtime replication
`objects_forwarded` | The number of Riak objects forwarded to the leader the participate in replication. *Please note that this value will only be accurate on a non-leader node*.
`objects_sent` | The number of objects sent via realtime replication

##### Other

Field | Description
:-----|:-----------
`listener_<nodeid>` | Defines a replication listener that is running on node `<nodeid>`
`[sitename]_ips` | Defines a replication site
`leader` | Which node is the current leader of the cluster
`local_leader_message_queue_len` | The length of the object queue on the leader
`local_leader_heap_size `| The amount of memory the leader is using

#### Client Statistics

Field | Description
------|------------
`node` | A unique ID for the OpenRiak node on which the client (site) is running
`site` | The connected site name configured with `riak repl add-site`
`strategy` | A replication strategy defines an implementation of the Riak Replication protocol. Valid values: `keylist`, `syncv1`
`fullsync_worker` | The Erlang process ID of the fullsync worker
`waiting_to_retry` | The listeners currently waiting to retry replication after a failure
`connected` | A list of connected clients<ul><li>`connected` - The IP address and port of a connected client (site)</li><li>`cluster_name` - The name of the connected client (site)</li><li>`connecting` - The PID, IP address, and port of a client currently establishing a connection</li></ul>
`state` | State shows what the current replication strategy is currently processing. The following definitions appear in the status output if keylist strategy is being used. They can be used by Basho support to identify replication issues.<ul><li>`request_partition`</li><li>`wait_for_fullsync`</li><li>`send_keylist`</li><li>`wait_ack`</li></ul>

#### Bounded Queue

The bounded queue is responsible for holding objects that are waiting to
participate in realtime replication. Please see the [Riak MDC Replication Configuration]({{< baseurl >}}kv/3.4.1/how-to/configure/replication/configure-v2-multi-datacenter/) guide for more information.

Field | Description
------|------------
`queue_pid` | The Erlang process ID of the bounded queue
`dropped_count` | The number of objects that failed to be enqueued in the bounded queue due to the queue being full. *These objects will be replicated during the next fullsync operation*.
`queue_length` | The number of Riak objects currently in the bounded queue
`queue_byte_size` | The size of all objects currently in the queue
`queue_max_size` | The number of bytes the queue can hold before objects are dropped. *These objects will be replicated during the next fullsync operation*.
`queue_percentage` | The percentage of the queue that is full
`queue_pending` | The current count of "in-flight" objects we've sent that the client has not acknowledged
`queue_max_pending` | The maximum number of objects that can be "in flight" before we refuse to send any more.

#### Server Statistics

Field | Description
------|------------
`node`  | A unique ID for the OpenRiak node on which the server (listener) is running
`site` | The connected site name configured with `riak repl add-site`
`strategy` | A replication strategy defines an implementation of the Riak Replication protocol. Valid values: `keylist` or `syncv1`.
`fullsync_worker` | The Erlang process ID of the fullsync worker
`bounded_queue` | See the <a href="{{< baseurl >}}kv/3.4.1/reference/replication-api/runtime-controls/#bounded-queue">Bounded Queue</a> section above
`state` | State shows what the current replication strategy is processing. The following definitions appear in the status output if the keylist strategy is being used. They can be used by Basho support to identify replication issues.<ul><li>`wait_for_partition`</li><li>`build_keylist`</li><li>`wait_keylist`</li><li>`diff_bloom`</li><li>`diff_keylist`</li></ul>s
`message_queue_len` | The number of Erlang messages that are waiting to be processed by the server

#### Keylist Strategy

These similar fields are under both the `keylist_server` and
`keylist_client` fields. Any differences are described in the table.

Field | Description
------|------------
`fullsync` | On the client, the number of partitions that remain to be processed. On the server, the partition currently being processed by fullsync replication.
`partition_start` | The number of elapsed seconds since replication has started on a given partition
`stage_start` | The number of elapsed seconds since replication has started on a given stage
`get_pool_size` | The number of Riak get finite state workers available to process requests

[config v3 mdc]: {{< baseurl >}}kv/3.4.1/how-to/configure/replication/configure-v3-multi-datacenter/
[config v3 nat]: {{< baseurl >}}kv/3.4.1/how-to/configure/replication/configure-replication-through-nat/
[config v3 quickstart]: {{< baseurl >}}kv/3.4.1/tutorials/replication/two-cluster-replication/
[config v3 ssl]: {{< baseurl >}}kv/3.4.1/how-to/configure/replication/secure-replication/
[ref v3 stats]: {{< baseurl >}}kv/3.4.1/reference/operations/replication-statistics/

This document explains how to manage replication with the `riak repl`
command. Some of these commands can be set or behavior altered by
setting appropriate [configuration][config v3 mdc] values.

All commands need to be run only once on a single node of a cluster for
the changes to propagate to all other nodes. All changes will persist
across node restarts and will automatically take effect when nodes are
added to the cluster.

#### Cluster Connectivity

##### clustername

Set the `clustername` for all nodes in an OpenRiak cluster.

* Without a parameter, returns the current name of the cluster
* With a parameter, names the current cluster

To **set** the `clustername`:

* Syntax: `riak repl clustername <clustername>`
* Example: `riak repl clustername Boston`

To **get** the `clustername`:

* Syntax: `riak repl clustername`
* Example: `riak repl clustername`

###### connect

The `connect` command establishes communications from a source cluster
to a sink cluster of the same ring size. The `host:port` of the sink
cluster is used for this. The IP and port to connect to can be found in
the `advanced.config` of the remote cluster, under `riak_core` and
`cluster_mgr`.

The `host` can be either an IP address

* Syntax: `riak repl connect <ip>:<port>`
* Example: `riak repl connect 192.168.2.1:9080`

...or a hostname that will resolve to an IP address.

* Syntax: `riak repl connect <host>:<port>`
* Example: `riak repl connect Austin:9080`

###### disconnect

Disconnecting a source cluster from a sink cluster.

You may define a `host:port` combination

* Syntax: `riak repl disconnect <host>:<port>`
* Example: `riak repl disconnect 192.168.2.1:9080`

...or use the *name* of the cluster.

* Syntax: `riak repl disconnect <sink_clustername>`
* Example: `riak repl disconnect Austin`

###### connections

Display a list of connections between source and sink clusters.

* Syntax: `riak repl connections`
* Example: `riak repl connections`

###### clusterstats

Displays current cluster stats using an optional `ip:port` as well as an
optional `protocol-id`.

`protocol-id` can be one of the following:

* `cluster_mgr`
* `rt_repl`
* `fs_repl`

The `clusterstats` command in use:

* Syntax: `riak repl clusterstats <host>:<port> <protocol-id>`
* Example: `riak repl clusterstats 192.168.2.1:9080`
* Example: `riak repl clusterstats 192.168.2.1:9080 fs_repl`

#### Realtime Replication Commands

##### realtime enable

Enable realtime replication from a source cluster to sink clusters.

This will start queuing updates for replication. The cluster will still
require an invocation of `realtime start` for replication to occur.

* Syntax: `riak repl realtime enable <sink_clustername>`
* Example: `riak repl realtime enable Austin`

###### realtime disable

Disable realtime replication from a source cluster to sink clusters.

* Syntax: `riak repl realtime disable <sink_clustername>`
* Example: `riak repl realtime disable Austin`

###### realtime start

Start realtime replication connections from a source cluster to sink
clusters. See also `realtime enable` (above).

* Syntax: `riak repl realtime start <sink_clustername>`
* Example: `riak repl realtime start Austin`

###### realtime stop

Stop realtime replication from a source cluster to sink clusters.

* Syntax `riak repl realtime stop <sink_clustername>`
* Example `riak repl realtime stop Austin`

#### Fullsync Replication Commands

These behaviors can be altered by using the `advanced.config`
`fullsync_on_connect` parameter. See the [Configuration Guide][config v3 mdc] for more information.

##### fullsync enable

Enable fullsync replication from a source cluster to sink clusters. By
default, a fullsync will begin as soon as a connection to the remote
cluster is established.

* Syntax: `riak repl fullsync enable <sink_clustername>`
* Example: `riak repl fullsync enable Austin`

###### fullsync disable

Disables fullsync for a cluster.

* Syntax: `riak repl fullsync disable <sink_clustername>`
* Example: `riak repl fullsync disable Austin`

###### fullsync start

Starts a fullsync. If the application configuration
`fullsync_on_connect` is set to `false`, a fullsync needs to be started
manually. This is also used to trigger a periodic fullsync using a cron
job. While a fullsync is in progress, a `start` command is ignored and a
message is logged.

* Syntax: `riak repl fullsync start <sink_clustername>`
* Example: `riak repl fullsync start Austin`

###### fullsync stop

Stops a fullsync.

* Syntax: `riak repl fullsync stop <sink_clustername>`
* Example: `riak repl fullsync stop Austin`

#### Cascading Realtime Writes

##### realtime cascades

Shows the current cascading realtime setting.

* Syntax: `realtime cascades`
* Example: `riak repl realtime cascades`

###### realtime cascades always

Enable realtime cascading writes.

* Syntax: `realtime cascades always`
* Example: `riak repl realtime cascades always`

###### realtime cascades never

Disable realtime cascading writes.

* Syntax: `realtime cascades never`
* Example: `riak repl realtime cascades never`

#### NAT

**Note**: See the [V3 Multi Data Center Replication With NAT][config v3 nat] for more information.

##### nat-map show

Show the current NAT mapping table.

* Syntax: `nat-map show`
* Example: `riak repl nat-map show`

###### nat-map add

Adds a NAT map from the external IP, with an optional port, to an
internal IP.

* Syntax: `nat-map add <externalip>[:port] <internalip>`
* Example: `riak repl nat-map add 128.205.106.1:5555 192.168.1.2`

###### nat-map del

Deletes a specific NAT map entry.

* Syntax: `nat-map del <externalip>[:port] <internalip>`
* Example: `riak repl nat-map del 128.205.106.1:5555 192.168.1.2`

NAT changes will be applied once fullsync and/or realtime replication
has been stopped and started.

#### Riak CS MDC Gets

##### proxy-get enable

Enable Riak CS `proxy_get` requests from a **sink** cluster (if
`proxy_get` has been enabled in `advanced.config`).

* Syntax: `proxy-get enable  <sink_clustername>`
* Example: `riak repl proxy-get enable  newyorkbackup`

###### `proxy-get disable`

Disable Riak CS `proxy_get` requests from a **sink** cluster (if
`proxy_get` has been enabled in `advanced.config`).

* Syntax: `proxy-get disable <sink_clustername>`
* Example: `riak repl proxy-get disable newyorkbackup`

###### `add-block-provider-redirect`

Provide a redirection to the `<to-cluster-id>` for `proxy_get` if the
`<from-cluster>` is going to be decommissioned.

* Syntax: `riak repl add-block-provider-redirect <from-cluster> <to-cluster>`
* Example: `riak repl add-block-provider-redirect "{'dev1@127.0.0.1',{1391,544501,519016}}" "{'dev3@127.0.0.1',{1299,512501,511032}}"`

###### `show-block-provider-redirect`

Show the mapping for a given cluster-id redirect.

* Syntax: `riak repl show-block-provider-redirect <from-cluster>`
* Example: `riak repl show-block-provider-redirect "{'dev1@127.0.0.1',{1391,544501,519016}}"`

###### `delete-block-provider-redirect`

Delete a existing redirect such that proxy_gets go again to the original
provider cluster id.

* Syntax:* `riak repl delete-block-provider-redirect <from-cluster>`
* Example:* `riak repl delete-block-provider-redirect "{'dev1@127.0.0.1', {1391,544501,519016}}"`

###### `show-local-cluster-id`

Display this cluster's cluster-id tuple, for use with the
`*-block-provider-redirect` commands.

**Note**: A cluster-id is surrounded by double quotes, which need to be
included when passed to `*-block-provider-redirect`.

* Syntax: `riak repl show-local-cluster-id`
* Example:

```bash
    riak repl show-local-cluster-id
    ```

Possible output:

```
    local cluster id: "{'dev1@127.0.0.1',{1391,544501,519016}}"
    ```

#### `riak repl` Status Output

Details about the `riak repl status` command can be found under
[Statistics][ref v3 stats].

#### Tuning

These tuning values may also be set via the node's `advanced.config` file.
See the [Configuration Guide][config v3 mdc] for more information.

##### `fullsync max_fssource_node`

This limits the number of fullsync workers that will be running on each
individual node in a source cluster. This is a hard limit for *all*
fullsyncs that are enabled. Additional fullsync configurations will
*not* increase the number of fullsync workers allowed to run on any
node. This only affects nodes on the source cluster on which this
parameter is defined via the configuration file or command line.

* Syntax: `riak repl fullsync max_fssource_node <value>`
* Default: `1`
* Example: `riak repl fullsync max_fssource_node 2`

###### `fullsync max_fssource_cluster`

This is the hard limit of fullsync workers that will be running on the
source side of a cluster across all nodes on that cluster for a fullsync
to a sink cluster. This means if one has configured fullsync for two
different clusters, both with a max_fssource_cluster of 5, 10 fullsync
workers can be in progress. Only affects nodes on the source cluster on
which this parameter is defined via the configuration file or the
command line.

* Syntax: `riak repl fullsync max_fssource_cluster <value>`
* Default: `5`
* Example: `riak repl fullsync max_fssource_cluster 5`

###### `fullsync max_fssink_node`

This limits the number of fullsync workers allowed to run on each
individual node in a sink cluster. This is a hard limit for each
fullsync source node interacting with a sink node. Thus, multiple
simultaneous source connections to a sink node will have to share the
sink node’s number of maximum connections. Only affects nodes on the
sink cluster on which this parameter is defined via the configuration
file or command line.

* Syntax: `riak repl fullsync max_fssink_node <value>`
* Default: `1`
* Example: `riak repl fullsync max_fssink_node 5`

#### Mixing Version 2 Replication with Version 3 Replication

Riak Version 2 Replication and Version 3 Replication can be safely used
at the same time. If you choose to move to Version 3 Replication
completely, we recommend disabling Version 2 realtime
replication bucket hooks with the `riak repl modes` command.

##### `riak repl modes`

`modelist` is one or both of `mode_repl12` (Version 2) or `mode_repl13`
(Version 3) separated by spaces (without commas).

* Syntax: `riak repl modes <modelist>`
* Example:

```bash
    riak repl modes mode_repl12 mode_repl13
    ```

Possible output:

```
    Current replication modes: [mode_repl12,mode_repl13]
    ```

To check the current replication modes:

* Syntax: `riak repl modes`
* Example:

```bash
    riak repl modes
    ```

Possible output:

#### Configurations and Metadata in Replication

Fullsync and Realtime replication replicates data from source clusters to sink clusters,
but some configurations and metadata (such as bucket properties) will
not be replicated.

Non-replication of certain configurations and metadata supports
heterogenous cluster configurations in Replication, but there operational things you can
do when you want homogeneous cluster configurations.

##### Buckets and Bucket Types in Replication

Buckets and Bucket Type properties on the source cluster
will _not_ be replicated from source clusters to sink clusters.

If you want the properties for Buckets or Bucket Types
present on the source cluster to be propagated to sink clusters
you should update this data for each cluster at the same
time you would change the source cluster.

#### Tuning checks - the maximum results limit

With o(10bn) keys in a cluster, there are 10K keys and clocks to be compared for every segment ID with a delta.  To reduce the cost of fetching and comparing keys in the `clock_compare` stage, the number of segments to be compared each loop is constrained by a maximum results limit.  This maximum results list is used at all phases of the exchange to reduce the scope of comparisons.  The maximum results limit is calculated from:

- `ttaaefs_maxresults = <max_results>`;
  - The number of segments to be compared each loop.
- `ttaaefs_rangeboost = <multiplier>`;
  - A multiplier applied to the `ttaaefs_maxresults` when a `ttaaefs_rangecheck` is used.
  - The product of `ttaaefs_maxresults` and `ttaaefs_rangeboost` should not exceed 1024.  Larger values will work, but not necessarily be efficient.

It is important that when a delta is being resolved, the comparison queries can complete in the time slot for the check.  If they do not complete, checks will begin to overlap and queue, and this will lead to checks being dropped and also the waste of compute resources; a timed out exchange will not be able to prompt repairs even though the fold operations may have continued through to completion.

The speed of checks are recorded in logs, and can be tested manually with different numbers of segment IDs using the [AAE fold `fetch_clocks_nval`]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/).  The speed of folds using segment IDs are improved if the segment IDs are in a smaller range (i.e. are numerically close together), and the AAE exchange will attempt to exploit this efficiency when selecting a subset of segment IDs.

#### Making runtime changes to the Source

There are four functions on the source that may be [called from the `remote_console`]({{< baseurl >}}kv/3.4.1/how-to/operate/use-remote-console/).  To suspend and resume a queue:

```erlang
riak_kv_replrtq_src:suspend_rtq(QueueName).
```

```erlang
riak_kv_replrtq_src:resume_rtq(QueueName).
```

To check the length of the queue, and if necessary clear the queue (for example if a mistaken `repl_keys_range` fold has been prompted):

```erlang
riak_kv_replrtq_src:length_rtq(QueueName).
```

```erlang
riak_kv_replrtq_src:clear_rtq(QueueName).
```

> Clearing a queue will clear all entries from the queue, regardless of priority.

#### Making runtime changes to the Sink

More workers and sink peers can be added at [runtime via the `remote_console`]({{< baseurl >}}kv/3.4.1/how-to/operate/use-remote-console/), by resetting the worker counts.  This reset is a cluster-wide change, not just a change on the local node:

```erlang
riak_client:replrtq_reset_all_workercounts(WorkerCount, PerPeerLimit)
```

To force peer discovery to immediately update the list of peers on a sink node (this is a node-specific not cluster-wide change):

```erlang
riak_client:replrtq_reset_all_peers(QueueName)
```

When introducing a new node to a sink cluster, if the new node is configured as a sink node it will begin to consume changes from the source as soon as the node has started - which may be prior to joining the cluster.  This will cause a temporary loss of in-sync state for inter-cluster reconciliation.  It is possible to suspend and resume a node from acting as a sink using:

```erlang
riak_kv_replrtq_snk:suspend_snkqueue(QueueName)
```

```erlang
riak_kv_replrtq_snk:resume_snkqueue(QueueName)
```

> Riak will always be eventually consistent, any changes consumed by a sink node prior to joining will be transferred as part of the join; otherwise the reconciliation process will repair any deltas.

#### Prompting a reconciliation check

Individual full-syncs between clusters can be triggered outside the standard schedule:

```erlang
riak_client:ttaaefs_fullsync(all_check).
```

The `all_check` can be replaced with `hour_check`, `day_check` or `range_check` as required.  The request will use the standard max_results and range_boost for the node.

#### Configure and monitor work queues

The node worker pool configuration is [detailed further in the AAE fold API documentation]({{< baseurl >}}kv/3.4.1/how-to/operate/monitor-worker-pools/).

There are two per-node worker pool sizes which have particular relevance to full-sync: `af1_worker_pool_size = <size>`; `af3_worker_pool_size = <size>`.

The AF1 pool is used for rebuilds of the AAE tree cache, and the AF3 pool is used for key/clock fetches when using cluster-wide reconciliation.

If the full-sync processes are taking too long (perhaps as max_results or range_boost are set too aggressively) then the worker pools may backup.  At some stage there may develop a situation where all full-sync queries will time out as the queries will take too long to reach the front of the queue, and hence all the effort associated with the queries will be wasted.

By default there is a log prompted for every aae_fold on completion (all full-sync activity depends on aae_folds prompted on both the source and sink).  For more information on monitoring node worker pools [refer to the Operations guide]({{< baseurl >}}kv/3.4.1/how-to/operate/monitor-worker-pools/).

#### Update the request limits

If there is sufficient capacity to resolve a delta between clusters, but the current schedule is taking too long to resolve - the max_results and range_boost settings on a given node can be overridden.

```erlang
application:set_env(riak_kv, ttaaefs_maxresults, 64).
application:set_env(riak_kv, ttaaefs_rangeboost, 16).
```

Individual repair queries will do more work as these numbers are increased, but will repair more keys per cycle.  This can be used along with prompted checks (especially range checks) to rapidly resolve a delta.

> If the number of segment IDs being checked goes significantly over one thousand, then the number of blocks that can be skipped will tend towards zero.  So the combined value of `maxresults * rangeboost` should be kept to a value less than or equal to 1024.

#### Overriding the range

When a query successfully repairs a significant number of keys, it will set the range property to guide any future range queries on that node.  This range can be temporarily overridden, if for example, there exists more specific knowledge of what the range should be.  It may also be necessary to override the range when an event erroneously wipes the range (e.g. falling behind in the schedule will remove the range to force range_checks to throttle back their activity).

To override the range (for the duration of one request):

```erlang
riak_kv_ttaaefs_manager:set_range({Bucket, KeyRange, ModifiedRange}).
```

Bucket can be a specific bucket (e.g. `{<<"Type">>, <<"Bucket">>}` or `<<"Bucket">>`) or the keyword `all` to check all buckets (if n_val full-sync is configured for this node). The KeyRange may also be `all` or a tuple of StartKey and EndKey.

To remove the range:

```erlang
riak_kv_ttaaefs_manager:clear_range().
```

Remember the `range_check` queries will only run if either: the last check on the node found the clusters in sync, or; a range has been defined.  Clearing the range may prevent future range_check queries from running until another check re-assigns a range.

#### Re-Sync a Bucket

Full-sync reconciliation is designed to be fast and efficient for confirming that clusters are in sync, but is relatively slow to resolve deltas between clusters.  The common case, when the delta is associated with a recent window of last-modified-dates (e.g. due to a recent temporary failure of replication or nodes) is optimised through the `auto_check` process; and also [re-replication]({{< baseurl >}}kv/3.4.1/how-to/operate/rereplicate-time-window/) may be used to accelerate this.  However, if the delta is not restricted to a given time range of modified dates, and the delta is large, there is a need for alternative intervention to close the delta in a timely manner.

For small buckets (in terms of object count), simply re-replicating the bucket could be the easiest solution, especially where it is clear the replication failure is uni-directional.  For larger buckets, and for handling bi-directional deltas, then it is possible to manually intervene to re-sync a bucket.

The re-sync can be triggered from any node, from either cluster - assuming that bi-directional replication is configured.  The re-sync is cluster-wide, it is not a re-sync of data local to the node. The re-sync can handle, as with other nextgenrepl features, clusters with different configurations (e.g. `n_val` settings).

A bucket re-sync will suspend the local full-sync process on the node from which it is triggered, and roll through segment slices of the bucket performing bucket-specific `range_check` operations.  As each loop covers only a single slice of the segment space, this is much quicker to repair than the standard full-sync per-bucket check, which needs to read the whole bucket space to build AAE trees for comparison.

The re-sync bucket can be called via [remote_console]({{< baseurl >}}kv/3.4.1/how-to/operate/use-remote-console/):

```console
riak_client:resync_bucket({<<"BucketType">>, <<"BucketName">>}).
```

Or, for untyped buckets:

```console
riak_client:resync_bucket(<<"BucketName">>).
```

> In small buckets, of o(10m) keys, it would be normal to have a bucket resync operation repair deltas at a rate exceeding 1,000 per second.

As well as the helper function in `riak_client`, there is a configurable `riak_kv_ttaaefs_manager:resync_bucket/6` function exported.  For much larger buckets, this configurable version can be used to optimise the process e.g. use a smaller width (the size of the slice of the segment space), fix a specific key range or within a modified date range.

> It is possible to have multiple nodes running resync_bucket concurrently - to sync different buckets, or different key ranges within a bucket.  The limiting factor to horizontal scaling of resync_bucket is usually the size of [AF3 worker pool]({{< baseurl >}}kv/3.4.1/how-to/operate/monitor-worker-pools/).  Once all workers in the pool are continuously busy, no further scaling can be achieved, without running larger pools (on all clusters).

#### Participate in Coverage

The full-sync comparisons between clusters are based on coverage plans - a plan which returns a set of vnode to give r=1 coverage of the whole cluster.  When a node is known not to be in a good state (perhaps following a crash), it can be rejoined to the cluster, but made ineligible for coverage plans by using the `participate_in_coverage` configuration option.

This can be useful when tree caches have not been rebuilt after a crash. The `participate_in_coverage` option can also be controlled without a restart via the `riak remote_console`:

```erlang
riak_client:remove_node_from_coverage()
```

```erlang
riak_client:reset_node_for_coverage()
```

The `remove_node_from_coverage` function will drop the local node out of any coverage plans being generated within the cluster (the equivalent of setting participate_in_coverage to false).  The `reset_node_for_coverage` will return the node to its configured setting (in the riak.conf file loaded at start up).

#### Suspend full-sync

If there are issues with full-sync and its resource consumption, it maybe suspended:

```erlang
riak_kv_ttaaefs_manager:pause()
```

when full-sync is ready to be resumed on a node:

```erlang
riak_kv_ttaaefs_manager:resume()
```

These run-time changes are relevant to the local node only and its peer relationships.  The node may still participate in full-sync operations prompted by a remote cluster even when full-sync is paused locally.

When using auto-checks it is also possible to suppress a fixed number of checks.  By default if there are timeouts on queries, the full-sync manager will assume there is excess pressure in the system and enable auto_check_suppress automatically.  This will disable the next two auto-checks.

This can be triggered manually from remote_console `riak_kv_ttaaefs_manager:autocheck_suppress()`.

To change the count of checks for which the suppression is enabled, either alter then environment variable `application:set_env(riak_kv, ttaaefs_autocheck_suppress_count, 4)` or when manually using suppression the count can be specified i.e. `riak_kv_ttaaefs_manager:autocheck_suppress(4)`.

#### Trigger Tree Repairs

When an `all_check` is prompted due to a `{clock_compare, 0}` result, there are two scenarios:

- the cached trees differ but the differences lie outside the previous range;
- the cached trees differ due to a bad tree cache, and there are no actual differences.

For the second case, it is necessary to repair the trees, so when an `all_check` is triggered it will also prompt for trees to be repaired on this node (for the identified mismatched segments only) the next time there is a fetch for keys and clocks.  The triggering should have a log of:

`Setting node to repair trees as unsync'd all_check had no repairs - count of triggered repairs for this node is ~w`

The triggering of tree repairs increases the cost of the fetching of keys and clocks.  Each trigger is coordinated so that it is only fired once and once only (per trigger event) on each vnode.  Usually there is a single vnode with a bad tree cache, but it may take a full cycle of checks for the trigger to be enabled and enacted on the correct node.  This assumes that full-sync reconciliation is bidirectional and configured across all nodes, so eventually each node will see the bad state and trigger the repair mode.  If this isn't the case, manual intervention may be required.

To force a node to enter into the tree repair state, then the following functions can be called via `remote_console`.

```erlang
riak_kv_ttaaefs_manager:trigger_tree_repairs() % Trigger tree repairs on this node
riak_kv_ttaaefs_manager:disable_tree_repairs() % Reverse
```

> The common root cause of bad tree caches, and hence the prompting of tree repairs, is resolved in Riak 3.2.5.  Workarounds to prompt repair remain in place, should other triggers exist.
