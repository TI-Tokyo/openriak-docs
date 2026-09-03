---
title: 'Configure Fullsync replication'
description: 'Show operators how to configure fullsync replication and validate data movement.'
weight: 2
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\replication\fullsync.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\next-gen-replication\fullsync.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\performance\v2-scheduling-fullsync.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v2-multi-datacenter\scheduling-fullsync.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v3-multi-datacenter\scheduling-fullsync.md'
  - 'Legacy multi-datacenter replication terminology and commands require compatibility review.'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#configuration-of-all-cluster-reconciliation'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#enabling-checks'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#initial-configuration'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure fullsync replication and validate data movement.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### FullSync

[configure tictacaae]: {{< product-version-root >}}foundations/replication/tictac-aae/
[configure nextgenrepl fullsync]: ../fullsync/
[configure nextgenrepl realtime]: ../realtime/
[configure nextgenrepl queuing]: {{< product-version-root >}}foundations/replication/queues/

NextGenRepl's FullSync feature provides a considerable improvement over the legacy fullsync engines. It is faster, more efficient, and more reliable. NextGenRepl is the recommended replication engine to use.

FullSync will ensure that the data in the source cluster is also in sink cluster.

**Note:**
NextGenRepl relies on [TicTac AAE]({{< product-version-root >}}foundations/replication/tictac-aae/), so this must be enabled.

#### Overview

NextGenRepl's FullSync works on an automated schedule whereupon a source cluster node checks for changes with a predefined sink cluster node (or load balancer). It then pushes any changes found to a specific preconfigured queue in the queuing system.

A source node can connect to 1 sink node using an IP address or FQDN to check for differences. This can be the IP or FQDN of a load balancer for the sink cluster. Each source node can have the the same FullSync settings as the other source cluster nodes, or entirely different FullSync settings per node if needed.

A source node will sync data from all nodes in the source cluster.

A source node will run FullSync according to the schedule on that specific source node. The source nodes will co-ordinate to ensure that only one FullSync task runs at a time.

If a source node or sink peer is offline for any reason, Riak will wait until the node is repaired before continuing. You should ensure that sufficient redundancies are in place to ensure uptime. This can be done by having multiple source nodes connecting to the same sink cluster, and by using a load balancer in front of the sink cluster.

The number of different clusters you can FullSync to is defined by the number of OpenRiak KV nodes in the source cluster.

**Note:**
Currently all changes listed in this documentation to NextGenRepl must be made by changing the values in the `riak.conf` file.

#### Enable

To turn on FullSync replication, a scope of operation (`ttaaefs_scope`) is needed. The default scope is `disabled` which means that FullSync replication is turned off. The scope can be set to:

- `disabled` - FullSync is disabled
- `all` - all buckets are replicated
- `bucket` - only the specified bucket is replicated
- `type` - only buckets of the specified bucket type are replicated

To FullSync replicate all buckets, use the `ttaaefs_scope` of `any`. For example, to FullSync replicate all buckets, set this value:

```conf {partialname="riak-conf-ttaaefs-scope"}
ttaaefs_scope = all
```

To FullSync replicate using a bucket name filter, use the `ttaaefs_scope` of `bucket` and the `ttaaefs_bucketfilter_name` setting. For example, to only FullSync replicate the bucket "my-bucket-name", set these values:

```conf {partialname="riak-conf-ttaaefs-scope-and-bucketfilter-name"}
ttaaefs_scope = bucket
ttaaefs_bucketfilter_name = my-bucket-name
```

To FullSync replicate all buckets using a bucket type filter, use the `ttaaefs_scope` of `type` and the `ttaaefs_bucketfilter_type` setting. For example, to only FullSync replicate all buckets of bucket type "my-bucket-type", set these values:

```conf {partialname="riak-conf-ttaaefs-scope-and-bucketfilter-type"}
ttaaefs_scope = type
ttaaefs_bucketfilter_type = my-bucket-type
```

#### Queues

FullSync will send all changes from the sink cluster to the queue configured using the `ttaaefs_queuename` setting. The default for this is `q1_ttaaefs`. This can be any queue name, including the same queue name as used by RealTime replication.

For example, to set the FullSync queue name to the default of `q1_ttaaefs`, set `ttaaefs_queuename` like this:

