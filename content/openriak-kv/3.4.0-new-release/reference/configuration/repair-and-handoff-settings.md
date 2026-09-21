---
title: Repair and handoff settings
description: Repair, handoff, and worker settings govern transfer concurrency and background work. Reducing their
  impact on client traffic also changes the time required to restore redundancy.
weight: 180
diataxis: reference
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
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/configuration/repair.md
related:
- how-to/cluster-lifecycle/monitor-and-control-handoffs
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Repair, handoff, and worker settings govern transfer concurrency and background work. Reducing their impact on client traffic also changes the time required to restore redundancy.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(repair_|handoff|cluster_transfer_limit|transfer_limit|background_manager|.*worker_pool.*|backend_pause_ms|read_repair_)
{{< /configuration-reference-table >}}
