---
title: Persistence, filesystems, and space reclamation
description: Persistence concerns which acknowledged data survives a failure. Space reclamation concerns when storage
  occupied by obsolete state can be reused. Both depend on the backend and filesystem, but they answer different
  ques
weight: 310
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- performance-engineers
- architects
- operators
source_material:
- live-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#notes-on-implementation
- https://openriak.github.io/riak/ObjectAPI.html#performance-and-efficiency
- https://openriak.github.io/riak/ObjectAPI.html#performance-expectations
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/performance/storage-and-filesystem-effects.md
- foundations/operations/garbage-collection.md
related:
- foundations/data-and-consistency/deletion-tombstones-and-expiration
- foundations/storage-and-performance/how-bitcask-stores-data
- foundations/storage-and-performance/how-leveled-stores-data
- how-to/storage-maintenance/schedule-bitcask-merges
- how-to/storage-maintenance/schedule-leveled-compaction
- reference/operations-and-observability/runtime-files-and-backup-contents
---

Persistence concerns which acknowledged data survives a failure. Space reclamation concerns when storage occupied by obsolete state can be reused. Both depend on the backend and filesystem, but they answer different questions.

## From memory to durable storage

A write can pass through process memory, operating-system caches, and storage-controller caches before reaching stable media. Backend synchronisation settings and request acknowledgement options determine which steps a success response relies on. Replication adds copies, but shared power or storage failures can still affect several copies together.

## Logical and physical deletion

An update or tombstone can make older records obsolete without immediately removing their bytes. Bitcask merges and Leveled compaction reclaim eligible space later. Snapshots, retained versions, and active work can keep files necessary after a newer logical state exists.

## Filesystem effects

Capacity planning must include temporary files and background rewriting, not just the sum of current values. Latency spikes can reflect I/O contention or storage limits even while the application request rate is unchanged.

Erlang garbage collection reclaims process memory. It is not the mechanism that compacts database files or reaps replicated tombstones.
