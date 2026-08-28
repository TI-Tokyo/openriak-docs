---
sidebar_position: 2
title: Choosing a backend
sidebar_label: backend
pagination_label: Planning
sidebar_class_name: kv-setup-plan
date: 2026-01-22
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[overview]: #overview
[feature comparison]: #riak-backend-feature-comparison

# Overview 

Pluggable storage backends are a key feature of OpenRiak KV. They enable you to choose a low-level storage engine that suits specific operational needs. For example, if your use case requires maximum throughput, data persistence, and a bounded keyspace, then Leveled, which is a backend designed specifically for OpenRiak, is a good choice. On the other hand, if you need to store a large number of keys or to use secondary indexes, LevelDB is likely a better choice.

The following backends are supported:

    * [Bitcask]: : ../../setup/install/plan/choosing-a-backend/bitcask
    * [Leveled]: : ../../setup/install/plan/choosing-a-backend/leveled
    * [Memory]: : ../../setup/install/plan/choosing-a-backend/memory
    * [Multi]: : ../../setup/install/plan/choosing-a-backend/multi


# Riak Backend Feature Comparison

| Feature / Characteristic                   | Bitcask  | LevelDB | Memory | Leveled |
|--------------------------------------------|----------|---------|--------|---------|
| Default Riak KV backend                    | Y        |         |        |         |
| Persistent                                 | Y        | Y       |        | Y       |
| Keyspace in RAM                            | Y        |         | Y      | Y       |
| Keyspace can be greater than available RAM |          | Y       |        |         |
| Keyspace loaded into RAM on startup¹       | Y        |         |        | Y       |
| Objects in RAM                             |          |         | Y      |         |
| Object expiration                          | Y        |         | Y      | Y       |
| Secondary indexes                          |          | Y       | Y      | Y       |
|--------------------------------------------|----------|---------|--------|---------|


