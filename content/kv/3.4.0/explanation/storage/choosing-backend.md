---
title: 'Choosing a storage backend'
description: 'Explain choosing a storage backend, its constraints, and the workloads for which it is appropriate.'
weight: 4
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\backends\index.md'
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\plan\Choosing-a-backend\index.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
  - 'Legacy version text or MDX syntax remains and requires editorial review.'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\planning\backend.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#database-backend'
  - 'https://openriak.github.io/riak/RiakTheoryGuide.html#backend-design'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain choosing a storage backend, its constraints, and the workloads for which it is appropriate.

## Overview

### Choosing a Backend

[plan backend bitcask]: /kv/3.4.0/explanation/storage/bitcask/
[plan backend leveldb]: /kv/3.4.0/explanation/storage/leveldb/
[plan backend memory]: /kv/3.4.0/explanation/storage/memory/
[plan backend multi]: /kv/3.4.0/explanation/storage/multi-backend/
[plan backend leveled]: /kv/3.4.0/explanation/storage/leveled/
[dev api backend]: /kv/3.4.0/reference/specialized-apis/backend-api/

Pluggable storage backends are a key feature of OpenRiak KV. They enable you to
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

OpenRiak KV supports the use of custom storage backends as well. See the
storage [Backend API][dev api backend] for more details.

Feature or Characteristic                      |Bitcask|LevelDB|Memory|
:----------------------------------------------|:-----:|:-----:|:----:|
Default OpenRiak KV backend                        |✓      |       |      |
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

#### Backend Design

For Riak 3.4, there are two backends recommended for use in production systems:

- the bitcask backend;
- the leveled backend.

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.
