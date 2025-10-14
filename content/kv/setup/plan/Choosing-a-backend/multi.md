---
sidebar_position: 5
title: Multi backend
sidebar_label: Multi
pagination_label: Planning
sidebar_class_name: kv-setup-plan
date: 2025-10-13
---

# Contents
1. [Introduction](#introduction)
2. [Enabling Multiple backends](#enabling-multiple-backends)
3. [Configuring multiple backends](#configuring-multiple-backends)

# Introduction 

OpenRiak allows you to run multiple backends within a single OpenRiak cluster. Selecting the Multi backend enables you to use different storage backends for different buckets. Any combination of the three available backends — Bitcask, LevelDB, and Memory can be used.


# Enabling Multiple Backends

You can enable Multi backend by changing the value of `storage_backend` in your `riak.conf` file to the following:

```bash
storage_backend = multi
```

# Configuring multiple Backends

Once you've enabled multiple backends, you need to configure each backend on its own. All the normal configuration options for a chosen memory backend are available to your when using multi-backend.

Here is an example of the general form for configuring multiple backends:

```riak.conf
multi_backend.$name.$setting_name = setting
```

If you are using, for example, the LevelDB and Bitcask backends and wish to set LevelDB’s `bloomfilter` setting to off and the Bitcask backend’s `io_mode` setting to nif, you would do that as follows:

```riak.conf
multi_backend.leveldb.bloomfilter = off
multi_backend.bitcask.io_mode = nif
```

# Using Multiple Backends

In OpenRiak 3.2.5 and later, we recommend using multiple backends by applying them to buckets using [bucket types](). Assuming that the cluster has already been configured to use the multi backend, this process involves three steps:

1. Creating a bucket type that enables buckets of that type to use the desired backends
2. Activating that bucket type
3. Setting up your application to use that type

Let’s say that we’ve set up our cluster to use the Multi backend and we want to use LevelDB and the Memory backend for different sets of data. First, we need to create two bucket types, one which sets the backend bucket property to leveldb and the other which sets that property to memory. All bucket type-related activity is performed through the [riak admin][use admin riak admin cli] command interface.

We’ll call our bucket types `leveled_backend` and `memory_backend`, but you can use whichever names you wish.

```bash
riak admin bucket-type create leveled_backend '{"props":{"backend":"leveled"}}'
riak admin bucket-type create memory_backend '{"props":{"backend":"memory"}}'
```

Then we need to activate those bucket types so they can be used in the cluster:

```bash
riak admin bucket-type activate leveled_backend
riak admin bucket-type activate memory_backend
```

Once those types have been activated, any objects stored in buckets bearing the type `leveled_backend` will be stored in Leveled, whereas all objects stored in buckets of the type memory_backend will be stored in the Memory backend.

More information can be found in our documentation on using [bucket types]()

