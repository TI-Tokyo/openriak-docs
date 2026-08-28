---
title: 'Verify configuration before startup'
description: 'Show operators how to verify configuration before startup and verify the result.'
weight: 10
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---key-riakconf-changes'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to verify configuration before startup and verify the result.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Configuration of Riak - key riak.conf changes

Almost all configuration of Riak can be done through the `etc/riak.conf` file.  Each public configuration option should be described in that file, but there are additional `hidden` options supported for expert-advised changes.  The `riak.conf` file is built from individual schema files, and the repositories which contribute towards those schema files are listed in [the `cuttlefish` section of the `riak/rebar.config` file](https://github.com/OpenRiak/riak/blob/fd27c6933391ece65b31760cccb87b671a80f310/rebar.config#L23-L37).

Each individual schema component can be found in the `priv` folder for that repository, e.g [priv/riak_kv.schema for the riak_kv schema](https://github.com/OpenRiak/riak_kv/blob/openriak-3.4/priv/riak_kv.schema).

When starting a first cluster to experiment, the following configuration items are of particular importance:

- `ring_size`; refer to the [ring size selection in the design decisions document](/kv/3.4.0/how-to/plan/choose-ring-size/), should be set smaller than the default for test/dev environments and larger than the default for production systems.
- `tictacaae_active`; refer to the [intra-cluster resilience in the design decisions document](/kv/3.4.0/how-to/plan/choose-intra-cluster-resilience/).  Should be set to active if the active repair of deltas between vnodes is required, otherwise repair will be reactive (i.e. only once a delta has been detected on read).
- `tictacaae_storeheads`; should be enabled when using `tictacaae_active` on a leveled backend if the full scope of AAE Folds are to be used.
- `anti_entropy`; this is a deprecated anti-entropy system, and should be set to `passive` if using `tictacaae_active`.  It may be set to `active` in parallel to `tictacaae_active` to transition between the services.  The legacy anti-entropy system is quicker and more aggressive at repairing deltas, but offers less functionality and runs at a higher cost when in sync.
- `storage_backend`; refer to the [backend selection in the design decisions document](/kv/3.4.0/how-to/plan/choose-storage-backend/), but for full Riak functionality must be set to leveled.
- `read_repair_primaryonly`; will impact the behaviour in failure, by default when a standby vnode replaces a failed vnode, read repair will be triggered on every GET to populate the standby with old writes, but this will have a negative impact performance during both failure and recovery.
- `buckets.default.merge_strategy`; should always be set to `2`, and `2` will be the only supported option from Riak 4.0.
- `nodename`; a unique name for the node within the cluster.
- `platform_data_dir`; where the actual data will be stored, must be a space with sufficient capacity and throughput.
- `listener.http.internal` or `listener.pb.internal`; the IP address and port for accessing the API. It is recommended to bind this IP address to a specific interface address.  [The Query API](/kv/3.4.0/tutorials/query-api/) requires use of the `http` listener, and performance will differ between the `pb` and `http` transports when using [the Object API](/kv/3.4.0/reference/http-api/).

In a `riak.conf` file, the last setting of any configuration item is the actual value used in the configuration.  Edits to the riak.conf file don't have to change the configuration in place, defaults may be overwritten by concatenating changes to the end of the file.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
