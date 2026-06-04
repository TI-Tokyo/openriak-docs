---
sidebar_position: 4
title: Memory backend
sidebar_label: Memory
pagination_label: Planning
sidebar_class_name: kv-setup-plan
date: 2026-06-04
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[strengths]: #strengths
[weaknesses]: #weaknesses
[installenable]: #installing-and-enabling
[confiuring]: #configuring-memory-backend

[configuring-memory]: : ../../setup/install/plan/choosing-a-backend/memory

>[!MEMO]Introduction to Memory backend

The Memory storage backend relies entirely on in-memory tables to hold data, which means nothing is ever saved to disk or any other storage medium. It's ideally suited for testing Riak clusters or managing small, temporary data in live production environments. It is generally not recommended for long-term data storage use in production.

## Weaknesses

1. Memory backend means all data is store in-memory, nothing is saved to disk, so a sudden loss of power or hardware failure could lead to significant/total data loss.

## Installing and enabling

OpenRiak comes packaged with memory backend, so there is no need for further steps to install it.

You can select memory as your backend by changing the value of `storage_backend` in your `riak.conf` file to `memory` as it appears below:

    ```bash
        storage_backend = memory
    ```

### Note: If you replace the existing specified backend by removing it or commenting it out as shown in the above example, data belonging to the previously specified backend will still be preserved on the filesystem but will no longer be accessible through Riak unless the backend is enabled again.

 You can verify that memory is currently being used as the storage backend on an active cluster by checking the `riak.conf` file for the following line:

    ```bash
        storage_backend = memory
    ```

If the value of `storage_backend` does not match above, then OpenRiak is not using memory as it's backend.

You can also use the following command to check this value for a single node or all nodes in a cluster:

    ```bash
        $ sudo riak admin show storage_backend
    ```

The output for a single node should appear as follows:

    ```bash
        +--------------+-----------------------+
        |     node     |    storage_backend    |
        +--------------+-----------------------+
        |riak@127.0.0.1|riak_kv_memory_backend|
        +--------------+-----------------------+

        ok
    ```

To check the value on every node, you need to add the -all flag as follows:

    ```bash
        $ sudo riak admin show storage_backend -all
    ```

    ```bash
        +--------------+-----------------------+
        |     node     |    storage_backend    |
        +--------------+-----------------------+
        |riak@127.0.0.1|riak_kv_memory_backend|
        +--------------+-----------------------+
        |riak@127.0.0.2|riak_kv_memory_backend|
        +--------------+-----------------------+
        |riak@127.0.0.3|riak_kv_memory_backend|
        +--------------+-----------------------+
        |riak@127.0.0.4|riak_kv_memory_backend|
        +--------------+-----------------------+
        |riak@127.0.0.5|riak_kv_memory_backend|
        +--------------+-----------------------+

        ok
    ```

## Configuring memory backend

The Memory backend enables you to configure two fundamental aspects of object storage: maximum memory usage per vnode and object expiry.

### Max Memory

The Max Memory defines on a per-vnode basis, how much memory is consumed by the Memory backend. The fact that it is per-vnode and not per-node or per-cluster is important when planning memory usage, as the total memory used will be the value of max memory time the nubmer of vnodes in the cluster.
If the threshold for max meory is hit for a vnode, then OpenRiak will start discarding objects, starting from the oldest and moving forward from there until the vnode drops below the threshold.

You can configure maximum memory using the `memory_backend.max_memory_per_vnode` setting. You can specify `max_memory_per_vnode` however you’d like, using kilobytes, megabytes, or even gigabytes.

The following are all possible settings:

    ```bash
        memory_backend.max_memory_per_vnode = 500KB
        memory_backend.max_memory_per_vnode = 10MB
        memory_backend.max_memory_per_vnode = 2GB
    ```

### Time-To-Live (TTL)

The time-to-live (TTL) parameter specifies the amount of time an object remains in memory before it expires. The minimum time is one second. You can specify the value in seconds, minutes, hours, days etc. The following are possible values for the parameters:

    ```bash
        memory_backend.ttl = 1s
        memory_backend.ttl = 10m
        memory_backend.ttl = 3h
        memory_backend.ttl = 1d
    ```
