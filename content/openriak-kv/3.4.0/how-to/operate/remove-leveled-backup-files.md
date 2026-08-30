---
title: 'Remove obsolete Leveled backup files'
description: 'Show operators how to identify and safely remove obsolete Leveled backup files.'
weight: 27
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
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#garbage-collecting-bak-files-in-leveled'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to identify and safely remove obsolete Leveled backup files.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Garbage collecting .bak files in leveled

The leveled backend will in some cases persist to disk work in progress during compaction, and then find that work in progress orphaned if it is interrupted by a restart before the change can be applied - there is space consumed on disk by files not referred to in the manifest for the store.  At the next restart, within the leveled ledger, such orphaned files will be renamed as `*.bak` files.

Clearing up the history of these orphaned files is a manual process.  It is always safe to delete `*.bak` files, but for extra caution one may choose to only delete those files unmodified since before the previous start of Riak.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
