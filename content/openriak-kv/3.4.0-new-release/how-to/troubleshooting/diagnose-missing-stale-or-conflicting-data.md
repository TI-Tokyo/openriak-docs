---
title: Diagnose missing, stale, or conflicting data
description: Investigate an object that appears missing, stale, or conflicted without overwriting the evidence.
weight: 1310
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- developers
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/troubleshoot/unexpected-or-stale-data.md
related:
- how-to/application-data/resolve-concurrent-object-updates
- how-to/data-inspection-and-repair/repair-a-selected-key-range
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Investigate an object that appears missing, stale, or conflicted without overwriting the evidence.

## Confirm identity

Check the exact type, bucket, key bytes, endpoint, and cluster. A typed and untyped request can address different namespaces.

## Preserve versions

Fetch the object with its context and siblings. Record deletions, expiry policy, recent restores, and the application’s last successful write.

## Compare replica and replication state

Check reachable primaries, recent membership changes, repair progress, source queues, and destination lag. Do not assume an empty queue proves dataset equality.

## Resolve the identified cause

Correct a namespace or client-context error first. Use a bounded repair or an application merge only after determining whether the difference is stale replication or genuine concurrency. Re-read and verify after the change.
