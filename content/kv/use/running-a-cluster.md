---
title: Running a Cluster
sidebar_label: "Running a Cluster"
date: 2025-11-13
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';
[configure]: #configure-the-first-node
[setipport]: #set-your-listener-ip-address-and-port
[namenode]: #name-your-node
[start]: #start-the-node
[addnode]: #adding-nodes-to-your-cluster



All configuration changes in this document take place in your nodes `riak.conf` file unless otherwise stated.

## Configure the first node

First, stop your Riak node if it is currently running:

    ```bash
        riak stop
    ```

## Set your listener IP address and port

Let’s say that the IP address for your cluster is `192.168.1.10` and that you’ll be using the default port (8087). If you’re using the Protocol Buffers interface to Riak (which we recommend over the HTTP interface due to performance gains), you should change the value of `listener.protobuf.internal` from the default to something resembling the following:

    ```bash
        listener.protobuf.internal = 192.168.1.10:8087
    ```

If you're using the HTTP interact, you will need to change the value of `listener.http.internal` in similar manner as follows:

    ```bash
        listener.http.internal = 192.168.1.10:8098
    ```

## Name your Node

Now that you've sen your listeners, you need to set your node name.
Every node in Riak has a name associated with it. The default name is `riak@127.0.0.1`. Let’s say that you want to change the name to `riak@192.168.1.10`, then you will need to update the value of `nodename` in your `riak.conf` file from the default to the following:

    ```bash
        nodename = riak@192.168.1.10
    ```

>[!NOTE]Note on domain names and IP addresses for node names
> It is strongly recommended to use fully qualified domain names (FQDNs) rather than IP address for cluster node names.

Once a node has been started, in order to change the name you must either remove ring files from the `/data/ring` directory or `riak admin cluster force-replace` the node.

## Start the node

Now that your node is properly configured, you can start it:

```bash
    riak start
```

If the Riak node has been previously started, you must use the `riak admin cluster replace` command to change the node name and update the node’s ring file.

    ```bash
        riak admin cluster replace riak@127.0.0.1 riak@192.168.1.10
    ```

>[!NOTE]Note on single nodes
>If a node is started singly using default settings, as you might do when you are building your first test environment, you will need to remove the ring files from the data directory after you edit your configuration files. riak admin cluster replace will not work since the node has not been joined to a cluster.

As with all cluster changes, you need to view the planned changes by running `riak admin cluster plan` and then running `riak admin cluster commit` to finalize those changes.

The node is now properly set up to join other nodes for cluster participation. You can proceed to adding a second node to the cluster.

## Adding nodes to your cluster

You can repeat the above steps for each new node you are creating. Once you've started your node, you need to stage the node to join the cluster with the following:

    ```bash
        riak admin cluster join riak@192.168.1.11 riak@192.168.1.10
    ```

The first nodename is the name of the new node, the second is the name of the node in the cluster that this new node is joining.

You can add multiple nodes to a cluster at the same time, though with established production clusters, this should be done with care, to avoid overloading the existing nodes with transfers.

Once you've performed the `riak admin cluster join` command on all the new nodes, you can check the staged changes with the following: 

    ```bash
        riak admin cluster plan
    ```

You will see an output similar to below:

    ```bash
        =============================== Staged Changes ================================
        Action         Details(s)
        -------------------------------------------------------------------------------
        join           'riak@192.168.1.11'
        join           'riak@192.168.1.12'
        join           'riak@192.168.1.13'
        join           'riak@192.168.1.14'
        -------------------------------------------------------------------------------


        NOTE: Applying these changes will result in 1 cluster transition

        ###############################################################################
                                 After cluster transition 1/1
        ###############################################################################

        ================================= Membership ==================================
        Status     Ring    Pending    Node
        -------------------------------------------------------------------------------
        valid     100.0%     20.3%    'riak@192.168.1.10'
        valid       0.0%     20.3%    'riak@192.168.1.11'
        valid       0.0%     20.3%    'riak@192.168.1.12'
        valid       0.0%     20.3%    'riak@192.168.1.13'
        valid       0.0%     18.8%    'riak@192.168.1.14'
        -------------------------------------------------------------------------------
        Valid:5 / Leaving:0 / Exiting:0 / Joining:0 / Down:0
    ```

You should always double check that everything is correct before the next step.
Finally you need to run `riak admin cluster commit` which should produce the following output, assuming you've already run `riak admin cluster plan`:

    ```bash
        Cluster changes committed
    ```

The cluster will now  begin transfers to the new node and between existing nodes to rebalance the rings.

To examine your cluster and check the current members, you can use the `riak admin` command line as follows:

    ```bash
        riak admin status | grep ring_members
    ```

You will see an output such as below:

    ```bash
        ring_members : ['riak@192.168.1.10','riak@192.168.1.11','riak@192.168.1.12','riak@192.168.1.13','riak@192.168.1.14']
    ```

Alternatively, you can check via `riak attach` which opens an Erlang shell:

    ```bash
        1> {ok, R} = riak_core_ring_manager:get_my_ring().

        %% Response:

        {ok,{chstate,'riak@192.168.1.10',.........
        (riak@192.168.1.10)2> riak_core_ring:all_members(R).
        ['riak@192.168.1.10','riak@192.168.1.11','riak@192.168.1.12','riak@192.168.1.13','riak@192.168.1.14`]
    ```