```conf {partialname="riak-conf-ttaaefs-queuename"}
ttaaefs_queuename = q1_ttaaefs
```

##### Bi-directional FullSync

From OpenRiak KV 3.0.10 onwards, it is possible to have the sink cluster also detect changes from the source cluster (bi-directional FullSync) and queue them on the sink clsuter side. This is configured using the `ttaaefs_queuename_peer` setting. The default for this setting is `disabled`.

For example, to set the sink cluster FullSync queue name to the standard name of `q1_ttaaefs`, set `ttaaefs_queuename_peer` like this:

```
ttaaefs_queuename_peer = q1_ttaaefs
```

#### Read and write n_vals

When performing a GET on a Riak object in the source cluster, the FullSync client will read with an `r` value of `ttaaefs_localnval`. When performing a PUT of a Riak object in the sink cluster, the FullSync client will write with an `w` value of `ttaaefs_remotenval`. Both of these default to the standard Riak `n_val` of `3`.

To customise these values, use these settings:

```
ttaaefs_localnval = 3
ttaaefs_remotenval = 3
```

#### Connections

Each source cluster node can connect to a single sink cluster node (or a load balancer). This is specificed in the settings of `ttaaefs_peerip`, `ttaaefs_peerport`, and `ttaaefs_peerprotocol`.

- `ttaaefs_peerip` - the IP address or FQDN of the sink cluster node.
- `ttaaefs_peerport` - the port to connect to on the sink cluster node.
- `ttaaefs_peerprotocol` - the protocol to use to talk to the sink cluster node. Use `pb` for the Protocol Buffer API, and use `http` fpr the HTTP API.

For example, to connect to IP `10.2.34.56` on port `8087` using the Protocol Buffer API, these would be the settings to use:

```
ttaaefs_peerip = 10.2.34.56
ttaaefs_peerport = 8087
ttaaefs_peerprotocol = pb
```

For example, to connect to the FQDN `node01.source-cluster-a.mynetwork.com` on port `8098` using the HTTP API, these would be the settings to use:

```
ttaaefs_peerip = node01.source-cluster-a.mynetwork.com
ttaaefs_peerport = 8098
ttaaefs_peerprotocol = http
```

If you need to have TLS encryption and certificate-based authentication then you must exclusively use the Protocol Buffer API (`pb`) for replication.

##### TLS encryption

TLS security is configured for replication using the settings of `repl_cacert_filename`, `repl_cert_filename` and `repl_key_filename` which operate in a similar manner to the protocol listener settings.

For example, you could use settings similar to these:

```
repl_cacert_filename = /etc/riak/cacert.pem
repl_cert_filename = /etc/riak/cert.pem
repl_key_filename = /etc/riak/key.pem
```

##### Riak Security

If Riak Security is enabled on the sink cluster, then the username for replication can be set with the `repl_username` setting:

```
repl_username = source-cluster-replication-user
```

#### Schedule

FullSync uses an automated scheduling tool based on a configurable number of slots in a 24-hour period.

FullSync has the ability to check different time ranges, so recent changes can be checked more often than very old changes.

These time ranges are:

- `ttaaefs_autocheck` - uses logic to decide the best form of FullSync time range to check; this is the default.
- `ttaaefs_allcheck` - checks all keys.
- `ttaaefs_daycheck` - checks keys changed in the last 24 hours.
- `ttaaefs_hourcheck` - checks keys changed in the last hour.
- `ttaaefs_rangecheck` - checks keys since the last successfull check.
- `ttaaefs_nocheck` - skips the check; this is useful for padding the schedule.

Each check is set to an integer, and the FullSync scheduler will distribute the checks evenly over a 24 hours period in proportion to the number of each type of check.

For example, this schedule will run autocheck every hour:

```
ttaaefs_autocheck = 24
ttaaefs_allcheck = 0
ttaaefs_daycheck = 0
ttaaefs_hourcheck = 0
ttaaefs_rangecheck = 0
ttaaefs_nocheck = 0
```

For example, this schedule will run allcheck once per day, daycheck 3 times per day, hour check 8 times per day, and range check 12 times per day (for a total of 24 checks):

```
ttaaefs_autocheck = 0
ttaaefs_allcheck = 1
ttaaefs_daycheck = 3
ttaaefs_hourcheck = 8
ttaaefs_rangecheck = 12
ttaaefs_nocheck = 0
```

