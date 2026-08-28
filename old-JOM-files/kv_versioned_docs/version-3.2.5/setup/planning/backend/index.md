---
title: "Choosing a Backend"
sidebar_position: 102
sidebar_label: Choosing a Backend
pagination_label: "Choosing a Backend"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2025-03-24
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


[plan backend bitcask]: ./bitcask
[plan backend leveldb]: ./leveldb
[plan backend memory]: ./memory
[plan backend multi]: ./multi
[plan backend leveled]: ./leveled
[dev api backend]: ./../../../developing/api/backend

Pluggable storage backends are a key feature of Riak KV. They enable you to
choose a low-level storage engine that suits specific operational needs.
For example, if your use case requires maximum throughput, data
persistence, and a bounded keyspace, then Bitcask is a good choice. On
the other hand, if you need to store a large number of keys or to use
secondary indexes, LevelDB is likely a better choice.

The following backends are supported:

* [Bitcask][plan backend bitcask]
* [LevelDB][plan backend leveldb]
* [Memory][plan backend memory]
* [Multi][plan backend multi]
* [Leveled][plan backend leveled]

Riak KV supports the use of custom storage backends as well. See the
storage [Backend API][dev api backend] for more details.

Feature or Characteristic                      |Bitcask|LevelDB|Memory|
:----------------------------------------------|:-----:|:-----:|:----:|
Default Riak KV backend                        |✓      |       |      |
Persistent                                     |✓      |✓      |      |
Keyspace in RAM                                |✓      |       |✓     |
Keyspace can be greater than available RAM     |       |✓      |      |
Keyspace loaded into RAM on startup<sup>1</sup>|✓      |       |      |
Objects in RAM                                 |       |       |✓     |
Object expiration                              |✓      |       |✓     |
Secondary indexes                              |       |✓      |✓     |
Tiered storage

<sup>1</sup> Noted here since this can affect Riak start times for large
keyspaces.

