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