##### Tuning for autocheck

Autocheck can limit the use of allcheck by setting a window of time in which allcheck can be safely called. This is ideal for scenarios where there is a dip in activity in the source and sink clusters. By default `ttaaefs_allcheck.policy` is set to `always`. It can be set to `never` to not allow autocheck to use allcheck at all, or `window` to restrict the hours in which allcheck can be used.

For example, to stop autocheck from ever using allcheck, use this setting:

```
ttaaefs_allcheck.policy = never
```

To limit the hours autocheck can use allcheck to between 10pm and 6am, use these settings:

```
ttaaefs_allcheck.policy = window
ttaaefs_allcheck.window.start = 22
ttaaefs_allcheck.window.end = 6
```

#### Tuning

##### Results size

When performing a comparison between clusters, the keys are compared in chunks called segments. The number of chunks checked at one time can be set via the `ttaaefs_maxresults` setting. This is 32 chunks by default. To speed up comparisons but at the cost of more comparisons, reduce this value. If you intend to use autocheck or rangecheck in the scheduler, then this value can be reduced to as low as 16 and will apply to daycheck and hourcheck.

As a performance boost for rangecheck, `ttaaefs_rangeboost` will increase the number of chunks checked but only for rangecheck. This is a multipler, so the number of chunks checked will be `ttaaefs_maxresults` * `ttaaefs_rangeboost`.

For example, this will limit the daycheck and hourcheck to 32 chunks, but allow rangecheck to (32 * 16 =) 512 chunks:

```
ttaaefs_maxresults = 32
ttaaefs_rangeboost = 16
```

##### Cluster slice

`ttaaefs_cluster_slice` helps space out queries between clusters if you have more than 2 clusters performing FullSync to the same sink cluster. This will stop two clusters with identical schedules from mutual full-syncs at the same time. Each cluster may be configured with `ttaaefs_cluster_slice` number between 1 and 4.

For example, this will set the `ttaaefs_cluster_slice` to `1`.

```
ttaaefs_cluster_slice = 1
```

### V2 Scheduling Fullsync

**Deprecation Warning**
v2 Multi-Datacenter Replication is deprecated and will be removed in a future version. Please use [v3]({{< product-version-root >}}reference/replication-api/runtime-controls/) instead.

With the `pause` and `resume` commands it is possible to limit the
fullsync operation to off-peak times. First, disable `fullsync_interval`
and set `fullsync_on_connect` to `false`. Then, using cron or something
similar, execute the commands below at the start of the sync window.
In these examples, the commands are combined in a `.sh` or analogous
file:

```bash
#!/bin/sh

#### Resume from where we left off

riak repl resume-fullsync

#### Start fullsync if nothing is running

riak repl start-fullsync
```

At the end of the sync window:

```bash
#!/bin/sh

#### Stop fullsync until start of next sync window

riak repl pause-fullsync
```

### V2 Multi-Datacenter Replication Reference: Scheduling Fullsync

**Deprecation Warning**
v2 Multi-Datacenter Replication is deprecated and will be removed in a future version. Please use [v3]({{< product-version-root >}}how-to/configure/replication/configure-fullsync/) instead.

#### Scheduling Fullsync Operation

### Scheduling Fullsync

