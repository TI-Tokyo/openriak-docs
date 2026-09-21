---
title: Recover a cluster after a widespread failure
description: Recover service after a widespread failure by first preserving evidence and determining which data
  copies remain trustworthy. Avoid making membership changes while the extent of the failure is still unknown.
weight: 830
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery\failure-recovery.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/troubleshoot/recover-cluster-failure.md
related:
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- how-to/troubleshooting/recover-a-failed-node-or-choose-replacement
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- how-to/cluster-lifecycle/restore-node-data-from-a-backup
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/backups-restores-and-disaster-recovery
---

Recover service after a widespread failure by first preserving evidence and determining which data copies remain trustworthy. Avoid making membership changes while the extent of the failure is still unknown.

## Stabilise and inventory

Stop automated destructive recovery actions and coordinate application writes where necessary. Record unavailable nodes, storage health, network failures, logs, and the last known healthy membership. Preserve affected disks and metadata before attempting repair.

## Choose the recovery source

If nodes retain intact data, restore connectivity and restart them with their original identities. If only selected members lost storage, use [Repair a vnode or node from surviving replicas]({{< product-version-root >}}how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas/) with verified surviving replicas. If local replicas are insufficient, evaluate another reconciled cluster or a verified backup. Current-generation replication uses the controls in [Next-generation replication runtime controls]({{< product-version-root >}}reference/replication-interfaces/next-generation-replication-runtime-controls/), not legacy `riak_repl` commands.

## Recover in a controlled environment

Bring back the smallest well-understood set of intact members first, inspect their view of the ring, and expand recovery deliberately. For backup recovery, follow [Restore node data from a backup]({{< product-version-root >}}how-to/cluster-lifecycle/restore-node-data-from-a-backup/) in isolation. Do not force-remove multiple members simply to make membership output look clean; that can discard the information needed for recovery.

## Prove readiness

Check known critical keys, causal histories, indexes, bucket policies, security, and replication scope. Wait for the required repairs and reconciliation, then restore traffic gradually while monitoring errors and latency. Record any unrecoverable time range or data scope explicitly.
