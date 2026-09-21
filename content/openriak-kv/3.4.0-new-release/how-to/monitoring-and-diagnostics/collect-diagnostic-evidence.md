---
title: Collect diagnostic evidence
description: Collect a reproducible incident record before changing a failing node. Include timestamps and enough
  scope information to compare evidence from several nodes.
weight: 910
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
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
- how-to/operate/collect-debug-information.md
related:
- reference/commands/diagnostic-commands
- reference/operations-and-observability/node-and-cluster-metrics
- reference/operations-and-observability/log-files-and-event-formats
- how-to/monitoring-and-diagnostics/inspect-vnode-and-backend-status
- how-to/troubleshooting/investigate-a-running-node-with-erlang-diagnostics
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Collect a reproducible incident record before changing a failing node. Include timestamps and enough scope information to compare evidence from several nodes.

## Capture the current state

Record the release, runtime, operating system, node identity, backend, recent deployment changes, affected keys or buckets, and a minimal failing request. Capture its status code and response body separately from client-library exceptions.

Use the diagnostic commands for node status, membership, ring state, transfers, and vnode status. Generate a cluster-info report when its scope and runtime cost are appropriate:

{{< cli-example key="shell:riak admin cluster-info" >}}

## Preserve logs and metrics

Collect the interval before and after the symptom, including restarts, queue growth, storage errors, and replication events. Keep the original timestamps and identify the clock and timezone used by each source.

## Prepare a shareable record

Remove passwords, distribution cookies, private keys, and confidential object bodies from the copy you share. Retain an access-controlled original when needed for investigation. State which commands or recovery actions have already run, so later observations are not mistaken for the original state.
