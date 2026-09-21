---
title: Diagnose stalled or incomplete replication
description: Locate the stalled stage of a replication path and verify convergence after restoring it.
weight: 1320
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
- how-to/troubleshoot/replication-failures.md
related:
- reference/replication-interfaces/next-generation-replication-runtime-controls
- reference/replication-interfaces/legacy-riak-repl-runtime-controls
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Locate the stalled stage of a replication path and verify convergence after restoring it.

## Identify the generation

Confirm whether the path is next-generation replication or legacy v2/v3, its direction, queue or site, and dataset scope.

## Check connectivity and authentication

Test the configured source endpoint from the sink environment. Inspect certificate, credential, and connection failures.

## Check delivery

Compare source queue growth, sink worker activity, failures, and source/sink storage pressure. Verify that queue names and filters match.

## Recover and compare

Restore the failed stage, observe backlog draining, and perform a reconciliation check for work lost outside the current queue. Verify a known write and deletion at the destination.
