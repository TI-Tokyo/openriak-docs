---
title: Handoff states and transfer records
description: Handoffs transfer vnode data during ownership changes, temporary fallback recovery, or explicit repair.
  Their status records describe work in progress, not an atomic cluster transaction.
weight: 1060
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\handoff.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/operations/handoff.md
related:
- how-to/cluster-lifecycle/monitor-and-control-handoffs
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- reference/configuration/repair-and-handoff-settings
- foundations/cluster-architecture/membership-gossip-and-handoff
---

Handoffs transfer vnode data during ownership changes, temporary fallback recovery, or explicit repair. Their status records describe work in progress, not an atomic cluster transaction.

## Inspection interfaces

{{< cli-example key="shell:riak admin handoff summary" >}}
{{< cli-example key="shell:riak admin handoff details" >}}
{{< cli-example key="shell:riak admin transfers" >}}

The command metadata defines available flags and output forms. Identify source, destination, partition, transfer type, and progress when comparing observations.

## State and completion

A committed membership plan can coexist with pending transfers. A node must retain its data and connectivity until its required transfers complete. Repair handoffs can restore only data held by surviving replicas. A paused or constrained transfer still represents unfinished recovery work.

## Controls

Concurrency, limits, and transport settings are in [Repair and handoff settings]({{< product-version-root >}}reference/configuration/repair-and-handoff-settings/). Runtime handoff controls are in [Handoff commands]({{< product-version-root >}}reference/commands/riak/admin/handoff/). Apply a change to the relevant transfer class and restore temporary limits after the operation.
