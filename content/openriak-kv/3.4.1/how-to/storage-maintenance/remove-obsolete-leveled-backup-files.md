---
title: Remove obsolete Leveled backup files
weight: 350
product: OpenRiak KV
product_version: 3.4.1
diataxis: how-to
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Remove Leveled files that have been explicitly renamed as obsolete `.bak` files after startup recovery.
  Do not remove active journal, ledger, manifest, or hot-backup files based only on their age.
related:
- how-to/storage-maintenance/repair-a-leveled-store
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- reference/operations-and-observability/runtime-files-and-backup-contents
- foundations/storage-and-performance/storage-backend-trade-offs
- foundations/storage-and-performance/persistence-filesystems-and-space-reclamation
---

Remove Leveled files that have been explicitly renamed as obsolete `.bak` files after startup recovery. Do not remove active journal, ledger, manifest, or hot-backup files based only on their age.

## Identify the exact store

Record the node, partition directory, and current backend. Confirm that startup recovery has completed and the files are inside the intended Leveled store. Retain incident evidence if the node recently crashed.

## Review candidates

List `.bak` files within that store and compare their modification times with the last successful startup. For a cautious cleanup, select only files older than that startup. Review the explicit list before deletion; do not run a broad filesystem-wide wildcard removal.

## Remove and verify

Delete only the reviewed obsolete files. Check available space, backend logs, and sample reads afterwards. If space does not return as expected, inspect open file handles and retained hot-backup links instead of deleting additional store files.


## Journal files in 3.4.1

Startup recovery also identifies unused Leveled journal files, in addition to unused ledger files. Review only files explicitly marked obsolete after a successful startup; active journals and manifests remain part of the store.
