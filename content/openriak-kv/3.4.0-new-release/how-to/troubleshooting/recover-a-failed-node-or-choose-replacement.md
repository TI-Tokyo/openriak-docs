---
title: Recover a failed node or choose replacement
description: Choose between restarting an intact member, repairing lost storage, and replacing failed hardware.
  Preserve evidence before clearing data or changing membership.
weight: 1330
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery\failed-node.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#completing-a-repair
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#reactive-replacement
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#replace-repair-and-recover
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/troubleshoot/recover-failed-node.md
related:
- how-to/cluster-lifecycle/replace-a-failed-node
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- how-to/cluster-lifecycle/recover-a-cluster-after-a-widespread-failure
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Choose between restarting an intact member, repairing lost storage, and replacing failed hardware. Preserve evidence before clearing data or changing membership.

## Determine what survived

Check storage integrity, node identity, ring metadata, and whether the original process can still run. If data and identity are intact, fix the underlying failure and return the same node without staging a leave or replacement. Wait for hinted handoff and AAE recovery.

## Recover an empty member

If local data is lost but other replicas remain, rebuild the host with the intended identity and compatible configuration. Ensure the old process cannot return. For a new identity use [Replace a failed node]({{< product-version-root >}}how-to/cluster-lifecycle/replace-a-failed-node/); for the same identity, stage a rejoin and review the plan before committing. The plan should not unexpectedly redistribute unrelated ownership.

Keep the empty member out of coverage, repair with [Repair a vnode or node from surviving replicas]({{< product-version-root >}}how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas/), and re-enable protection and routing only after verification. Restoring a stale single-node backup is usually less direct than repairing from current surviving replicas.

## Escalate the recovery scope

If too many replicas are lost, use [Recover a cluster after a widespread failure]({{< product-version-root >}}how-to/cluster-lifecycle/recover-a-cluster-after-a-widespread-failure/) to evaluate another cluster or backup. Do not repeatedly force membership changes in the hope that missing values will reappear. Record which data sources remain available and which time ranges cannot yet be verified.
