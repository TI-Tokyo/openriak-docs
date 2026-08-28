---
title: 'Configure the LevelDB backend'
description: 'Show operators how to configure the leveldb backend without losing access to required data.'
weight: 4
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\backends\configure-leveldb.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
  - 'LevelDB is deprecated in OpenRiak KV 3.4 and should not be selected for new deployments.'
source_material:
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#eleveldb-deprecated'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure the leveldb backend without losing access to required data.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Eleveldb (deprecated)

The eleveldb backend has the following characteristics and features:

- A heavily-adapted version of the google leveldb store - a LSM tree backend written in C++.  The adapted version is now deprecated, and the original version is subject to only limited maintenance activity.
  - has specific optimisations when compared with google leveldb to: reduce stalling; share and schedule resources where multiple instances operate on the same server; recover disk space following deletion; support automated object expiry.
- Supports secondary index entries, but will not support the full Riak Query API.
- Potentially faster and more efficient than leveled when values are small.
- Moves the majority of CPU and memory management away from the BEAM, to be managed directly within the C++ code.
  - This provides some additional capabilities, in particular the ability to fix the percentage of memory used across all eleveldb-backed vnodes on a node.
  - This has some long-term maintenance overheads, which the OpenRiak community are not expecting to continue to support after the release of Riak 4.0.

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
