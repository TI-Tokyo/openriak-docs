---
title: 'Re-replicate keys from a time window'
description: 'Show operators how to re-replicate keys modified during a selected time window.'
weight: 30
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#re-replicating-keys-for-a-given-time-period'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to re-replicate keys modified during a selected time window.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Re-replicating keys for a given time period

The aae_fold `repl_keys_range` will replicate any key within the defined range to the clusters consuming from a defined queue.  See the [AAE fold API documentation]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/) for more information on using `repl_key_range`.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
