---
title: Investigate read-repair activity
description: Investigate increased read-repair work by correlating it with recent failures, ownership changes, and
  application traffic.
weight: 880
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging-and-monitoring-of-read-repairs
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/monitor-read-repairs.md
related:
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- how-to/monitoring-and-diagnostics/inspect-stored-objects-and-metadata
- how-to/troubleshooting/diagnose-missing-stale-or-conflicting-data
- reference/operations-and-observability/node-and-cluster-metrics
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
---

Investigate increased read-repair work by correlating it with recent failures, ownership changes, and application traffic.

## Establish the pattern

Measure read-repair activity as a rate over time and compare nodes. Record concurrent client errors, request latency, handoffs, restarts, and AAE discrepancies. A repair after a temporary outage can be expected; a sustained increase without recovery needs explanation.

## Inspect representative keys

Choose a small sample associated with the problem and compare values, siblings, and causal context through the normal API. Check that clients preserve context and that bucket replica policies are consistent. Avoid exhaustive key listing as the first diagnostic step.

## Resolve the cause

Allow expected handoffs to complete, repair lost data through [Repair a vnode or node from surviving replicas]({{< product-version-root >}}how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas/), or correct application conflict handling through [Resolve concurrent object updates]({{< product-version-root >}}how-to/application-data/resolve-concurrent-object-updates/). If cold data remains divergent, verify TicTac AAE rather than relying on future reads to discover it.

## Verify

Compare repair rates and client latency after the fix. A lower counter alone is not enough: confirm the affected keys are present and the required background protection is still running.
