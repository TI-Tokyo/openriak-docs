---
sidebar_position: 1
title: Bitcask backend
sidebar_label: Bitcask
pagination_label: Planning
sidebar_class_name: kv-setup-plan
date: 2025-09-25
---
[configuring-bitcask]: : ../../setup/install/plan/choosing-a-backend/bitcask

## Contents

1. Introduction
2. Strengths
3. Weaknesses
4. Installing and enabling
5. Configuring Bitcask

## Introduction

Bitcask is an erlang-based application that provides fast access via an API for storage & retrival of key/value data using log-structured hash tables.

## Strengths

* Low per-item read/write latency due to write-once, append only nature of bitcask.

* High throughput - Bitcask write operations saturate I/O and disk bandwith, This saturation happens for two key reasons: 1. Bitcask writes data without requiring it to be ordered on disk, and 2. its log-structured architecture minimizes disk head movement during write operations.

* Single seek to retrieve any value

  Bitcask’s in-memory hash table of keys points directly to locations on disk where the data lives. Bitcask never uses more than one disk seek to read a value and sometimes even that isn’t necessary due to filesystem caching done by the operating system.

* Predictable performance for both lookup and insert operations.

* Fast, bounded crash recovery

  Crash recovery is easy and fast with Bitcask because Bitcask files are append only and write once. The only items that may be lost are partially written records at the tail of the last file that was opened for writes. Recovery operations need to review only the last record or two written and verify CRC data to ensure that the data is consistent.

* Easy backup

  Bitcasks append-only, write-once format makes backups easy and simple for any backup utility that copies files in disk-block order.

## Weaknesses

* Keys must fit in memory

The major weaknesses for Bitcask is that it keeps all the keys in memory at all times, which means the system must have enough memory for the entire keyspace plus the required amount for the operating system and other system components.

## Installing and enabling

OpenRiak comes packaged with Bitcask and is the default backend for OpenRiak. You can verify that Bitcask is currently being used as the storage backend by checking the `riak.conf` file for the following line:

```
storage_backend = bitcask
```

If the value of `storage_backend` does not match above, then OpenRiak is not using Bitcask as it's backend.

### Note: If you replace the existing specified backend by removing it or commenting it out as shown in the above example, data belonging to the previously specified backend will still be preserved on the filesystem but will no longer be accessible through Riak unless the backend is enabled again.

You can also use the following command to check this value for a single node or all nodes in a cluster:

```bash
$ sudo riak admin show storage_backend
```

The output for a single node should appear as follows:

```
+--------------+-----------------------+
|     node     |    storage_backend    |
+--------------+-----------------------+
|riak@127.0.0.1|riak_kv_bitcask_backend|
+--------------+-----------------------+

ok
```

To check the value on every node, you need to add the -all flag as follows:

```bash
$ sudo riak admin show storage_backend -all
```

```
+--------------+-----------------------+
|     node     |    storage_backend    |
+--------------+-----------------------+
|riak@127.0.0.1|riak_kv_bitcask_backend|
+--------------+-----------------------+
|riak@127.0.0.2|riak_kv_bitcask_backend|
+--------------+-----------------------+
|riak@127.0.0.3|riak_kv_bitcask_backend|
+--------------+-----------------------+
|riak@127.0.0.4|riak_kv_bitcask_backend|
+--------------+-----------------------+
|riak@127.0.0.5|riak_kv_bitcask_backend|
+--------------+-----------------------+

ok
```

## Configuring Bitcask

The following are the default Bitcask configuration values available in `riak.conf`. Additional options are available, which are in the [configuring bitcask][configuring-bitcask] section.

```
bitcask.data_root = ./data/bitcask
bitcask.io_mode = erlang
```


