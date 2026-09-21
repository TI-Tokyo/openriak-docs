---
title: Inspect vnode and backend status
description: Inspect vnode and backend status when a partition or local store needs diagnosis. Record the node and
  partition identifiers with the observation.
weight: 860
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
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#vnode-status
tags:
- diataxis
- kv
- how-to
- quickdocs
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/check-vnode-status.md
related:
- reference/commands/vnode-status
- how-to/monitoring-and-diagnostics/inspect-node-and-cluster-health
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- how-to/storage-maintenance/repair-a-leveled-store
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Inspect vnode and backend status when a partition or local store needs diagnosis. Record the node and partition identifiers with the observation.

## Capture status

{{< cli-example key="shell:riak admin vnode-status" >}}

Use the generated command entry for the fields and invocation supported by the installed release. Compare the affected vnode with healthy vnodes using the same backend; status structures can differ by backend and version.

## Correlate the evidence

Check whether the partition is primary, fallback, or transferring ownership. Compare its backend errors, file or store state, queues, and recent log events with client failures at the same time. A busy vnode during handoff is a different diagnosis from a store that cannot open its files.

## Choose the next action

Preserve logs and status before restarting or repairing. Use the backend-specific repair procedure only after identifying the scope. After a corrective action, repeat the same status capture and verify representative object reads and indexed queries.
