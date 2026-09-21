---
title: Diagnose node crashes
description: Investigate an unexpected process exit using the evidence from the failure interval.
weight: 1270
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
- how-to/troubleshoot/node-crashes.md
related:
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- how-to/troubleshooting/recover-a-failed-node-or-choose-replacement
- how-to/troubleshooting/investigate-a-running-node-with-erlang-diagnostics
- reference/operations-and-observability/log-files-and-event-formats
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Investigate an unexpected process exit using the evidence from the failure interval.

## Preserve evidence

Save the service exit status, crash dump if produced, system logs, and OpenRiak logs before rotation overwrites them.

## Separate causes

Check for operating-system OOM termination, an external stop, resource exhaustion, storage faults, and an Erlang exception. Correlate host timestamps with application errors.

## Control recovery

Restore capacity or correct the identified fault before returning the node. Avoid a restart loop that continually interrupts repair or overwrites evidence.

## Verify stability

Observe the node under representative traffic and check transfers and repair. If it exits again, compare the first failure signatures rather than treating every restart as a new unexplained event.
