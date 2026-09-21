---
title: Control repair impact during application traffic
description: Control repair resource use while application traffic continues. Define both an application latency
  target and a recovery-progress target before adjusting concurrency.
weight: 1070
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/repair-under-load.md
related:
- how-to/monitoring-and-diagnostics/inspect-worker-queues-and-saturation
- reference/configuration/repair-and-handoff-settings
- reference/configuration/tictac-anti-entropy-settings
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
---

Control repair resource use while application traffic continues. Define both an application latency target and a recovery-progress target before adjusting concurrency.

## Establish a baseline

Measure client latency and errors, backend I/O, worker queues, handoff activity, and repair progress over the same interval. Identify whether the constraint is CPU, disk, network, or a worker limit.

## Adjust one control

Use the release's repair, handoff, and worker settings. Reduce concurrency or pacing when foreground requests are harmed; increase it only when the constrained resource has capacity. Keep a record of the original value and whether a runtime change persists after restart.

{{< configuration-reference-table >}}
^repair_
^.*worker_pool.*
^tictacaae_(exchangetick|maxresults|rangeboost)$
{{< /configuration-reference-table >}}

## Verify the trade-off

Repeat the baseline measurements. Confirm that repair still advances and that the estimated recovery window remains acceptable. Revert an adjustment that moves the queue elsewhere or slows recovery without improving the application target.

Do not advance a rolling operation while a required repair gate is still failing.
