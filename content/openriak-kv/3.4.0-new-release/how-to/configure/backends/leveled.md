---
title: 'Configure the Leveled backend'
description: 'Show operators how to configure the leveled backend without losing access to required data.'
weight: 5
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\backends\configure-leveled.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
  - 'Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.0 and require technical verification.'
  - 'Legacy version text or MDX syntax remains and requires editorial review.'
source_material:
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#leveled'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---leveled-backend'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure the leveled backend without losing access to required data.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Leveled

The leveled backend has the following characteristics and features:

- Pure erlang log-structured-merge (LSM) tree backend, designed and developed specifically for use within Riak.
  - Implementation in Erlang simplifies resource management as CPU scheduling of all Riak activity is under the control of the Erlang virtual machine.
- Differs from most other LSM implementations in that values are set-aside in a sequence-ordered journal, and only keys and metadata are placed in the key-ordered LSM-based ledger.  This provides for lower cost and more efficient reads when only keys and metadata are required (internally within Riak this is usually the case, even when the external user requires the value).  It also reduces the overhead of write amplification, supporting larger object sizes with greater efficiency.
- Internal optimisations to increase efficiency within Riak for the Tictac-based method of anti-entropy and inter-cluster reconciliation.
- Supports index entries as well as objects in the key-ordered ledger, to allow full use of the Riak Query API.
- Is the priority backend used within the OpenRiak community for both functional and non-functional testing of new releases.
- Generally requires significantly less memory than the total size of all the keys.
  - A fixed overhead (per vnode) of about 10K keys and metadata is kept in memory, plus 1% of the keys, plus 2-bytes per key.
- Guarding against out-of-memory errors is an operator responsibility.  The cluster should be expanded if the memory limit is close, the per-vnode memory overhead will not be proactively reduced.
  - Makes use of any spare memory of the system through proactive hints to the file-system page cache.

For further details on the design and implementation of the leveled backend refer to [the Riak Theory Guide]({{< product-version-root >}}foundations/storage/leveled/).

#### Configuration of Riak - leveled backend

Compression, decompression and compaction have a potentially significant impact on performance within leveled,  and so configuration items of notable importance are:

- Available from Riak 3.2.3`leveled.compression_method`; should be set to `zstd`, unless objects are sent to Riak compressed, in which case the compression method should be configured as `none`.
  - in testing `zstd` has been demonstrated to be the most efficient available option (when compared to `native` which uses zlib compression, or `lz4`).
- `leveled.ledger_compression`; if `compression_method` is set to `none`, then compression should still be enabled here e.g. set to `zstd`.
  - the ledger does not store object values, but stores the object keys and metadata in blocks by key order.
  - it is recommended to use some form of compression on the ledger, even when all values are pre-compressed.  The ledger blocks are generally highly compressible, even when the values are not.
- `leveled.compaction_runs_perday`; refer to the [operations guide]({{< product-version-root >}}how-to/configure/backends/leveled-compaction-window/) for more on leveled compaction.

There are further configurable options within the leveled backend, that can be changed within `riak.conf`.  For a comprehensive view, [refer to the leveled schema file](https://github.com/OpenRiak/leveled/blob/openriak-3.4/priv/leveled.schema).

The leveled logs are relatively verbose, when compared to log activity across Riak as a whole.  These logs can be tuned using:

- `leveled.log_level`; the info-level logs are useful for monitoring as well as troubleshooting, so careful consideration is required before moving to an alternate log level.

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