[config reference#advanced]: {{< product-version-root >}}reference/configuration/#advanced-configuration

The `fullsync_interval` parameter can be configured in the `riak repl`
section of [`advanced.config`][config reference#advanced] with either:

* a single integer value representing the duration to wait, in minutes,
  between fullsyncs, _or_
* a list of pairs of the form `[{"clustername", time_in_minutes},
  {"clustername", time_in_minutes}, ...]` pairs for each sink
  participating in fullsync replication. Note the commas separating each
  pair, and `[ ]` surrounding the entire list.

#### Examples

Sharing a fullsync time (in minutes) for all sinks:

```advancedconfig
{riak_repl, [
    % ...
    {data_root, "/configured/repl/data/root"},
    {fullsync_interval, 90} %% fullsync runs every 90 minutes
    % ...
    ]}
```

List of multiple sinks with separate times in minutes:

```advancedconfig
{riak_repl, [
    % ...
    {data_root, "/configured/repl/data/root"},
    % clusters sink_boston + sink_newyork have difference intervals (in minutes)
    {fullsync_interval, [
        {"sink_boston", 120},  %% fullsync to sink_boston with run every 120 minutes
        {"sink_newyork", 90}]} %% fullsync to sink_newyork with run every 90 minutes

]}
```

#### Additional Fullsync Stats

Additional fullsync stats per sink have been added in Riak.

* `fullsyncs_completed` &mdash; The number of fullsyncs that have been
  completed to the specified sink cluster.
* `fullsync_start_time` &mdash; The time the current fullsink to the
  specified cluster began.
* `last_fullsync_duration` &mdash; The duration (in seconds) of the last
  completed fullsync.

#### Configuration of All-Cluster Reconciliation

It is commonly most efficient to reconcile all data, rather than partial data.  If all data is not required, then [per-bucket reconciliation]({{< product-version-root >}}how-to/configure/replication/per-bucket-reconciliation/) can be enabled.  All-cluster reconciliation is much more common than per-bucket reconciliation in production systems, as it commonly has lower overheads.

#### Initial Configuration

Full-sync replication requires the existence of source queue definitions and sink worker configurations, in order for discovered deltas to be repaired.  The same configurations can be used as for real-time replication.  If there is a need to support reconciliation without allowing for real-time replication - then the `block_rtq` keyword can be used instead of `any` on the source queue definition.

> In configuration, reconciliation processes are commonly referred to by the initialism `ttaaefs` - TicTac AAE Full-Sync.

To enable reconciliation an initial configuration is required:

- `ttaaefs_scope = all`.
- `ttaaefs_queuename = <queue_name>`;
  - This is the queue name to be used by the remote cluster when fetching replication events.
  - When this node discovers a delta between the clusters, and the local cluster has the more up-to-date reference, the replication event will be added to the node's own replication queue under this queue name.
- `ttaaefs_queuename_peer = <queue_name>`;
  - This is the queue name to be used by the local cluster when fetching replication events from the remote cluster.
  - Adding a queue name makes full-sync reconciliation bidirectional.  If this node discovers the remote cluster has a more advanced version, it will send a request to the peer node to queue a replication event for the delta object on the configured queue.
  - If bidirectional reconciliation is not required, then the queue name should be set to `disabled`.
- `ttaaefs_localnval = <n_val>`;
  - The `n_val` to be used on this cluster when comparing to the opposing cluster.
  - The `n_val` may be different to the remote cluster, but it is preferred to avoid variance in `n_val` within a cluster.
- `ttaaefs_remotenval = <n_val>`;
  - The `n_val` to be used on the remote cluster.
- `ttaaefs_cluster_slice = 1`;
  - A number between 1 and 4.  All nodes on the same cluster should be given the same slice number.
  - Each time period has 4 slots, and clusters will schedule the activity in the slice associated with this number.
  - When configuring bidirectional replication between clusters, use 1 and 3, or 2 and 4 - as slice numbers for each cluster.
  - When multiple nodes are configured for reconciliation, time ranges are also sliced so that each node has its own time slice to run its reconciliation work.
    - Overlapping of reconciliation work is not managed through orchestration, but through allocation of slots based on node number (relative place in the list of nodes) and cluster slice.

Each node has a single manager for reconciliation - the `riak_kv_ttaaefs_manager`.  A manager can only have one configuration, it can manage reconciliation with one cluster for one `n_val` (and for one type, either all-cluster or per-bucket).  If the cluster needs to reconcile with other clusters, or with different settings, then other nodes should handle the alternate configurations.

> Reconciliation work is based on comparisons between clusters using AAE folds; so a single peer relationship between just two nodes is sufficient to reconcile the whole cluster.  However, for resilience and capacity reasons, ideally all nodes should be configured with different peer relationships.

To set up a peer relationship to another cluster, the following configuration is required:

- `ttaaefs_peerip = <ip_addr>`;
- `ttaaefs_peerport = <port>`;
- `ttaaefs_peerprotocol = pb|http`;
- For security the [settings for real-time replication]({{< product-version-root >}}how-to/configure/replication/configure-real-time-replication/) are used e.g. `repl_cacert_filename` etc.

#### Enabling Checks

Reconciliation requires the scheduling of checks.  Each check will perform a full-cluster AAE exchange to compare between the clusters, which has three phases:

- `root_compare`;
- `branch_compare`;
- `clock_compare`.

The root to be compared is the root of [the merkle tree]({{< product-version-root >}}foundations/replication/active-anti-entropy/) representing the state of the whole tree in 1,024 4-byte hashes.  The roots are merged across all partitions, to provide a representation of cluster state in a single 4KB integer.

If these roots match between the clusters, the clusters are considered to be reconciled - `in_sync = true` is the result of the exchange, and `{root_compare, 0}` is the final state of the exchange.  If not, the `root_compare` is repeated, and on the repeated check only deltas in the same 4-byte hash as the previous compare need to be considered a potential mismatch.  The `root_compare` will be repeated until the intersection of deltas is empty (all 1,024 hashes, have a some stage in the loop, matched between roots), or there exists a stable set of branches in the root, which differ on every comparison.  An empty set of deltas will be considered an `in_sync = true` result, otherwise the next phase is required.

The second phase is `branch_compare`.  Each branch is made up of 1,024 4-byte hash "leaves".  A subset of branches that have a consistent mismatch from the `root_compare` are chosen, and those branches are compared.  The same loop process used in the `root_compare` will be used to `branch_compare`, and discover either a stable delta - or potentially find that any delta is simply transient.

If all deltas are shown to be transient; then `in_sync = true` is the result of the exchange, and `{branch_compare, 0}` is the final state of the exchange.  Otherwise, a subset of tree leaves, also referred to as segment IDs, are chosen for the `clock_compare` stage.

In the final `clock_compare` stage, the keys and version vectors (clocks) are compared between the clusters.  The comparison behaviour will differ depending on the type of check that was requested.

All the keys that hash to those segment IDs need to be compared to be certain to find the delta, and this requires a full-scan of the keystore - and such a scan is a `ttaaefs_allcheck`.  This scan is accelerated by skipping over blocks of keys on disk that do not have any keys with a matching segment ID (using a hash-based filter cached with the block inside the leveled keystore).  Even with acceleration, the scan has a non-trivial cost in large stores.

If it can be determined from the results of previous checks, that all deltas are likely to be within a given time range (by object last_modified_date), or in a specific bucket; then this information can be used to narrow the scope of the scan in `clock_compare`.  A comparison reduced in scope this way is a `ttaaefs_rangecheck`, and can be substantially quicker than a `ttaaefs_allcheck`.

Available from Riak 3.0.15The preferred check approach is to use `ttaaefs_autocheck`.  This is a check that uses context to select an appropriate `ttaaefs_rangecheck` when possible, and only fallback to `ttaaefs_allcheck` if necessary.  For example, if a cluster falls out of sync, it will assume first that the delta is a modified date range since the last successful check.

> The ability to set a schedule of specific checks (e.g. `ttaaefs_allcheck`, `ttaaefs_hourcheck` etc) has been maintained, but from Riak 3.0.15 it is recommended that the schedule of checks should only be configured to use `ttaaefs_autocheck`.

The schedule of reconciliation jobs is configured for each peer by setting:

- `ttaaefs_autocheck = <checks_per_day>`;
  - Sets the number of checks each day for this peer relationship, noting that each peer relationship will schedule checks independently (i.e. setting to 24 checks in an 8 node cluster with 8 peer relationships to another 8 node cluster using bidirectional reconciliation - will amount to a check every 3 minutes and 45 seconds, or 24 x 8 x 2 checks per day).
- `ttaaefs_allcheck.policy = always`.
  - Should be set to `always` unless a specific issue occurs which requires a window to be set.
- All other checks should normally set to 0;
  - `ttaaefs_allcheck`, `ttaaefs_hourcheck`, `ttaaefs_daycheck` - these are checks where the time range is hard-coded.  The `ttaaefs_nocheck` and `ttaaefs_rangecheck` are legacy settings that solved problems that existed prior to the introduction of `ttaaefs_autocheck`.

[overview]: #overview
[enable fullsync]: {{< product-version-root >}}how-to/configure/replication/configure-fullsync/
[queues]: #queues
[read write values]: {{< product-version-root >}}how-to/configure/replication/configure-fullsync/
[connections]: #connections
[tls encryption]: #tls-encryption

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
