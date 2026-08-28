---
title: 'Configure global object expiration'
description: 'Show operators how to configure global object expiration and verify the result.'
weight: 4
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\global-object-expiration.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data---changing-the-choice'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure global object expiration and verify the result.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Configure Global Object Expiration

[ttl]: https://en.wikipedia.org/wiki/Time_to_live

By default, LevelDB keeps all of your data. But OpenRiak KV allows you to configure global object expiration (`expiry`) or [time to live (TTL)][ttl] for your data.

Expiration is disabled by default, but enabling it lets you expire older objects to reclaim the space used or purge data with a limited time value.

#### Enabling Expiry

To enable global object expiry, add the `leveldb.expiration` setting to your riak.conf file:

```riak.conf
leveldb.expiration = on
```

**Note:**
Turning on global object expiration will not retroactively expire previous data. Only data created while expiration is on will be scheduled for expiration.

#### Setting Retention Time

The `retention_time` setting is used to specify the time until objects expire.
Durations are set using a combination of an integer and a shortcut for the supported units:

- Milliseconds - `ms`
- Seconds - `s`
- Minutes - `m`
- Hours - `h`
- Days - `d`
- Weeks - `w`
- Fortnight - `f`

The following example configures objects to expire after 5 hours:

```riak.conf
leveldb.expiration = on
leveldb.expiration.retention_time = 5h
```

You can also combine durations. For example, let's say you wanted objects to expire after 8 days and 9 hours:

```riak.conf
leveldb.expiration = on
leveldb.expiration.retention_time = 8d9h
```

#### Expiry Modes

Global expiration supports two modes:

- `whole_file` - the whole sorted string table (`.sst`) file is deleted when all of its objects are expired.
- `normal` - individual objects are removed as part of the usual compaction process.

We recommend using `whole_file` with time series data that has a similar lifespan, as it will be much more efficient.

The following example configure objects to expire after 1 day:

```riak.conf
leveldb.expiration = on
leveldb.expiration.retention_time = 1d
leveldb.expiration.mode = whole_file
```

#### Disable Expiry

To disable global object expiration, set `leveldb.expiration` to `off` in your riak.conf file. If expiration is disabled, the other 2 settings are ignored. For example:

```riak.conf
leveldb.expiration = off
leveldb.expiration.retention_time = 1d
leveldb.expiration.mode = whole_file
```

#### Deleting data - changing the choice

The delete mode is a per-node configuration which needs to be applied consistently across all nodes in a cluster, and across all connected clusters.

Changing the delete mode is possible, with a restart, but needs to be a coordinated change across the whole environment - a small time delta between changes is not an issue and can be handled by anti-entropy and reconciliation processes.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
