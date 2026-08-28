---
title: 'Monitor active anti-entropy'
description: 'Show operators how to inspect active anti-entropy progress, health, and failure signals.'
weight: 22
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\active-anti-entropy.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-active-anti-entropy.md'
source_material:
  - 'legacy-3.2.5'
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-aae---logs-and-statistics'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-and-controlling-aae---command-line'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-anti-entropy'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-legacy-aae'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to inspect active anti-entropy progress, health, and failure signals.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Legacy Active Anti-Entropy

OpenRiak's [active anti-entropy](../../../learn/concepts/active-anti-entropy/) \(AAE) subsystem is a set of background processes that repair object inconsistencies stemming from missing or divergent object values across nodes. Riak operators can turn AAE on and off and configure and monitor its functioning.

In Riak versions 2.9.1 and later, [TicTac AAE](/kv/3.4.0/how-to/operate/monitor-active-anti-entropy/) is included with releases as an option to be used in addition to or instead of traditional AAE in Riak.

#### Enabling Active Anti-Entropy

Whether AAE is currently enabled in a node is determined by the value of
the `anti_entropy` parameter in the node's [configuration files](../../../configuring/reference/).

In Riak versions 2.0 and later, AAE is turned on by default.

```riakconf
anti_entropy = active
```

```appconfig
{riak_kv, [

{anti_entropy, {on, []}},

%% More riak_kv settings...
]}
```

For monitoring purposes, you can also activate AAE debugging, which
provides verbose debugging message output:

```riakconf
anti_entropy = active-debug
```

%% With debugging
    {anti_entropy, {on, [debug]}},

