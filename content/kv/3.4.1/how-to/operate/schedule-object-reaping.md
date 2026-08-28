---
title: 'Schedule object reaping and erasure'
description: 'Show operators how to schedule reaping and erasure while controlling load and retention risk.'
weight: 26
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
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data---changing-the-choice'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#garbage-collection---reap-erase-and-scheduled-compaction'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#riak-kv-eraser-and-riak-kv-reaper'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to schedule reaping and erasure while controlling load and retention risk.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Deleting data - changing the choice

The delete mode is a per-node configuration which needs to be applied consistently across all nodes in a cluster, and across all connected clusters.

Changing the delete mode is possible, with a restart, but needs to be a coordinated change across the whole environment - a small time delta between changes is not an issue and can be handled by anti-entropy and reconciliation processes.

#### OpenRiak KV Eraser and OpenRiak KV Reaper

Available from Riak 3.0.10

The `riak_kv_eraser` is a process that receives requests to delete keys, queues those requests, and continuously erases keys from that queue.  Refer to the [API guide for AAE Fold]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/) for information on triggering a `erase_keys` AAE fold to feed the eraser queue.

Likewise the `riak_kv_reaper` process receives requests to delete tombstones, queues those requests, and continuously reaps keys referenced in the queue.  Refer to the [API guide for AAE Fold]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/) for information on triggering a `reap_tombs` AAE fold to feed the reaper queue.

Filters within the AAE folds can be used to select specific key_ranges, or last modified date ranges for the erase or reap process.

When queueing large volumes of changes, note that:

- The number of vnodes per node on which the fold is run will be restricted by the size of the `AF4_QUEUE` if the `dscp` worker strategy is used.  This will lead to a situation where items on the queue will be grouped by vnode, and dequeued in batches containing objects within the same preflist.
- The pace of which items are dequeued and processed is limited by the `tombstone_pause` configuration.  The pause should be increased if the rate of reaps or erases cause pressure within the cluster, or any clusters receiving replicas of the reap/erase events.  The pause can be adjusted at run-time by changing the underlying environment variable.
- In multi-data centre configurations, reap events must be specifically configured to be replicated - this is controlled through the `repl_reap` configuration setting.  Otherwise reap jobs must be run separately on each cluster (with reconciliation suspended until the reaps complete).
- Each queue on each node has a limit to the size of reaps or erases it can hold - this is controlled through the `eraser_overflow_limit` and the `reaper_overflow_limit`.  The queue, except for a small number, is held on disk; and so increasing this limit can be achieved without hitting memory constraints.
- As of Riak 3.4, if a reap is dequeued, but the primaries are not all available, then the reap will be acted on all available primaries and an item will be queued to act on the remaining primaries once they are available.
- Large reap jobs should not be queued while cluster change operations are planned on the cluster, or any cluster linked by replication.

Whether reaps are required depends on the `delete_mode` setting of the cluster.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
