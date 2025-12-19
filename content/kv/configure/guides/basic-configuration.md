---
sidebar_position: 1
title: Basic Configuration
sidebar_label: "Basic Configuration"
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

[overview]: #overview
[ring-size]: #ring-size
[verify ring size]: #verifying-ring-size

## Overview

This page covers the following: [Ring Size][ring-size], [Backend][backend] and [Enabling TicTac Active Anti-Entropy][enable-TTAAE]

## Ring Size

    The ring size is the number of data partitions that comprise the cluster. This quantity impacts the scalability and performance of a cluster and, importantly, it should be established before the cluster starts receiving data.

    If the ring size is too big for the number of servers, each server will have to run too many databases at once, which will slow down disk performance. If the ring size is too small, the servers won’t use their CPU and memory efficiently.

    For help choosing the right ring size, check the Cluster Capacity Planning guide.

    The steps to change the ring size depend on whether the nodes in the cluster are already connected.

    The ring size is set in the `riak.conf` file.

## New nodes that have not yet joined a cluster

1. Change the ring creation size value by uncommenting it and then setting it to the desired value, for example 64:

    ```bash
        ring_size = 64
    ```

2. Stop all nodes

3. Remove the ring data file on each node (this varies by operating system, so you should check this using the OS specific refence)

    This will allow you to start the nodes and join them together with the correct ring size.

## Cluster joined, but no data needs to be preserved

1. Open the `riak.conf` file and change the ring creation size parameter by uncommenting it and then setting it to the desired value, for example 64:

    ```bash
        ring_size = 64
    ```

2. Stop all nodes

3. Remove the ring data file on each node (this varies by operating system, so you should check this using the OS specific refence)

4. Start all nodes

5. Re-add all the nodes to the cluster

## Verifying ring size

You can use the riak admin command can verify the ring size:

    ```bash
        riak admin status | grep ring
        Console output:

        ring_members : ['riak@127.0.0.1',`riak@127.0.0.2`,`riak@127.0.0.3`,`riak@127.0.0.4`,`riak@127.0.0.5`]
        ring_num_partitions : 64
        ring_ownership : <<"[{'riak@127.0.0.1',13},\n {'riak@127.0.0.2',13},\n {'riak@127.0.0.3',13},\n {'riak@127.0.0.4',13},\n {'riak@127.0.0.5',12}]">>
        ring_creation_size : 64
    ```

If `ring_num_partitions` and `ring_creation_size` do not agree, that means that the `ring_creation_size` value was changed too late and that the proper steps were not taken to start over with a new ring.

>![NOTE] Note on different ring size between nodes
> Riak will not allow two nodes with different ring sizes to be joined into a cluster.