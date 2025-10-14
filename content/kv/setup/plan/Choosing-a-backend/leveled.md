---
sidebar_position: 3
title: Leveled backend
sidebar_label: Leveled
pagination_label: Planning
sidebar_class_name: kv-setup-plan
date: 2025-10-01
---
[configuring-leveled]: : ../../setup/install/plan/choosing-a-backend/leveled

# Contents

1. [Introduction](#introduction)
2. [Strengths](#strengths)
3. [weaknesses](#weaknesses)
4. [Installing and enabling](#installing-and-enabling)
5. [Configuring leveled](#configuring-leveled)

# Introduction

(Leveled)[https://github.com/martinsumner/leveled] is an open source project that has been developed specifically as a backend option for Riak/OpenRiak, rather than a generic backend.

(Leveled)[https://github.com/martinsumner/leveled] is a simple Key-Value store based on the concept of Log-Structured Merge Trees, with the following characteristics:

* Optimised for workloads with larger values (e.g. > 4KB).
* Explicitly supports HEAD requests in addition to GET requests:
* Splits the storage of value between keys/metadata and body (assuming some definition of metadata is provided);
* Allows for the application to define what constitutes object metadata and what constitutes the body (value-part) of the object - and assign tags to objects to manage multiple object-types with different extraction rules;
* Stores keys/metadata in a merge tree and the full object in a journal of CDB files
* Allowing for HEAD requests which have lower overheads than GET requests; and
* Queries which traverse keys/metadatas to be supported with fewer side effects on the page cache than folds over keys/objects.
* Support for tagging of object types and the implementation of alternative store behaviour based on type.
* Allows for changes to extract specific information as metadata to be returned from HEAD requests;
* Potentially usable for objects with special retention or merge properties.
* Support for low-cost clones without locking to provide for scanning queries (e.g. secondary indexes).
* Low cost specifically where there is a need to scan across keys and metadata (not values).
* Written in Erlang as a message passing system between Actors.

# Strengths

1. Leveled was developed specifically for OpenRiak, with specific features included by default:

* Support for secondary indexes
* Multiple fold types
* Auto expiry of objects Enabling compression means more CPU usage but less disk space. Compression is especially good for text data, including raw text, Base64, JSON, etc.

2. Optimised for larger value workloads (e.g. > 4KB).

3. Support for HEAD requests in additiong to GET requests.

4. Support for low-cost clones without locking to provide for scanning queries (e.g. secondary indexes).


# Weaknesses

1. Leveled is still a comparatively new technology and more likely to suffer from edge case issues than Bitcask or LevelDB simply because they’ve been around longer and have been more thoroughly tested via usage in customer environments.

2. Leveled works better with medium to larger sized objects. It works perfectly well with small objects but the additional diskspace overhead may render LevelDB a better choice if disk space is at a premium and all of your data will be exclusively limited a few KB or less. This may change as Leveled matures though.

# Installing and enabling

OpenRiak comes packaged with leveled, so there is no need for further steps to install it.

You can select leveled as your backend by changing the value of `storage_backend` in your `riak.conf` file to `leveled` as it appears below:

```
storage_backend = leveled
```

### Note: If you replace the existing specified backend by removing it or commenting it out as shown in the above example, data belonging to the previously specified backend will still be preserved on the filesystem but will no longer be accessible through Riak unless the backend is enabled again.

 You can verify that leveled is currently being used as the storage backend on an active cluster by checking the `riak.conf` file for the following line:

```
storage_backend = leveled
```

If the value of `storage_backend` does not match above, then OpenRiak is not using leveled as it's backend.

You can also use the following command to check this value for a single node or all nodes in a cluster:

```bash
$ sudo riak admin show storage_backend
```

The output for a single node should appear as follows:

```
+--------------+-----------------------+
|     node     |    storage_backend    |
+--------------+-----------------------+
|riak@127.0.0.1|riak_kv_leveled_backend|
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
|riak@127.0.0.1|riak_kv_leveled_backend|
+--------------+-----------------------+
|riak@127.0.0.2|riak_kv_leveled_backend|
+--------------+-----------------------+
|riak@127.0.0.3|riak_kv_leveled_backend|
+--------------+-----------------------+
|riak@127.0.0.4|riak_kv_leveled_backend|
+--------------+-----------------------+
|riak@127.0.0.5|riak_kv_leveled_backend|
+--------------+-----------------------+

ok
```

# Configuring leveled

Leveled's default behavior can be changed by adding and modifying the following parameters in the leveled section of `riak.conf`.

```

```
