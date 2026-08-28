---
sidebar_position: 205
title: How to Configure the Memory Backend
sidebar_label: Memory Backend
sidebar_custom_props:
  icon: settings
pagination_label: Configure Memory
sidebar_class_name: kv-configure-backends-memory
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }           from '@site/src/components/ConfigReference/ConfigListing';
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[howconfigure]: #how-to-configure-memory
[recommendations]: #recommended-settings
[quickref]: #quick-config-reference

<ConfigReferenceProvider configNamePattern='^(storage_backend|memory_backend\.).*'>

## How to Configure Memory

Memory backend is including by default with OpenRiak KV, so to enable it, you just need to change the following:

  ```bash
    storage_backend = memory
  ```

> [!NOTE]Note on replacing an existing backend
> If you replace the existing specified backend by removing it or commenting it out as shown in the above example, data belonging to the previously specified backend will still be preserved on the filesystem but will no longer be accessible through OpenRiak unless the backend is enabled again.
> If you require multiple backends in your configuration, please consult the [Multi-backend(: ../../configure/backends/configure-multi)] documentation.

## Max memory

The Max memory setting allows you to specify the maximum amount of memory that can be used by the Memory backend. This functions on a per-vnode basis, not on a per-node or per-cluster basis. This should be accounted for when calculating memory usage with the Memory backend, as the total memory used will be MM (max memory) times the number of vnodes in the cluster.

When the threshold value that you set has been met in a particular vnode, OpenRiak will begin discarding objects, beginning with the oldest object and proceeding until memory usage returns below the allowable threshold.

You can configure maximum memory using the following methods depending on your prefered method:

  ```bash
    memory_backend.max_memory_per_vnode = 500KB
    memory_backend.max_memory_per_vnode = 10MB
    memory_backend.max_memory_per_vnode = 2GB
  ```

## Time-to-live (TTL)

The time-to-live (TTL) configuration value defines the amount of time an object remains in memory before it expires. The minimum time is one second.

You can define the TTL in seconds, minutes or hours, depending on your needs and prefence as follows:

  ```bash
    memory_backend.ttl = 1s
    memory_backend.ttl = 10m
    memory_backend.ttl = 3h
  ```

## Quick Config Reference

The configuration options relating to the Memory storage backend are listed below.

<ConfigListing />
</ConfigReferenceProvider>