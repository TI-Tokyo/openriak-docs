---
title: Node Control
sidebar_label: "Node Control"
date: 2026-06-25
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

[start]: #starting-a-node
[stop]: #stopping-a-node
[restart]: #restarting-a-node
[inspect]: #inspecting-your-node
[test]: #testing-read-and-write
[nodestatus]: #checking-node-status
[clusterstatus]: #checking-cluster-status
[member]: #checking-member-status
[clusterstatus]: #checking-cluster-status
[ringstatus]: #checking-ring-status

## Overview

This section covers the various commands used in general control of your node, including [starting a node][start node], [stopping a node][stop node], [inspecting your node][inspect node] and other operations.

> [!CODE] `riak` commands
>
> ```bash
>riak start
>riak stop
>riak ping
>riak debug
>riak reboot

> [!CODE] `riak admin` commands
>
>riak admin test
>riak admin cluster status
>riak admin member status
>riak admin ring-status

## Starting and stopping a node

This section covers starting and stopping your OpenRiak node via command line.

## Starting a node

    To start an OpenRiak node, you will use the following command:

    ```bash
        riak start
    ```

    If the node has started successfully, you will not see any response from OpenRiak.

## Stopping a node

    To stop an OpenRiak node, you will use the following command:

    ```bash
        riak stop
    ```

    If the node has stopped successfully, you will not see any response from OpenRiak.

## Restarting a node

    To restart a node, use the following command:

    ```bash
        riak reboot
    ```

    You will see no output if the command is correct, but you can check whether the node restarted successfully using the `riak ping` command in the next section. 
## Checking if a node is running

    If you are uncertain whether an OpenRiak node is running currently, you can check with the following:

    ```bash
        riak ping
    ```

    If the node is running, you should see the following response:


    ```bash
        pong
    ```

    If a node is not running or has crashed, you will see:

    ```bash
        Node riak@127.0.0.1 is not responding to pings
    ```

## Inspecting your node

There are a variety of ways to inspect your node for a variety of reasons, from checking it can read and write, to reviewing the performance statistics.

## Testing read and write

    If you want to test if your node is able to read and write, you can use the following command:

    ```bash
        riak admin test
    ```

    You should see the following output, or something similar:


    ```bash
        Successfully completed 1 read/write cycle to 'riak@127.0.0.1'
    ```

    If you see a different output to this, your node may be in trouble and this will require further investigation.

## Checking node status

`riak admin status` is a subcommand of the `riak admin` command that is included with every installation of OpenRiak. The status subcommand provides data related to the current operating status for a node. The output of `riak admin status` is extensive.


## Checking cluster status

    You can check the status of your cluster with:

    ```bash
        riak admin cluster status
    ```

    You will see an output that contains your clusters node names, ring status, availability, ring share and any pending transfers:

    ```bash
        ---- Cluster Status ----
        Ring ready: true

        +-----------------------+------+-------+-----+-------+
        |          node         |status| avail |ring |pending|
        +------------------------+------+-------+-----+------+
        | (C) riak@192.168.0.20 |valid |  up   | 20.3|  --   |
        |     riak@192.168.0.21 |valid |  up   | 20.3|  --   |
        |     riak@192.168.0.22 |valid |  up   | 20.3|  --   |
        |     riak@192.168.0.23 |valid |  up   | 20.3|  --   |
        |     riak@192.168.0.24 |valid |  up   | 18.8|  --   |
        +------------------------+------+-------+-----+------+

        Key: (C) = Claimant; availability marked with '!' is unexpected
        ok
    ```

## Checking member status

    You can check the status of all the nodes in your cluster, including pending transfers, the ring % held by each node and the operating status of each node using the following:

    ```bash
        riak admin member status
    ```

    This will produce an output similar to below:

    ```bash
        ================================= Membership ================================
        Status     Ring    Pending    Node
        -----------------------------------------------------------------------------
        valid      20.3%      --      riak@192.168.0.20
        valid      20.3%      --      riak@192.168.0.21
        valid      20.3%      --      riak@192.168.0.22
        valid      20.3%      --      riak@192.168.0.23
        valid      18.8%      --      riak@192.168.0.24
        -----------------------------------------------------------------------------
        Valid:5 / Leaving:0 / Exiting:0 / Joining:0 / Down:0
        ok
    ```
    
## Checking ring status

    You can check the status of your clusters ring with:

    ```bash
        riak admin ring-status
    ```
    
    You will see an output similar to below:

    ```bash
        ================================== Claimant ===================================
        Claimant:  'riak@192.168.56.20'
        Status:     up
        Ring Ready: true

        ============================== Ownership Handoff ==============================
        No pending changes.

        ============================== Unreachable Nodes ==============================
        All nodes are up and reachable

        ok
    ```

    If there are changes happening, such as a node leaving or joining, or if a node is down, it will show the status here.

## Checking with riak-debug

The `riak-debug` command can be used to identify and diagnose common problems with your OpenRiak KV nodes. The command runs a series of operations to collect data, logs and information, condensing it all into a compressed folder for you to extract and review.

> [!NOTE]
>Extensive use of `riak-debug` as part of regular monitoring is not recommended as it can lead to overloads if a node is already in an unhealthy state. Operators should utilise alternative methods listed in this document to inspect their node regularly.

You can see an example of the use of `riak-debug` and the output from the command below:

    ```bash
        $ riak-debug
        ..........EEEEE.......EE................ /usr/lib64/riak/riak@127.0.0.1-riak-debug.tar.gz
    ```

