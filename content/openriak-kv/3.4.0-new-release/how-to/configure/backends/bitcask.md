---
title: 'Configure the Bitcask backend'
description: 'Show operators how to configure the bitcask backend without losing access to required data.'
weight: 2
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\backends\configure-bitcask.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
source_material:
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#bitcask'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---bitcask-backend'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure the bitcask backend without losing access to required data.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Bitcask

The bitcask backend has the following characteristics and features:

- A simple low-code, journal based key-value store, originally designed and developed by the founding Riak team at Basho; that has been used as a general implementation model for other such stores.
  - Although there have been minimal changes to the original version as of Riak 3.4, bitcask remains under active development within the OpenRiak community, with plans for future enhancements.
- Written primarily in Erlang, but including around 3K lines of C code to provide the in-memory database of keys.  Access to C-code is generally for short-lived functions, which limits the impact on the scheduling requirements of the BEAM.  The C-code is also extremely stable, and is low-risk in terms of overheads associated with platform evolution.
- Support for pure objects only, no support for index entries and any part of the Riak Query API.
- Requires an out-of-hours merge window to be available and configured, for compaction of mutated objects.  Merging under database load may lead to highly unpredictable performance.
- Requires a separate key-store backend if anti-entropy or inter-cluster reconciliation features are required.
- All keys are kept in-memory, and so sufficient memory is required as the number of keys expands.
  - Guarding against out-of-memory errors is an operator responsibility.  The cluster should be expanded as the memory limit is reached, the per-vnode memory overhead will not be proactively reduced.
- No current support for optimised HEAD requests, which can have significant impact on overall efficiency within Riak.
  - Implementations of bitcask have been produced with this optimisation, and may be open-sourced in the future.

For further details on the design and implementation of the bitcask backend refer to [the Riak Theory Guide]({{< product-version-root >}}foundations/storage/bitcask/).

#### Configuration of Riak - bitcask backend

For the bitcask backend, the configuration items of notable importance are:

- `bitcask.merge_policy`; refer to the [operations guide]({{< product-version-root >}}how-to/configure/backends/bitcask-merge-window/) for more on bitcask compaction.
- `bitcask.io_mode`; should be set to `erlang`, careful consideration is required before moving to `nif`.

There are further configurable options within the bitcask backend, that can be changed within `riak.conf`.  For a comprehensive view, [refer to the bitcask schema file](https://github.com/OpenRiak/bitcask/blob/openriak-3.4/priv/bitcask.schema).

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
