---
sidebar_position: 202
title: How to Configure the Bitcask Backend
sidebar_label: Bitcask Backend
sidebar_custom_props:
  icon: settings
pagination_label: Configure Bitcask
sidebar_class_name: kv-configure-guides-backends-bitcask
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }           from '@site/src/components/ConfigReference/ConfigListing';
import ChosenOS                    from '@site/src/components/OSSelection/ChosenOS';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';

[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[howconfigure]: #how-to-configure-bitcask
[opentimeout]: #open-timeout
[maxsize]: #max-file-size
[hintfiles]: #hint-file-crc-check
[I/Omode]: #io-mode
[osync]: #o_sync-on-linux
[policy]: #merge-policy
[thresholds]: #merge-thresholds
[interval]: #merge-interval
[foldthreshold]: #fold-keys-threshold
[expiration]: #automatic-expiration

<ConfigReferenceProvider configNamePattern='^(storage_backend|bitcask\.).*'>

## How to Configure Bitcask

The default configuration values for Bitcask are as follows:

  ```bash
    bitcask.data_root = ./data/bitcask
    bitcask.io_mode = erlang
  ```

Bitcask is the Default backend for OpenRiak currently, so there is no need to make any changes to your `riak.conf` file to run it on first start.

All of the other available settings listed below can be added to your `riak.conf file`.

### Open Timeout

The open timeout setting specifies the maximum time Bitcask will block on startup while attempting to create or open the Bitcask data directory. The default is 4 seconds.

In general, you will not need to adjust this setting. If, however, you begin to receive log messages of the form `Failed to start bitcask backend: ...`, you may want to consider using a longer timeout.

Open timeout is specified using the `bitcask.sync.open_timeout` parameter, and can be set in terms of seconds, minutes, hours, etc. The following example sets the parameter to 10 seconds:

  ```
    bitcask.sync.open_timeout = 10s
  ```
### Sync Strategy

Bitcask allows you to configure the durability of writes by defining when to synchronize data to disk, this is known as a Sync Strategy. By default, this is set to `none` which means that the data will be written to disk when the Operating System flushes it's buffers. The risk with this setting is that if the system fails for any reasons (such as sudden power loss), then any data left in those buffers is lost.
This means that the default setting of `none` will protect against data loss due to appliation failure, but leaves a small chance that data could be lost in the event of complete system failure (hardware or software).

You can prevent the above scenario by choosing the `o_sync` strategy instead. This strategy forces the Operating System to flush any data to disk at write time for every write. This will allow for more durability in your data, but will slow the write throughput as each write will have to wait for it to be written to disk.

The following sync strategies are available:

  * `none` - lets the operating system manage syncing writes (default)
  * `o_sync` - uses the O_SYNC flag, which forces syncs on every write
  * `Time interval` - OpenRiak will force Bitcask to sync at specified interval

In addition to Strategys, you can define the sync interval, which controls how often Bitcask forces a write to disk, with the following:

  ```bash
    bitcask.sync.interval = 65s
  ```

>[NOTE!]Note on Sync Strategy Interval Limitations
>Setting the sync interval to a value lower or equal to `riak_core.vnode_inactivity_timeout` (default: 60 seconds), will prevent OpenRiak from performing handoffs.
>A vnode must be inactive (not receive any messages) for a certain amount of time before the handoff process can start. The sync mechanism causes a message to be sent to the vnode for every sync, thus preventing the vnode from ever becoming inactive.

The following are possible configurations:

  ```bash
    bitcask.sync.strategy = none
    bitcask.sync.strategy = o_sync
    bitcask.sync.strategy = interval
    bitcask.sync.interval = 65s
  ```

### Max file size

The `max_file_size` setting describes the maximum permitted size for any single data file in the Bitcask directory. If a write causes the current file to exceed this size threshold then that file is closed, and a new file is opened for writes. The default is 2 GB.

Increasing `max_file_size` will cause Bitcask to create fewer, larger files that are merged less frequently, while decreasing it will cause Bitcask to create more numerous, smaller files that are merged more frequently.

To give an example, if your ring size is 16, your servers could see as much as 32 GB of data in the bitcask directories before the first merge is triggered, irrespective of your working set size. You should plan storage accordingly and be aware that it is possible to see disk data sizes that are larger than the working set.

The `max_file_size` setting can be specified using kilobytes, megabytes, etc. The following example sets the max file size to 1 GB:

  ```bash
    bitcask.max_file_size = 1GB
  ```

### Hint File CRC check

During startup, Bitcask will read from `.hint` files in order to build its in-memory representation of the key space, falling back to `.data` files if necessary. This reduces the amount of data that must be read from the disk during startup, thereby also reducing the time required to start up. You can configure Bitcask to either disregard .hint files that don’t contain a CRC value or to use them anyway.

If you are using the newer, r`iak.conf`-based configuration system, you can instruct Bitcask to disregard .hint files that do not contain a CRC value by setting the `hintfile_checksums` setting to `strict` (the default). To use Bitcask in a backward-compatible mode that allows for `.hint` files without CRC signatures, change the setting to `allow_missing`.

The following example sets the parameter to strict:

```bash
bitcask.hintfile_checksums = strict
```

### I/O Mode

The `io_mode` setting specifies which code module Bitcask should use for file access. The available settings are:

  * `erlang` (default) - Writes are made via Erlang’s built-in file API
  * `nif` - Writes are made via direct calls to the POSIX C API

The following example sets io_mode to erlang:

  ```bash
    bitcask.io_mode = erlang
  ```

In general, the `nif` IO mode provides higher throughput for certain workloads, but it has the potential to negatively impact the Erlang VM, leading to higher worst-case latencies and possible throughput collapse.

### `O_SYNC` on Linux

Synchronous file I/O via `o_sync` is supported in Bitcask if io_mode is set to `nif` and is not supported in the erlang mode.

If you enable `o_sync` by setting io_mode to nif, however, you will still get an incorrect warning along the following lines:

```bash
[warning] <0.445.0>@riak_kv_bitcask_backend:check_fcntl:429 {sync_strategy,o_sync} not implemented on Linux
```

### Merge Policy

Bitcask enables you to select a merge policy, i.e. when during the day merge operations are allowed to be triggered. The valid options are:

  * `always` - No restrictions on when merge operations can occur (default)
  * `never` - Merge will never be attempted
  * `window` - Merge operations occur during specified hours

If you are using the newer, riak.conf-based configuration system, you can select a merge policy using the merge.policy setting. The following example sets the merge policy to never:

  ```bash
    bitcask.merge.policy = never
  ```

If you opt to specify start and end hours for merge operations, you can do so with the `merge.window.star`t and `merge.window.end` settings in addition to setting the merge policy to window. Each setting is an integer between 0 and 23 for hours on a 24h clock, with 0 meaning midnight and 23 standing for 11 pm. The merge window runs from the first minute of the `merge.window.start` hour to the last minute of the `merge.window.end` hour. The following example enables merging between 3 am and 4:59 pm:

  ```bash
    bitcask.merge.policy = window
    bitcask.merge.window.start = 3
    bitcask.merge.window.end = 17
  ```

>[!NOTE] Note on `merge_window` and the `Multi` backend
>If you are using the older configuration system and using Bitcask with the `Multi` backend, please note that if you wish to use a merge window, you must set it in the global `bitcask` section of your configuration file. `merge_window`settings in per-backend sections are ignored.

If merging has a significant impact on performance of your cluster, or if your cluster has quiet periods in which little storage activity occurs, you may want to change this setting from the default.

A common way to limit the impact of merging is to create separate merge windows for each node in the cluster and ensure that these windows do not overlap. This ensures that at most one node at a time can be affected by merging, leaving the remaining nodes to handle requests. The main drawback of this approach is that merges will occur less frequently, leading to increased disk space usage

### Merge Thresholds

Merge thresholds determine which files will be chosen for inclusion in a merge operation.

  * Fragmentation - This setting describes which ratio of dead keys to total keys in a file will cause it to be included in the merge. The value of this setting is a percentage (0-100). For example, if a data file contains 4 dead keys and 6 live keys, it will be included in the merge at the default ratio (40%). Increasing the value will cause fewer files to be merged, while decreasing the value will cause more files to be merged.

  * Dead Bytes - This setting describes which ratio the minimum amount of data occupied by dead keys in a file to cause it to be included in the merge. Increasing this value will cause fewer files to be merged, while decreasing this value will cause more files to be merged. The default is 128 MB.

  * Small File - This setting describes the minimum size a file must be to be excluded from the merge. Files smaller than the threshold will be included. Increasing the value will cause more files to be merged, while decreasing the value will case fewer files to be merged. The default is 10 MB.

You can set the thresholds described above using the `merge.thresholds.fragmentation`, `merge.thresholds.dead_bytes`, and `merge.threshold.small_file` settings, respectively.

The fragmentation setting is expressed as an integer between 0 and 100, and the dead_bytes and small_file settings can be expressed in terms of kilobytes, megabytes, gigabytes, etc. The following example sets the fragmentation threshold to 45%, the dead bytes threshold to 200 MB, and the small file threshold to 25 MB:

  ```bash
    bitcask.merge.thresholds.fragmentation = 45
    bitcask.merge.thresholds.dead_bytes = 200MB
    bitcask.merge.thresholds.small_file = 25MB
  ```
>[!NOTE]Note on choosing threshold values
> The values for the fragmentation and dead bytes thresholds must be equal to or less than their corresponding trigger values. If they are set higher, Bitcask will trigger merges in cases where no files meet the threshold, which means that Bitcask will never resolve the conditions that triggered merging in the first place.

### Merge Interval

Bitcask periodically runs checks to determine whether merges are necessary. You can determine how often those checks take place using the `bitcask.merge_check_interval` parameter. The default is 3 minutes.

  ```bash
    bitcask.merge_check_interval = 3m
  ```

If merge check operations happen at the same time on different vnodes on the same node, this can produce spikes in I/O usage and undue latency. Bitcask makes it less likely that merge check operations will occur at the same time on different vnodes by applying a jitter to those operations. A jitter is a random variation applied to merge times that you can alter using the `bitcask.merge_check_jitter` parameter. This parameter is expressed as a percentage of `bitcask.merge_check_interval`. The default is 30%.

```bash
bitcask.merge_check_jitter = 30%
```

For example, if you set the merge check interval to 4 minutes and the jitter to 25%, merge checks will occur at intervals between 3 and 5 minutes. With the default of 3 minutes and 30%, checks will occur at intervals between roughly 2 and 4 minutes.

### Fold Keys Threshold
Fold keys thresholds will reuse the keydir (a) if another fold was started less than a specified time interval ago and (b) there were fewer than a specified number of updates. Otherwise, Bitcask will wait until all current fold keys complete and then start. The default time interval is 0, while the default number of updates is unlimited. Both thresholds can be disabled.

The conditions described above can be set using the `fold.max_age` and `fold.max_puts` parameters, respectively. The former can be expressed in terms of minutes, hours, days, etc., while the latter is expressed as an integer. Each threshold can be disabled by setting the value to unlimited. The following example sets the max_age to 1⁄2 second and the max_puts to 1000:

  ```bash
    bitcask.max_age = 0.5s
    bitcask.max_puts = 1000
  ```

### Automatic Expiration

By default, Bitcask keeps all of your data. But if your data has limited time value or if you need to purge data for space reasons, you can configure object expiration, aka expiry. This feature is disabled by default.

You can enable and configure object expiry using the expiry setting and either specifying a time interval in seconds, minutes, hours, etc., or turning expiry off (off). The following example configures objects to expire after 1 day:

  ```bash
    bitcask.expiry = 1d
  ```

>[!NOTE]Note on stale data
>Space occupied by stale data may not be reclaimed immediately, but the data will become immediately inaccessible to client requests. Writing to a key will set a new modification timestamp on the value and prevent it from being expired.

By default, Bitcask will trigger a merge whenever a data file contains an expired key. This may result in excessive merging under some usage patterns. You can prevent this by configuring an expiry grace time. Bitcask will defer trigger a merge solely for key expiry by the configured amount of time. The default is 0, signifying no grace time.

If you are using the newer, riak.conf-based configuration system, you can set an expiry grace time using the expiry.grace_time setting and in terms of minutes, hours, days, etc. The following example sets the grace period to 1 hour:

  ```bash
    bitcask.expiry.grace_time = 1h
  ```

## Recommended Configuration Settings


## Quick Config Reference

The configuration options relating to the Bitcask storage backend are listed below.

<ConfigListing />
</ConfigReferenceProvider>