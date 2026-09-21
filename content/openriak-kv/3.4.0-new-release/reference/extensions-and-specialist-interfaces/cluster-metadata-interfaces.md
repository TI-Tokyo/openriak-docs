---
title: Cluster metadata interfaces
description: Cluster metadata stores configuration state shared within a cluster, including definitions required
  to interpret object data. It is distinct from backend object files and from the ring's ownership records.
weight: 1240
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\app-guide\cluster-metadata.md
source_material:
- legacy-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup---ring-folder-and-cluster-metadata
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/specialized-apis/cluster-metadata.md
related:
- how-to/application-data/create-and-activate-bucket-types
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- how-to/cluster-lifecycle/restore-node-data-from-a-backup
- reference/operations-and-observability/runtime-files-and-backup-contents
- foundations/storage-and-performance/storage-backend-trade-offs
---

Cluster metadata stores configuration state shared within a cluster, including definitions required to interpret object data. It is distinct from backend object files and from the ring's ownership records.

## Scope

Bucket-type definitions, security state, and other distributed metadata must be included in deployment and recovery planning. Inter-cluster object replication does not automatically clone this state into another cluster.

## Access contract

Use the supported administrative or API operation for the resource instead of editing metadata files or invoking internal storage functions directly. Internal metadata representations and conflict handling are release-sensitive.

## Backup and restore

Capture ring and cluster metadata with the node configuration and compatible backend recovery set. Preserve node identity, release, and ownership information. Restoring only object files into an unrelated metadata state can produce an incomplete or incorrectly configured recovery.
