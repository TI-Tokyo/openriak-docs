---
title: Monitor and control handoffs
description: Observe ownership, hinted, and repair handoffs, and adjust transfer pressure when it interferes with
  the workload. Record the original limits before changing them.
weight: 770
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\handoff.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---await-handoffs
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/manage-handoffs.md
related:
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- reference/commands/riak/admin/handoff
- reference/operations-and-observability/handoff-states-and-transfer-records
- foundations/cluster-architecture/membership-gossip-and-handoff
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
---

Observe ownership, hinted, and repair handoffs, and adjust transfer pressure when it interferes with the workload. Record the original limits before changing them.

## Inspect current work

{{< cli-example key="shell:riak admin handoff summary" >}}
{{< cli-example key="shell:riak admin handoff details" >}}
{{< cli-example key="shell:riak admin transfers" >}}

Identify the transfer type, source, target, and whether bytes or objects continue to progress. Check storage and network health on both ends before assuming a transfer is stalled.

## Adjust deliberately

{{< cli-example key="shell:riak admin handoff config" >}}

Use the command's options and [Repair and handoff settings]({{< product-version-root >}}reference/configuration/repair-and-handoff-settings/) to change the relevant concurrency or limit. Reduce pressure when client latency or queues grow; do not disable all transfers simply to suppress an alert. A temporary pause postpones recovery and leaves the cluster in its transitional state.

## Restore and verify

Return normal limits when the pressure subsides. Verify that all expected transfers finish, ownership reaches the committed plan, and no member was decommissioned prematurely. Persist lasting settings in configuration rather than relying solely on runtime changes.
