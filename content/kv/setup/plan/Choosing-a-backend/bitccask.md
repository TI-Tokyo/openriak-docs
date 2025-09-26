---
sidebar_position: 1
title: Bitcask backend
sidebar_label: Bitcask
pagination_label: Planning
sidebar_class_name: kv-setup-plan
date: 2025-09-25
---

## Contents

1. Introduction
2. Strengths
3. Weaknesses
4. Installing and enabling


## Introduction

Bitcask is an erlang-based application that provides fast access via an API for storage & retrival of key/value data using log-structured hash tables.

## Strengths


## Weaknesses

* Keys must fit in memory

The major weaknesses for Bitcask is that it keeps all the keys in memory at all times, which means the system must have enough memory for the entire keyspace plus the required amount for the operating system and other system components.

## Installing and enabling

Riak comes packaged with and is the default backend for OpenRiak. You can verify that Bitcask is currently being used as the storage backend by checking the `riak.conf` file for the following line:

```
storage_backend = bitcask
```

If the value of `storage_backend` does not match above, then OpenRiak is not using Bitcask as it's backend.