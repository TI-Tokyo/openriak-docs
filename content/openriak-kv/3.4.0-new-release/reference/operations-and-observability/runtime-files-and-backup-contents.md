---
title: Runtime files and backup contents
weight: 1090
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Runtime artefacts belong to several different recovery scopes. Record the active paths from the generated
  settings and the running configuration before copying, moving, or restoring them.
related:
- reference/configuration/node-identity-directories-and-ring-settings
- reference/configuration/bitcask-settings
- reference/configuration/leveled-settings
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- how-to/cluster-lifecycle/restore-node-data-from-a-backup
- how-to/storage-maintenance/remove-obsolete-leveled-backup-files
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
---

Runtime artefacts belong to several different recovery scopes. Record the active paths from the generated settings and the running configuration before copying, moving, or restoring them.

## Configuration and identity

`riak.conf`, advanced configuration, the node name, distribution credentials, certificates, and service overrides describe how the node starts and participates. Protect secrets in backup copies and restore their ownership and permissions.

## Cluster metadata

Ring state and cluster metadata preserve membership and policy information. They are not interchangeable with backend object files. A restored ring from another cluster or an inappropriate point in its history can conflict with the intended recovery environment.

## Backend state

Bitcask data and hint files, Leveled journals and ledgers, and legacy backend files require their own consistent backup procedure. Leveled backup artefacts and active store files must be distinguished before cleanup.

## Rebuildable and temporary state

Logs, queued work, anti-entropy stores, and query-result files have different lifecycles. Do not assume that every non-object directory is safe to delete: rebuilding it can take substantial time or discard work that has not reached another system.
