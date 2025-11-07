---
title: Basic Configuration
sidebar_label: "Basic Configuration"
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';

# Basic OpenRiak KV node configuration

This page covers the most baisc configuration changes to be made when setting up a new OpenRiak node/cluster.
All the configuration values discussed here are maintained in the configuration file (`riak.conf`) on each node, and a node will require a restart for any changes to take effect.

# Contents

1. [Erlang VM Tunings](#erlang-vm-tunings)
2. [Ring Size](#ring-size)
3. [Backend](#backend)
4. [Default Bucket Properties](#default-bucket-properties)

# Erlang VM Tunings

Before building your cluster, there are Erlang-VM changes that should be made in your node's configuration files.

<insert link to erland vm changes here>

# Ring Size

The ring size, in OpenRiak parlance, is the number of data partitions that comprise the cluster. This quantity impacts the scalability and performance of a cluster and, importantly, it should be established before the cluster starts receiving data.

If the ring size is too large for the number of servers, disk I/O will be negatively impacted by the excessive number of concurrent databases running on each server; if the ring size is too small, the servers’ other resources (primarily CPU and RAM) will go underutilized.

### Note: The steps involved in changing the ring size depend on whether the Nodes in the cluster have already been joined together or if it is changed prior to joining.

The following steps will outline changing the ring size depending on two scenarios, If the nodes have joined a cluster but no data needs to be preserved and new nodes with no data and no cluster joined yet.

## Cluster joined, but no data needs to be retained.

1. Change the ring creation size parameter by uncommenting it and then setting it to the desired value, for example 64:

```bash
ring_size = 64
```

2. Stop all nodes

3. Remove the ring data file on each node (see <insert location here> for the location of this file)

4. You can start the nodes now, but you should finish reviewing this document and proceed to Basic Cluster Setup

## New nodes, have not yet joined a cluster

1. Change the ring creation size parameter by uncommenting it and then setting it to the desired value, for example 64:

```bash
ring_size = 64
```

2. Stop all nodes

3. Remove the ring data file on each node (see <insert location here> for the location of this file)

4. You can start the nodes now, but you should finish reviewing this document and proceed to Basic Cluster Setup

## Verifying ring size

You can use the `riak admin status` command can verify the ring size:

```bash
riak admin status | grep ring
```

You should see an output similar to below:

```bash
ring_members : ['riak@192.168.0.1']
ring_num_partitions : 8
ring_ownership : <<"[{'riak@192.168.0.1',8}]">>
ring_creation_size : 8
```

If `ring_num_partitions` and `ring_creation_size` do not agree, that means that the `ring_creation_size` value was changed too late and that the proper steps were not taken to start over with a new ring.

### Note: OpenRiak will not allow two nodes with different ring sizes to be joined into a cluster.

# Backend

Another critical decision to be made is the backend to use. The choice of backend strongly influences the performance characteristics and feature set for a Riak environment.

While for most of Riak's lifetime, Bitcask was the recommend and default backend for users, in recent years a new backend was developed specifically for OpenRiak, entirely within the Erlang Environment called leveled.

See (choosing a backend)[.../setup/plan/choosing-a-backend] for details on which backend to select.

As with ring size, changing the backend will result in all data being inaccessible until the backend is changed back, so spend the necessary time up front to evaluate and benchmark backends or planning a method to migrate.

# Default Bucket Properties

Bucket properties are also very important factors in Riak’s performance and general behavior. The properties for any individual bucket can be configured dynamically using bucket types, but default values for those properties can be defined in your configuration files.

<insert bucket property links>

If the default bucket properties are modified in your configuration files and the node is restarted, any existing buckets will not be directly impacted, although the mechanism described in HTTP Reset Bucket Properties can be used to force them to pick up the new defaults.