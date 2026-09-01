---
title: 'Configure per-bucket reconciliation'
description: 'Show operators how to scope reconciliation to selected buckets and verify convergence.'
weight: 13
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
  - 'https://openriak.github.io/riak/ReplicationGuide.html#configuration-of-per-bucket-reconciliation'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to scope reconciliation to selected buckets and verify convergence.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Configuration of Per-Bucket Reconciliation

The `ttaaefs_scope` can be set to a specific bucket, rather than `all`.

The non-functional characteristics of the solution change when using per-bucket full-sync.  There is no per-bucket caching of AAE trees, so the AAE trees will need to be re-calculated by scanning the whole bucket for every full-sync check (subject to other restrictions on check type).  So the cost of checking full-sync for an individual bucket in non-failure scenarios is considerably higher than using a scope of `all`.

When deltas are discovered in trees, the scanning required to compare keys and clocks will be limited to the bucket, and so this may be faster.

The rules of the `ttaaefs_<sync_type>check` configuration are followed with per-bucket synchronisation.  So using `ttaaefs_autocheck` when a previous check succeeded will scan only recently modified items to build the tree for comparison.  This does mean that non-recently modified variations within the bucket (such as resurrected objects or tombstones) will not be detected by `ttaaefs_autocheck` as when `ttaaefs_scope = all`.  When using per-bucket full-sync, it may be wise to occasionally schedule a `ttaaefs_allcheck` to cover this scenario.

> A scheduled run of `ttaaefs_allcheck` will occur regardless of whether the current time is within or outside of the `allcheck.window`.  The window is related only to the running of `ttaaefs_autocheck`, to prevent a `ttaaefs_autocheck` from being escalated to a `ttaaefs_allcheck` within the window.

When using per-bucket full-sync, and performing a rolling upgrade to Riak 3.2.3 or {{< current-version >}} (from earlier releases than Riak 3.2.3), there may be errors merging trees.  To prevent these errors during the rolling upgrade, then either disable full-sync for the period of the upgrade, or use the configuration option to force the new nodes to use legacy format trees:

- `legacyformat_tictacaae_tree = enabled`

There are significant memory improvements related to the Riak 3.2.3 tree format, so the configuration should be reversed after the rolling upgrade has completed.  There are no inter-cluster issues with tree versions, it is only an issue when merging trees within a cluster to provide a cluster-wide view of a tree.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
