---
title: Vnode and backend status commands
description: Vnode status identifies local partition and backend state. Use the command's availability notice to
  distinguish releases that expose this interface.
weight: 300
diataxis: reference
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
- reference
- quickdocs
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/commands/vnode-status.md
related:
- how-to/monitoring-and-diagnostics/inspect-vnode-and-backend-status
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- reference/operations-and-observability/handoff-states-and-transfer-records
- reference/operations-and-observability/node-and-cluster-metrics
---

Vnode status identifies local partition and backend state. Use the command's availability notice to distinguish releases that expose this interface.

{{< cli-command key="shell:riak admin vnode-status" >}}

A vnode's process status is not evidence that all of its replicas or indexes are complete. Compare with handoff, AAE, and application observations.
