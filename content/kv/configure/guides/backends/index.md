---
sidebar_position: 201
title: How to Choose a Backend
sidebar_label: Backends
sidebar_custom_props:
  icon: settings
pagination_label: Backends
sidebar_class_name: kv-configure-guides-backends
linkFromConfigNames:
  - "backend_storage"
  - "bitcask.*"
  - "leveled.*"
  - "memory_backend.*"
  - "multi_backend.*"
  - "leveldb.*"
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';

[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

[choosing backend]: #how-to-choose-a-backend
[config reference]: #quick-config-reference
[bitcask]: #bitcask
[leveldb]: #leveldb
[leveled]: #leveled
[memory]: #memory
[multi]: #multi
[prefix multi]: #prefix_multi

<ConfigReferenceProvider configNamePattern='^(storage_backend).*'>

## How to Choose a Backend

OpenRiak KV comes with several different backends with different performance characteristics.

The default backend is <ConfigDefaultValue name="storage_backend" />, but you should give strong consideration to changing it based on the advice in this Guide. Our recommendation is `leveled` (see [How to Configure the Leveled Backend](./configure-leveled)).

## Recommended Configuration

  ```ini
    ## Set OpenRiak KV to use the "leveled" storage backend

  ```bash
    storage_backend = leveled
  ```

## Quick Config Reference

The configuration options relating to the all storage backends are listed below.

<ConfigListing />

## Bitcask

See: [How to Configure the Bitcask Backend](./backends/configure-leveldb)

  ```ini
    ## Set OpenRiak KV to use the "bitcask" storage backend
    storage_backend = bitcask
  ```

  In addition to this setting, there are several other configuration values that can be set to configure and tune the Bitcask backend. You can learn more in the [relevant guide](./configure-bitcask).

## LevelDB

  See: [How to Configure the LevelDB Backend](./backends/configure-leveldb)

  ```ini
    ## Set OpenRiak KV to use the "leveldb" storage backend
    storage_backend = leveldb
  ```

  In addition to this setting, there are several other configuration values that can be set to configure and tune the LevelDB backend. You can learn more in the [relevant guide](./configure-leveldb).

## Leveled

  See: [How to Configure the Leveled Backend](./backends/configure-leveled')

  ```ini
    ## Set OpenRiak KV to use the "leveled" storage backend
    storage_backend = leveled
  ```

  In addition to this setting, there are several other configuration values that can be set to configure and tune the Leveled backend. You can learn more in the [relevant guide](./configure-leveled).

## Memory

  See: [How to Configure the Memory Backend](./backends/configure-leveldb)

  ```ini
    ## Set OpenRiak KV to use the "memory" storage backend
    storage_backend = memory
  ```

  In addition to this setting, there are several other configuration values that can be set to configure and tune the memory backend. You can learn more in the [relevant guide](./configure-memory).


## Multi

  See: [How to Configure the Multi Backend](./backends/configure-leveldb)

  ```ini
    ## Set OpenRiak KV to use multiple backends
    storage_backend = multi
  ```

  This is an advanced option, and allows you to create multiple backends of the same or different types. Each backend can be configured individually.

  Each bucket type will need a property to tell it which backend to use.

  In addition to this setting, you must set other configuration values to configure and tune the multiple backends you create. You can learn more in the [relevant guide](./configure-multi).

## Prefix_Multi

  See: [How to Configure the Prefix_Multi Backend](./configure-prefix_multi).

  ```ini
    ## Set OpenRiak KV to use multiple backends with automatic backend selection
    storage_backend = prefix_multi
  ```

  This is an advanced option, and allows you to create multiple backends of the same or different types. Each backend can be configured individually.

  As part of the configuration, you can define which backend should be used based on bucket name.

  In addition to this setting, you must set other configuration values to configure and tune the multiple backends you create. You can learn more in the [relevant guide](./configure-prefix_multi).


</ConfigReferenceProvider>