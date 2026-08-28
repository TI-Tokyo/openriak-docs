---
title: 'Exclude a bucket from cached AAE trees'
description: 'Show operators how to exclude temporary non-replicated bucket data from cached AAE trees.'
weight: 15
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#property---aae_tree_exclude'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to exclude temporary non-replicated bucket data from cached AAE trees.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Property - aae_tree_exclude

**Available from OpenRiak KV 3.4.0.**

The `aae_tree_exclude` bucket property has a default value of `false` and allows for flexibility when reconciling between clusters using nextgenrepl full-sync.  In general with Riak nextgenrepl it is assumed that clusters aim to contain the same data.  It is possible to replicate specific buckets between specific sources, and also possible to reconcile only individual buckets between clusters - but per-bucket reconciliation is not as efficient as full-cluster reconciliation.  The efficiency of full cluster reconciliation is based on the use of cached and mergeable [AAE (active anti-entropy) merkle trees](/kv/3.4.1/explanation/replication/active-anti-entropy/) that represent all the data in the store.

The purpose of `aae_tree_exclude` is to not include the bucket in the cached tree, so that the bucket isn't considered in any all-data reconciliation jobs.  For example, this may help when:

- a subset of buckets are not replicated between clusters;
- a bucket is using a backend TTL within one of the clusters (a cached tree cannot coordinate changes with backend stores which implement auto-expiry - so cached trees may prompt false AAE workloads when a backend TTL is used).

If a bucket is configured to `{aae_tree_exclude, true}`, the keys are still visible to aae_folds.  If using parallel-mode Tictac AAE, modification will still impact the parallel keystore.

The preferred long-term strategy for temporary objects is to use the eraser and reaper processes to garbage collect objects, rather than relying on backend TTL.  However when migrating from a multi-backend store with TTL-based backends, the migration should be easier if: those temporary buckets are excluded from aae trees, are replicated separately using range_repl, and reconciled using bucket-specific aae full-sync jobs.

The `aae_tree_exclude` bucket property may be cached by processes within a cluster, so changing the property will not have immediate effect.  A change to the `aae_tree_exclude` property should be coordinated with a [rolling restart](/kv/3.4.1/how-to/operate/rolling-restart/).

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
