---
sidebar_position: 2
title: Changing the backend
sidebar_label: "Change backend"
date: 2026-06-03
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[assumptions]: #assumptions
[method1]: #method-1---changing-the-backend-on-an-empty-node
[method2]: #method-2---changing-the-backend-on-an-established-node-in-a-cluster

>[!MEMO] This section will provide instructions on how to switch the backend on an OpenRiak node/cluster.
>In this tutorial we will be demonstrating two methods for changing backends. The first method is for a node with zero data stored on it and the second is for nodes with data stored in an active cluster.

>[!NOTE]Note on the effect of changing backends in a cluster with data.
>When you change backends on a production cluster, it will start with zero data. The existing data will still be stored under the old backend, but will be unavailable until the original backend is enabled.


## Method 1 - Changing the backend on an empty node

To change the backend of a node that already exists but has no data and is not part of a cluster, the process is very simple.

1. Stop the node with `riak stop`.

2. Open the `riak.conf` file in your preferred text editor.

3. Change the following line:

    ```bash

        storage_backend = leveled

    ```

To the required new backend, in this case it will be bitcask:

    ```bash

        storage_backend = bitcask

    ```

4. Start the node again with `riak start` or `riak daemon`.

5. Once the node has started, you can check the backend with the following steps:

    5a. Run the following:
        
        ```bash
            riak attach
        ```
    
    5b. Enter the following command:

        ```bash
            application:get_env(riak_kv, storage_backend).
        ```

    5c. The output should appear similar to below:

        ```
            {ok,riak_kv_bitcask_backend}
        ```

6. That's it! you've now switched the node to a new backend.

## Method 2 - Changing the backend on an established node in a cluster

Switching backends on an established node/cluster is relatively simple process called a "Rolling Replace". This process will replace every node in the cluster, one at a time. To perform this function, you will also need a single extra node, of a similar specification & configuration to the old ones, but with the new backend set in the `riak.conf` file, by changing the value of `storage_backend = bitcask` to whatever backend you have selected.

To perform a rolling replace of all nodes in the cluster, follow these steps:

1. Configure the new node with the correct settings for your cluster, but the new backend set.

2. Join it to the cluster using:

    ```bash
        riak admin cluster join
    ```

>[!NOTE]For full details on adding or removing nodes see [add/remove](..\add-remove-node.md)

3. Set the node to replace the existing node of your choice with:

    ```bash
        riak admin cluster replace <old node name> <new node name>
    ```

This should produce an output similar to:

    ```bash
        Success: staged replacement of 'riak@192.168.0.22' with 'riak@192.168.0.21'
        ok
    ```

4. Check the plan with with:

    ```bash
        riak admin cluster plan
    ```
    
    which should produce an output similar to:

    ```bash
        =============================== Staged Changes ================================
        Action         Details(s)
        -------------------------------------------------------------------------------
        join           'riak@192.168.0.21'
        replace        'riak@192.168.0.22' with 'riak@192.168.0.21'
        -------------------------------------------------------------------------------


        NOTE: Applying these changes will result in 2 cluster transitions

        ###############################################################################
                                 After cluster transition 1/2
        ###############################################################################

        ================================= Membership ==================================
        Status     Ring    Pending    Node
        -------------------------------------------------------------------------------
        leaving    25.0%      0.0%    riak@192.168.0.22
        valid      25.0%     25.0%    riak@192.168.0.20
        valid       0.0%     25.0%    riak@192.168.0.21
        valid      25.0%     25.0%    riak@192.168.0.23
        valid      25.0%     25.0%    riak@192.168.0.24
        -------------------------------------------------------------------------------
        Valid:4 / Leaving:1 / Exiting:0 / Joining:0 / Down:0

        Transfers resulting from cluster changes: 16
          16 transfers from 'riak@192.168.0.22' to 'riak@192.168.0.21'

        ###############################################################################
                                 After cluster transition 2/2
        ###############################################################################

        ================================= Membership ==================================
        Status     Ring    Pending    Node
        -------------------------------------------------------------------------------
        valid      25.0%      --      riak@192.168.0.20
        valid      25.0%      --      riak@192.168.0.21
        valid      25.0%      --      riak@192.168.0.23
        valid      25.0%      --      riak@192.168.0.24
        -------------------------------------------------------------------------------
        Valid:4 / Leaving:0 / Exiting:0 / Joining:0 / Down:0

        ok
    ```

As you can see from the above, the planned sequence of events is:

    4a. Node riak@192.168.0.21 joins the cluster
    4b. Node riak@192.168.0.21 receives transfers from node riak@192.168.0.22
    4c. Node riak@192.168.0.22 leaves the cluster, with node riak@192.168.0.21 taking it's place in the ring.

If your plan looks correct, then you can commit with:

    ```bash
        riak admin cluster commit
    ```

Which will produce the following output:

    ```bash
            Cluster changes committed
        ok
    ```

You will then need to monitor transfers until the complete with the following:

    ```bash
        riak admin transfers
    ```

When the output of that command shows the following, the process is completed.

    ```bash
            No transfers active

            Active Transfers:

    
        ok
    ```

5. Once transfers are completed, you can now use the node that was replaced to replace the next node in the cluster, repeating the process down the line for each node in the cluster.

6. Once all the nodes have been replaced, that's it! You have completed a full rolling replace of all nodes in the cluster with the new backed in place.

