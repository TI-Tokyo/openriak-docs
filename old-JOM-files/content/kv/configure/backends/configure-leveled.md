---
sidebar_position: 204
title: How to Configure the Leveled Backend
sidebar_label: Leveled Backend
sidebar_custom_props:
  icon: settings
pagination_label: Configure Leveled
sidebar_class_name: kv-configure-backends-leveled
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }           from '@site/src/components/ConfigReference/ConfigListing';
import ChosenOS                    from '@site/src/components/OSSelection/ChosenOS';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[howconfigure]: #how-to-configure-leveled
[recommendations]: #recommended-settings
[quickref]: #quick-config-reference
<ConfigReferenceProvider configNamePattern='^(storage_backend|leveled\.|platform_data_dir).*'>

## How to Configure Leveled

Leveled is included with OpenRiak KV 3.2.5 onwards, so to enable it, you just need to change the following:

  ```bash
    storage_backend = leveled
  ```

>[!NOTE]Note on replacing an existing backend
>If you replace the existing specified backend by removing it or commenting it out as shown in the above example, data belonging to the previously specified backend will still be preserved on the filesystem but will no longer be accessible through OpenRiak unless the backend is enabled again.
>If you require multiple backends in your configuration, please consult the [Multi-backend(: ../../configure/backends/configure-multi)] documentation.

Leveled’s default behavior can be modified by adding/changing parameters in the leveled section of the `riak.conf` file.
The configuration values that ca nbe set or changed in your `riak.conf` file are:

  |--------------------------------------|-------------------------------------------------------------------------|----------------|
  | Config                               | Description                                                             | Default        |
  |--------------------------------------|-------------------------------------------------------------------------|----------------|
  | leveled.data_root                    | leveled data root.                                                      | ./data/leveled |
  | leveled.sync_strategy                | Strategy for flushing data to disk.                                     | none           |
  | leveled.compression_method           | Compression Method.                                                     | native         |
  | leveled.compression_point            | Compression Point - when compression is applied to the Journal.         | on_receipt     |
  | leveled.log_level                    | Log Level - minimum log level used within leveled.                      | info           |
  | leveled.journal_size                 | Approximate size (bytes) when a Journal file should be rolled.          | 1000000000     |
  | leveled.compaction_runs_perday       | Number of journal compactions per vnode per day.                        | 24             |
  | leveled.compaction_low_hour          | Hour of the day journal compaction can start.                           | 0              |
  | leveled.compaction_top_hour          | Hour of the day after which journal compaction should stop.             | 23             |
  | leveled.max_run_length               | Max Journal Files Per Compaction Run.                                   | 4              |
  |--------------------------------------|-------------------------------------------------------------------------|----------------|

## Recommended Configuration

  The defaults for Leveled are designed for most use-cases. As such, you only need to set these two values:

  ```bash
    storage_backend = leveled
    leveled.data_root = "$(platform_data_dir)/leveled"
  ```

### Block Device Scheduler

Beginning with the 2.6 kernel, Linux gives you a choice of four I/O elevator models. We recommend using the NOOP elevator. You can do this by changing the scheduler on the Linux boot line: `elevator=noop`.

### No Entropy

If you are using https protocol, the 2.6 kernel is widely known for stalling programs waiting for SSL entropy bits. If you are using https, we recommend installing the [HAVEGE](https://www.irisa.fr/caps/projects/hipsor/) package for pseudorandom number generation.

### clocksource

We recommend setting `clocksource=hpet` on your Linux kernel’s `boot` line. The TSC clocksource has been identified to cause issues on machines with multiple physical processors and/or CPU throttling.

### swappiness

We recommend setting `vm.swappiness=0` in `/etc/sysctl.conf`. The `vm.swappiness` default is 60, which is aimed toward laptop users with application windows. This was a key change for MySQL servers and is often referenced in database performance literature.

>[!NOTE]
>`$(platform_data_dir)` will be replaced at run-time with the value for the configuration setting `platform_data_dir`. This varies by operating system. For <ChosenOS type="plaintext" /> the default is <ConfigDefaultValue name="platform_data_dir" hidePlatform="true" />.
>

## Quick Config Reference

The configuration options relating to the Leveled storage backend are listed below.

<ConfigListing />
</ConfigReferenceProvider>