---
title: 'Configure the Bitcask merge window'
description: 'Show operators how to schedule Bitcask merges and verify that obsolete data is reclaimed.'
weight: 9
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#bitcask-merge-window'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to schedule Bitcask merges and verify that obsolete data is reclaimed.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### bitcask merge window

The bitcask backend operates at PUT time as an append-only database.  As bitcask does not provide a sorted view of objects, there is no immediate mutation on the file-system prompted by new object writes, other than the append.  If objects are immutable, there is no activity required to re-organise a bitcask store, it is a purely append-only operation.

If objects change; they are updated, deleted or they expire due to TTL - then bitcask must perform infrequent `merge` operations to update files so that replaced objects no longer consume space on disk.  Bitcask does not orchestrate merge operations so that they do not coincide, and the merge operations may have a significant impact on cluster performance when they are initiated.

If storing mutable objects in bitcask, then it is important to configure merge windows, windows in which merges are permitted to take place such that either:

- merges take place at different times on different nodes (or locations) so that only a single replica for each partition is impacted by a concurrent merge;
- merges take place outside of peak hours of database usage.

When testing the potential throughput of a bitcask-backed Riak database it is important to test with appropriate levels of mutation, and a realistic configuration of the bitcask merge window.

For information on configuring bitcask merge see the `bitcask.merge` sections [within the bitcask schema file](https://github.com/OpenRiak/bitcask/blob/openriak-3.2/priv/bitcask.schema).

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
