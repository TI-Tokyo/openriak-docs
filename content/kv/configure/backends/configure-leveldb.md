---
sidebar_position: 203
title: How to Configure the LevelDB Backend
sidebar_label: LevelDB Backend
sidebar_custom_props:
  icon: settings
pagination_label: Configure LevelDB
sidebar_class_name: kv-configure-backends-leveldb
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }           from '@site/src/components/ConfigReference/ConfigListing';
import ChosenOS                    from '@site/src/components/OSSelection/ChosenOS';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[howconfigure]: #how-to-configure-leveldb
[quickref]: #quick-config-reference
<ConfigReferenceProvider configNamePattern='^(storage_backend|leveldb\.).*'>


## How to Configure LevelDB

To enable levelDB in your `riak.conf` file, you need to chane the `storage_backend` value of your `riak.conf` file to the following:

  ```bash
    storage_backend = leveldb
  ```

LevelDB's default values can be adjusted by adding/changing the following values in the leveldb section of the `riak.conf`.

The configuration values that can be set in your riak.conf for eLevelDB are as follows:

  ```bash
    leveldb.data_root = ./data/leveldb
    leveldb.maximum_memory.percent = 70 # (default)
  ```

Additional Configuration values are available and can be added to your `riak.conf` file in the quick reference section later in this page.

## Recommended settings


## Quick Config Reference

The configuration options relating to the LevelDB storage backend are listed below.

<ConfigListing />
</ConfigReferenceProvider>