---
title: 'Configure basic node settings'
description: 'Show operators how to configure basic node settings and verify the result.'
weight: 3
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\basics.md'
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\guides\basic-configuration.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\basic.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---key-riakconf-changes'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure basic node settings and verify the result.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

### Basic OpenRiak KV Configuration

[config reference]: {{< product-version-root >}}reference/configuration/
[use running cluster]: {{< product-version-root >}}how-to/operate/
[use admin riak admin#member-status]: {{< product-version-root >}}reference/commands/riak-admin/#member-status
[perf erlang]: {{< product-version-root >}}how-to/tune/tune-erlang-vm/
[plan start]: {{< product-version-root >}}how-to/plan/
[plan best practices]: {{< product-version-root >}}how-to/plan/production-readiness-checklist/
[cluster ops backup]: {{< product-version-root >}}how-to/operate/back-up-node/
[cluster ops add remove node]: {{< product-version-root >}}tutorials/operations/change-cluster-membership/
[plan backend]: {{< product-version-root >}}explanation/storage/choosing-backend/
[plan backend multi]: {{< product-version-root >}}explanation/storage/multi-backend/
[plan backend bitcask]: {{< product-version-root >}}explanation/storage/bitcask/
[usage bucket types]: {{< product-version-root >}}how-to/develop/use-bucket-types/
[apps replication properties]: {{< product-version-root >}}explanation/replication/references-and-triggers/
[concept buckets]: {{< product-version-root >}}explanation/data-model/keys-objects-and-buckets/
[concept eventual consistency]: {{< product-version-root >}}explanation/consistency/eventual-consistency/
[perf benchmark]: {{< product-version-root >}}how-to/tune/benchmark-cluster/
[perf open files]: {{< product-version-root >}}how-to/tune/set-open-files-limit/
[perf index]: {{< product-version-root >}}how-to/tune/
[perf aws]: {{< product-version-root >}}how-to/tune/tune-aws-deployment/
[Cluster Capacity Planning]: {{< product-version-root >}}explanation/storage/capacity-planning/

This document covers the parameters that are commonly adjusted when
setting up a new cluster. We recommend that you also review the detailed
[Configuration Files][config reference] document before moving a cluster into
production.

All configuration values discussed here are managed via the
configuration file on each node, and a node must be restarted for any
changes to take effect.

> **Note**
>
> If you are upgrading to OpenRiak KV version 2.0 or later from an pre-2.0
release, you can use either your old `app.config` configuration file or
the newer `riak.conf` if you wish.
>
> If you have installed OpenRiak KV 2.0 directly, you should use only
`riak.conf`.
>
> More on configuring OpenRiak KV can be found in the [configuration files][config reference]
doc.

We advise that you make as many of the changes below as practical
_before_ joining the nodes together into a cluster. Once your
configuration has been set on each node, follow the steps in [Basic Cluster Setup][use running cluster] to complete the clustering process.

Use [`riak admin member-status`][use admin riak admin#member-status]
to determine whether any given node is a member of a cluster.

#### Erlang VM Tunings

Prior to building and starting a cluster, there are some
Erlang-VM-related changes that you should make to your configuration
files. If you are using the older, `vm.args`-based Erlang VM tunings,
you should set the following:

```vmargs
+sfwi 500
+scl false
```

If you are using the newer, `riak.conf`-based configuration system, we
recommend the following settings:

```riakconf
erlang.schedulers.force_wakeup_interval = 500
erlang.schedulers.compaction_of_load = false
```

More information can be found in [Erlang VM Tuning][perf erlang].

#### Ring Size

The ring size, in Riak parlance, is the number of data partitions that
comprise the cluster. This quantity impacts the scalability and
performance of a cluster and, importantly, **it should be established
before the cluster starts receiving data**.

If the ring size is too large for the number of servers, disk I/O will
be negatively impacted by the excessive number of concurrent databases
running on each server; if the ring size is too small, the servers' other
resources (primarily CPU and RAM) will go underutilized.

See [Cluster Capacity Planning] for more details on choosing a ring size.

The steps involved in changing the ring size depend on whether the
servers (nodes) in the cluster have already been joined together.

##### Cluster joined, but no data needs to be preserved

1. Change the ring creation size parameter by uncommenting it and then
setting it to the desired value, for example 64:

```riakconf
    ring_size = 64
    ```

```appconfig
    %% In the riak_core section:
    {ring_creation_size, 64}
    ```

2. Stop all nodes
3. Remove the ring data file on each node (see [Backing up Riak][cluster ops backup] for the location of this file)
4. Start all nodes
5. Re-add each node to the cluster (see [Adding and Removing Nodes][cluster ops add remove node]) or finish reviewing this document and proceed to [Basic Cluster Setup][use running cluster]

##### New servers, have not yet joined a cluster

2. Stop all nodes
3. Remove the ring data file on each node (see [Backing up Riak][cluster ops backup] for
the location of this file)
4. Finish reviewing this document and proceed to [Basic Cluster Setup][use running cluster]

##### Verifying ring size

You can use the `riak admin` command can verify the ring size:

```bash
riak admin status | grep ring
```

Console output:

```
ring_members : ['riak@10.160.13.252']
ring_num_partitions : 8
ring_ownership : <<"[{'riak@10.160.13.252',8}]">>
ring_creation_size : 8
```

If `ring_num_partitions` and `ring_creation_size` do not agree, that
means that the `ring_creation_size` value was changed too late and that
the proper steps were not taken to start over with a new ring.

**Note**: Riak will not allow two nodes with different ring sizes to be
joined into a cluster.

#### Backend

Another critical decision to be made is the backend to use. The choice
of backend strongly influences the performance characteristics and
feature set for a Riak environment.

See [Choosing a Backend][plan backend] for a list of supported backends. Each
referenced document includes the necessary configuration bits.

As with ring size, changing the backend will result in all data being
effectively lost, so spend the necessary time up front to evaluate and
benchmark backends.

If still in doubt, consider using the [Multi][plan backend multi] backend for future
flexibility.

If you do change backends from the default ([Bitcask][plan backend bitcask]), make sure you change it across all nodes. It is possible but generally unwise to use different backends on different nodes, as this would limit the
effectiveness of backend-specific features.

#### Default Bucket Properties

Bucket properties are also very important factors in OpenRiak's performance
and general behavior. The properties for any individual bucket can be
configured dynamically [using bucket types][usage bucket types], but default values for those properties can be defined in your [configuration files][config reference].

Below is an example of setting `last_write_wins` to `true` and `r` to 3.

```riakconf
buckets.default.last_write_wins = true
buckets.default.r = 3
```

```appconfig
{default_bucket_props, [
    {last_write_wins,true},
    {r,3},
    ...
    ]}
```

For more on bucket properties, we recommend reviewing our docs on
[buckets][concept buckets], [bucket types][usage bucket types], [replication properties][apps replication properties], and [eventual consistency][concept eventual consistency], as well as Basho's five-part blog series, "Understanding OpenRiak's Configurable Behaviors."

* [Part 1](https://riak.com/understanding-riaks-configurable-behaviors-part-1/)
* [Part 2](https://riak.com/riaks-config-behaviors-part-2/)
* [Part 3](https://riak.com/riaks-config-behaviors-part-3/)
* [Part 4](https://riak.com/riaks-config-behaviors-part-4/)
* [Epilogue](https://riak.com/riaks-config-behaviors-epilogue/)

If the default bucket properties are modified in your configuration
files and the node is restarted, any existing buckets will **not** be
directly impacted, although the mechanism described in [HTTP Reset Bucket Properties]({{< product-version-root >}}reference/http-api/reset-bucket-properties/) can be used to force them to pick up the new
defaults.

#### System tuning

Please review the following documents before conducting any
[benchmarking][perf benchmark] and/or rolling out a live production
cluster.

* [Open Files Limit][perf open files]
* [System Performance Tuning][perf index]
* [AWS Performance Tuning][perf aws]
* [Configuration Files][config reference]

#### Joining the nodes together

Please see [Running A Cluster][use running cluster] for the cluster creation process.

#### Configuration of Riak - key riak.conf changes

Almost all configuration of Riak can be done through the `etc/riak.conf` file.  Each public configuration option should be described in that file, but there are additional `hidden` options supported for expert-advised changes.  The `riak.conf` file is built from individual schema files, and the repositories which contribute towards those schema files are listed in [the `cuttlefish` section of the `riak/rebar.config` file](https://github.com/OpenRiak/riak/blob/fd27c6933391ece65b31760cccb87b671a80f310/rebar.config#L23-L37).

Each individual schema component can be found in the `priv` folder for that repository, e.g [priv/riak_kv.schema for the riak_kv schema](https://github.com/OpenRiak/riak_kv/blob/openriak-3.4/priv/riak_kv.schema).

When starting a first cluster to experiment, the following configuration items are of particular importance:

- `ring_size`; refer to the [ring size selection in the design decisions document]({{< product-version-root >}}how-to/plan/choose-ring-size/), should be set smaller than the default for test/dev environments and larger than the default for production systems.
- `tictacaae_active`; refer to the [intra-cluster resilience in the design decisions document]({{< product-version-root >}}how-to/plan/choose-intra-cluster-resilience/).  Should be set to active if the active repair of deltas between vnodes is required, otherwise repair will be reactive (i.e. only once a delta has been detected on read).
- `tictacaae_storeheads`; should be enabled when using `tictacaae_active` on a leveled backend if the full scope of AAE Folds are to be used.
- `anti_entropy`; this is a deprecated anti-entropy system, and should be set to `passive` if using `tictacaae_active`.  It may be set to `active` in parallel to `tictacaae_active` to transition between the services.  The legacy anti-entropy system is quicker and more aggressive at repairing deltas, but offers less functionality and runs at a higher cost when in sync.
- `storage_backend`; refer to the [backend selection in the design decisions document]({{< product-version-root >}}how-to/plan/choose-storage-backend/), but for full Riak functionality must be set to leveled.
- `read_repair_primaryonly`; will impact the behaviour in failure, by default when a standby vnode replaces a failed vnode, read repair will be triggered on every GET to populate the standby with old writes, but this will have a negative impact performance during both failure and recovery.
- `buckets.default.merge_strategy`; should always be set to `2`, and `2` will be the only supported option from Riak 4.0.
- `nodename`; a unique name for the node within the cluster.
- `platform_data_dir`; where the actual data will be stored, must be a space with sufficient capacity and throughput.
- `listener.http.internal` or `listener.pb.internal`; the IP address and port for accessing the API. It is recommended to bind this IP address to a specific interface address.  [The Query API]({{< product-version-root >}}tutorials/query-api/) requires use of the `http` listener, and performance will differ between the `pb` and `http` transports when using [the Object API]({{< product-version-root >}}reference/http-api/).

In a `riak.conf` file, the last setting of any configuration item is the actual value used in the configuration.  Edits to the riak.conf file don't have to change the configuration in place, defaults may be overwritten by concatenating changes to the end of the file.

## Basic Configuration

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
