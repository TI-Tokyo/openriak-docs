---
title: Migrate to another cluster using replication
description: Migrate an application to a separately provisioned cluster while preserving writes made during the
  copy. Keep a rollback plan for writes accepted after cutover.
weight: 680
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- openriak-quickdocs-3.4
- openriak-discussions
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#interconnecting-multiple-clusters---changing-the-choice
- https://openriak.github.io/riak/InitialDesignDecisions.html#ring-size---changing-the-choice
- https://openriak.github.io/riak/ReplicationGuide.html#migrating-a-cluster
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/migrate-cluster.md
related:
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- how-to/storage-maintenance/migrate-to-another-storage-backend
- tutorials/cluster-operations-and-recovery/practise-a-backend-migration
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
---

Migrate an application to a separately provisioned cluster while preserving writes made during the copy. Keep a rollback plan for writes accepted after cutover.

## Prepare the destination

Configure its intended backend, ring, capacity, and security before loading data. Create matching bucket types and properties. Verify the application against a small representative dataset, including indexes, data types, and sibling handling.

## Start replication and seed

Enable a dedicated source queue and destination consumers using [Connect clusters with next-generation replication]({{< product-version-root >}}how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication/). Verify delivery of a new write, then seed each required bucket using [Re-replicate a key range or time window]({{< product-version-root >}}how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window/). Include all relevant replica policies when enumerating buckets and configuring reconciliation.

## Prove catch-up

Monitor queue discards and sink failures during the copy. Run reconciliation until completed checks show the intended data in sync. Compare known values and application queries; object counts alone are insufficient. Resolve excluded buckets and any separately provisioned metadata explicitly.

## Cut over and retain recovery options

Coordinate or pause writers, complete the final catch-up, then switch the application endpoint. Monitor errors and latency before removing the source. If the destination receives new writes, rollback requires returning those writes to the original cluster and verifying them before switching back.
