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
[recommendations]: #recommended-settings
[quickref]: #quick-config-reference
<ConfigReferenceProvider configNamePattern='^(storage_backend|leveldb\.).*'>

## How to Configure LevelDB

To enable levelDB in your `riak.conf` file, you need to chane the `storage_backend` value of your `riak.conf` file to the following:

  ```bash
    storage_backend = leveldb
  ```

>[!NOTE]Note on replacing an existing backend
>If you replace the existing specified backend by removing it or commenting it out as shown in the above example, data belonging to the previously specified backend will still be preserved on the filesystem but will no longer be accessible through OpenRiak unless the backend is enabled again.
>If you require multiple backends in your configuration, please consult the [Multi-backend(: ../../configure/backends/configure-multi)] documentation.

LevelDB's default values can be adjusted by adding/changing the following values in the leveldb section of the `riak.conf`.

The configuration values that can be set in your riak.conf for eLevelDB are as follows:

  ```bash
    leveldb.data_root = ./data/leveldb
    leveldb.maximum_memory.percent = 70 # (default)
  ```

Additional Configuration values are available and can be added to your `riak.conf` file in the quick reference section later in this page.

## Recommended settings

### Block Device Scheduler

Beginning with the 2.6 kernel, Linux gives you a choice of four I/O elevator models. We recommend using the NOOP elevator. You can do this by changing the scheduler on the Linux boot line: `elevator=noop`.

### ext4 filesystem Options

The ext4 filesystem defaults include two options that increase integrity but slow performance. Because OpenRiak’s integrity is based on multiple nodes holding the same data, these two options can be changed to boost LevelDB’s performance. We recommend setting: `barrier`=0 and `data`=writeback.

### CPU Throttling

If CPU throttling is enabled, disabling it can boost LevelDB performance in some cases.

### No Entropy

If you are using https protocol, the 2.6 kernel is widely known for stalling programs waiting for SSL entropy bits. If you are using https, we recommend installing the [HAVEGE](https://www.irisa.fr/caps/projects/hipsor/) package for pseudorandom number generation.

### clocksource

We recommend setting `clocksource=hpet` on your Linux kernel’s `boot` line. The TSC clocksource has been identified to cause issues on machines with multiple physical processors and/or CPU throttling.

### swappiness

We recommend setting `vm.swappiness=0` in `/etc/sysctl.conf`. The `vm.swappiness default` is 60, which is aimed toward laptop users with application windows. This was a key change for MySQL servers and is often referenced in database performance literature.

## Quick Config Reference

The configuration options relating to the LevelDB storage backend are listed below.

<ConfigListing />
</ConfigReferenceProvider>