---
title: 'Repair a Leveled store'
description: 'Show operators how to diagnose and repair an individual Leveled store with appropriate safeguards.'
weight: 19
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
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#repair-an-individual-leveled-store'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to diagnose and repair an individual Leveled store with appropriate safeguards.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Repair an individual leveled store

The leveled backend is split into two parts - a journal, and a ledger.  The journal is the log of all received changes, and is the source of truth in leveled.  The ledger is a log-structured merge tree that provides a sorted view of the index keys, and object keys and metadata.  As the journal is the source of truth, the ledger can be rebuilt from the journal, and leveled will do this automatically on startup if the ledger is missing.

There exists the (very rare) potential for a ledger to be corrupted.  There are also circumstances where following an update the ledger is not fully efficient until it is rebuilt.  As a missing ledger is rebuilt automatically on startup, rebuilding of the ledger can simply be prompted by deleting it:

- Stopping the node;
- Deleting the ledgers in the impacted partitions (under each vnode's leveled store there should be a ledger folder);
- Restarting the node.

On restarting the node all missing ledgers will be rebuilt before the node becomes an active participant in the cluster - the `riak_kv` application which determines availability of a node, will not complete startup until all the rebuilds are complete.  Rebuild progress can be tracked in the leveled logs with `log_ref=b0006`.

Previous versions of Riak had an option to repair secondary index entries through a specific anti-entropy recovery process.  This is no longer supported.  If there are detected issues with inconsistency between objects and their index entries, then this should be addressed by the simple approach of deleting the ledger (which contains the index entries) to force a rebuild on restart of the vnode.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
