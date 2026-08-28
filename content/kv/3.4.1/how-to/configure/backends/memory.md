---
title: 'Configure the Memory backend'
description: 'Show operators how to configure the memory backend without losing access to required data.'
weight: 6
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\backends\configure-memory.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
  - 'The memory backend is deprecated in OpenRiak KV 3.4 and should not be selected for durable data.'
source_material:
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#in-memory-deprecated'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure the memory backend without losing access to required data.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### In-memory (deprecated)

The in-memory backend has the following characteristics and features:

- Not persisted, all data on an individual node will be lost on restart.
  - Note that Riak clusters are resilient to the loss of data on a single node, but constraining the ability to perform [rolling restarts]({{< baseurl >}}kv/3.4.1/how-to/operate/rolling-restart/) of Riak due to data loss, may cause operational overheads.
- Based on the erlang ETS tables.
- Has crude and imperfect handling of out-of-memory issues to help limit the size of each individual vnode store.
- Supports secondary index entries, but will not support the full Riak Query API.

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
