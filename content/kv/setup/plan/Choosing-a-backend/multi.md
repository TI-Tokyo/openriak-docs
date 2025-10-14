---
sidebar_position: 5
title: Multi backend
sidebar_label: Multi
pagination_label: Planning
sidebar_class_name: kv-setup-plan
date: 2025-10-13
---

# Contents
1. [introduction](#introduction)
2. [Configuring multiple backends](#configuring-multiple-backends)

# Introduction 

OpenRiak allows you to run multiple backends within a single OpenRiak cluster. Selecting the Multi backend enables you to use different storage backends for different buckets. Any combination of the three available backends — Bitcask, LevelDB, and Memory can be used.


# Configuring multiple backends

You can enable Multi backend by changing the value of `storage_backend` in your `riak.conf` file to the following:

```bash
storage_backend = multi
```