Remember that you will need to [restart the node](../../admin/riak-cli/#restart) for any configuration-related changes to take effect.

#### Disabling Active Anti-Entropy

Alternatively, AAE can be switched off if you would like to repair
object inconsistencies using [read repair](../../../learn/concepts/active-anti-entropy/#read-repair-vs-active-anti-entropy) alone:

```riakconf
anti_entropy = passive
```

%% AAE turned off
    {anti_entropy, {off, []}},

If you would like to reclaim the disk space used by AAE operations, you
must manually delete the directory in which AAE-related data is stored
in each node.

```bash
rm -Rf <path_to_riak_node>/data/anti_entropy/*
```

The default directory for AAE data is `./data/anti_entropy`, as in the
example above, but this can be changed. See the section below titled
**Data Directory**.

The directory deletion method above can also be used to force a
rebuilding of hash trees.

#### Monitoring AAE

OpenRiak's command-line interface includes a command that provides insight
into AAE-related processes and performance:

```bash
riak admin aae-status
```

When you run this command in a node, the output will look like this
(shortened for the sake of brevity):

```
================================== Exchanges ==================================
Index                                              Last (ago)    All (ago)
-------------------------------------------------------------------------------
0                                                  19.0 min      20.3 min
22835963083295358096932575511191922182123945984    18.0 min      20.3 min
45671926166590716193865151022383844364247891968    17.3 min      19.8 min
68507889249886074290797726533575766546371837952    16.5 min      18.3 min
91343852333181432387730302044767688728495783936    15.8 min      17.3 min
...

================================ Entropy Trees ================================
Index                                              Built (ago)
-------------------------------------------------------------------------------
0                                                  5.7 d
22835963083295358096932575511191922182123945984    5.6 d
45671926166590716193865151022383844364247891968    5.5 d
68507889249886074290797726533575766546371837952    4.3 d
91343852333181432387730302044767688728495783936    4.8 d

================================ Keys Repaired ================================
Index                                                Last      Mean      Max
-------------------------------------------------------------------------------
0                                                     0         0         0
22835963083295358096932575511191922182123945984       0         0         0
45671926166590716193865151022383844364247891968       0         0         0
68507889249886074290797726533575766546371837952       0         0         0
91343852333181432387730302044767688728495783936       0         0         0

```

Each of these three tables contains information for each
[vnode](../../../learn/concepts/vnodes) in your cluster in these three categories:

Category | Measures | Description
:--------|:---------|:-----------
**Exchanges** | `Last` | When the most recent exchange between a data partition and one of its replicas was performed
  | `All` | How long it has been since a partition exchanged with all of its replicas
**Entropy Trees** | `Built` | When the hash trees for a given partition were created
**Keys Repaired** | `Last` | The number of keys repaired during all key exchanges since the last node restart
  | `Mean` | The mean number of keys repaired during all key exchanges since the last node restart
  | `Max` | The maximum number of keys repaired during all key exchanges since the last node restart

All AAE status information obtainable using the `riak admin aae-status`
command is stored in-memory and is reset when a node is restarted with
the exception of hash tree build information, which is persisted on disk
(because hash trees themselves are persisted on disk).

#### Configuring AAE

OpenRiak's [configuration files](../../../configuring/reference/) enable you not just to turn AAE on and
off but also to fine-tune your cluster's use of AAE, e.g. how
much memory AAE processes should consume, how frequently specific
processes should be run, etc.

##### Data Directory

By default, data related to AAE operations is stored in the
`./data/anti_entropy` directory in each OpenRiak node. This can be changed
by setting the `anti_entropy.data_dir` parameter to a different value.

##### Bloom Filters

Bloom filters are mechanisms used to prevent reads that are destined to
fail because no object exists in the location that they're querying.
Using bloom filters can improve reaction time for some queries, but
entail a small general performance cost. You can switch bloom filters
on and off using the `anti_entropy.bloomfilter` parameter.

##### Trigger Interval

The `anti_entropy.trigger_interval` setting determines how often OpenRiak's
AAE subsystem looks for work to do, e.g. building or expiring hash
trees, triggering information exchanges between nodes, etc. The default
is every 15 seconds (`15s`). Raising this value may save resources, but
at a slightly higher risk of data corruption.

##### Hash Trees

As a fallback measure in addition to the normal operation of AAE on-disk
hash trees, Riak periodically clears and regenerates all hash trees
stored on disk to ensure that hash trees correspond to the key/value
data stored in Riak. This enables Riak to detect silent data corruption
resulting from disk failure or faulty hardware. The
`anti_entropy.tree.expiry` setting enables you to determine how often
that takes place. The default is once a week (`1w`). You can set up this
process to run once a day (`1d`), twice a day (`12h`), once a month
(`4w`), and so on.

In addition to specifying how often Riak expires hash trees after they
are built, you can also specify how quickly and how many hash trees are
built. You can set the frequency using the
`anti_entropy.tree.build_limit.per_timespan` parameter, for which the
default is every hour (`1h`); the number of hash tree builds is
specified by `anti_entropy.tree.build_limit.number`, for which the
default is 1.

##### Write Buffer Size

While you are free to choose the backend for data storage in Riak,
background AAE processes use [LevelDB](../../../setup/planning/backend/leveldb). You can adjust the size of the
write buffer used by LevelDB for hash tree generation using the
`anti_entropy.write_buffer_size` parameter. The default is `4MB`.

##### Open Files and Concurrency Limits

The `anti_entropy.concurrency_limit` parameter determines how many AAE
cross-node information exchanges or hash tree builds can happen
concurrently. The default is `2`.

The `anti_entropy.max_open_files` parameter sets an open-files limit for
AAE-related background tasks, analogous to [open files limit](../../performance/open-files-limit) settings used in operating systems. The default is `20`.

### TicTac Active Anti-Entropy

#### TicTac AAE

The version of TicTac AAE included in 2.9 releases is a working prototype with limited testing. The intention is to full integrate the library into the KV 3.0 release.

TicTac Active Anti-Entropy makes two changes to the way Anti-Entropy has previously worked in Riak. The first change is to the way Merkle Trees are contructed so that they are built incrementally. The second change allows the underlying Anti-entropy key store to be key-ordered while still allowing faster access to keys via their Merkle tree location or the last modified date of the object.

#### Configuring AAE

OpenRiak's [configuration files](../../../configuring/reference/) enable you not just to turn TicTac AAE on and
off but also to fine-tune your cluster's use of TicTac AAE to suit your requirements.

#### Monitoring Anti-Entropy

The Tictac anti-entropy system can be monitored either through the command line, or via logs and statistics.  It is recommended to manage the configuration via `riak.conf` file, but some configuration can be dynamically updated at runtime using the command line.

#### Monitoring and Controlling AAE - Command Line

**Available from OpenRiak KV 3.4.0.**

Monitoring and control functions for Tictac AAE are available through the command line interface - `riak admin tictacaae --help`.

```console
riak admin tictacaae rebuildtick|exchangetick|maxresults|rangeboost [-n NODE] [VAL]
riak admin tictacaae rebuild-soon [-n NODE] [-p PARTITION] DELAY
riak admin tictacaae rebuild-now [-n NODE] [-p PARTITION]
riak admin tictacaae storeheads [-n NODE] [-p PARTITION] [VALUE]
riak admin tictacaae tokenbucket [-n NODE] [-p PARTITION] [VALUE]
riak admin tictacaae rebuild_schedule [-n NODE] [-p PARTITION] [RW RD]
riak admin tictacaae treestatus [--format table|json] [--show STATES]
```

Configuration control commands `rebuildtick`, `exchangetick`, `maxresults`, and `rangeboost` are simple set/show commands, reading and setting the corresponding environment variables. The changes are applied to the local node by default, or on another node if specified with option `-n`.

- The `exchangetick` alters the frequency of AAE activity, each vnode runs a tick, and each tick prompts an exchange.
- The `rebuildtick` alters the frequency with which a vnode will check to see if a rebuild is due;
  - The tick does not alter the actual frequency of rebuilds.
- Changes to `rebuildtick` and `exchangetick` will take effect on the next tick, impacting the size of the next-but-one tick.
  - Both the `rebuildtick` and `exchangetick` are set in milliseconds.
- The `maxresults` limit controls the scope of repairs per exchange (a limit on [the segment IDs covered by an exchange](/kv/3.4.0/explanation/replication/active-anti-entropy/)).
  - This is multiplied by the `rangeboost` if the exchange has been seeded with range information auto-discovered in previous exchanges.  For example if all deltas are in a certain modified date range.

> Do not set the value of the `exchangetick` or `rebuildtick` to a value lower than double the riak_core `vnode_inactivity_timeout`.  The default `vnode_inactivity_timeout` is 60s, so setting this to a value lower than `120000` milliseconds would be unsafe.

> If the number of segment IDs being checked within an AAE exchange are significantly over one thousand, then the acceleration associated with the restriction will tend towards zero.  So the combined value of `maxresults * rangeboost` should be kept to a value less than or equal to 1024.

Configuration control commands `storeheads`, `tokenbucket`, `rebuild_schedule` will extract or inject the actual relevant values from or to the state of the running AAE controller processes.

- Changing `storeheads` at runtime will also require a parallel store rebuild to take full effect.
- Care is required when setting the `rebuild_schedule` to use the correct units (hours for `wait` and seconds for `delay`).
- Disabling the `tokenbucket` protection is not recommended.

> It is recommended to control configuration through management of `riak.conf` not via the CLI.  The `riak admin tictacaae` commands should only be used when there is an urgent need to change the configuration on a running node, without requiring a restart.

The action command `rebuild-soon` will set the next rebuild time on all the nodes and vnodes specified, to the `delay` in seconds:

- A rebuild on a parallel-mode AAE vnode will rebuild the parallel keystore from the vnode store, and then rebuild the cached trees from that parallel store.
- A rebuild of a native vnode (i.e. with a single `leveled` backend), will rebuild the cached tree from the [leveled ledger](/kv/3.4.0/explanation/storage/leveled/) keystore (but also checking for presence of the object in the journal).
- Rebuilds are expensive processes: concurrent store rebuilds will be queued on the Best Endeavours [node worker pool](/kv/3.4.0/how-to/operate/monitor-worker-pools/), and tree rebuilds on the AF1 pool.
- After the delay has been set, the rebuild will not be triggered until the next `rebuildtick` on each vnode after the delay.
  - To immediately trigger a `rebuildtick` then use of the `rebuild-now` command is required after the `delay` has been changed.  `rebuild-now` only triggers a rebuild that is due, it will have no impact if a rebuild is not due (e.g. when `rebuild-soon` has not first been used).

The `treestatus` command will collect information from running AAE controllers and produce a report:

```console
                                        Partition ID      Status      Last Rebuild Date     Next Rebuild Date   Controller PID  Key Store Status
----------------------------------------------------  ----------  ---------------------  --------------------  ---------------  ----------------
   1004782375664995756265033322492444576013453623296     unbuilt                  never   2025-03-21T19:14:21       <0.2780.0>            native
                                                   0     unbuilt                  never   2025-03-23T04:59:09       <0.2296.0>            native
   1073290264914881830555831049026020342559825461248     unbuilt                  never   2025-03-16T14:05:43       <0.2763.0>            native
```

#### Monitoring AAE - Logs and Statistics

When Tictac AAE is enabled, each vnode has a queue of exchanges related to that vnode's supported partitions, and the vnode will loop through that queue, prompting a new exchange every `exchangetick`.  If the `n_val` is 3 this will require 5 exchanges, and exchanges are required for every `n_val` configured in the cluster.

The result of each individual exchange is not logged by `riak_kv `unless it shows a discrepancy, although the details of each exchange can be found in the AAE logs with the tag `log_ref=ex*`.  A summary log is produced every loop from the `riak_kv_vnode` ("Tictac AAE loop completed"), giving the statistics for that loop.

Statistics on Tictac AAE exchanges are also available via [riak stats](/kv/3.4.0/reference/operations/statistics-and-monitoring/):

- `tictacaae_queue_microsec__max`, `tictacaae_queue_microsec_mean`.
  - The time spent by the vnode waiting for the controller to respond to an update (prompted by a PUT on the vnode).
  - May give an indication that the vnode is being delayed due to the overhead of maintaining a parallel-mode AAE store.
- `tictacaae_root_compare`, `tictacaae_branch_compare`, `tictacaae_clock_compare`, `tictacaae_error`, `tictacaae_timeout`, `tictacaae_notsupported`.
  - Counts of the exchanges by the closing status of the exchange.
    - Intra-cluster exchanges follow [the same process as inter-cluster reconciliation exchanges](/kv/3.4.0/how-to/configure/replication/configure-fullsync/).
    - `root_compare` or `branch_compare` indicate no deltas were discovered.
  - Because of the infrequency of exchanges, tracking the `*_total` statistics is normally required to gain understanding of trends in AAE activity.

> Additional logging will be generated if significant deltas are discovered, and the AAE process enters into a repair loop: a process through which repairs are accelerated by using information about the deltas being discovered (i.e. any pattern of buckets and modified date ranges discovered in deltas).

AAE will prompt the repair of delta using read repairs, so the [monitoring of read repairs](/kv/3.4.0/how-to/operate/monitor-read-repairs/) provides further information.

#### Monitoring legacy AAE

If using the non-tictac AAE process, [information on the management and monitoring of AAE can be found in the legacy documentation](https://docs.riak.com/riak/kv/latest/using/cluster-operations/active-anti-entropy/index.html).

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
