---
title: Replace nodes without stopping the cluster
description: Replace healthy members one at a time while they can transfer their data to prepared replacements.
  Use this for hardware changes or planned host retirement.
weight: 750
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery\rolling-replaces.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#proactive-replacement
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#rolling-replacement
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/rolling-replacement.md
related:
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
- how-to/cluster-lifecycle/monitor-and-control-handoffs
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- how-to/storage-maintenance/migrate-to-another-storage-backend
- foundations/cluster-architecture/membership-gossip-and-handoff
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
---

Replace healthy members one at a time while they can transfer their data to prepared replacements. Use this for hardware changes or planned host retirement.

## Prepare a spare

Install and configure an empty node with compatible placement and sufficient resources. Keep it out of coverage until its data is complete. Do not reuse the old node's identity while that node is still running.

## Stage one replacement

On the new node:

{{< cli-example key="shell:riak admin cluster join" args="riak@EXISTING_NODE" >}}

On a participating member:

{{< cli-example key="shell:riak admin cluster replace" args="riak@OLD_NODE riak@NEW_NODE" >}}

The argument order is old node first, replacement second. Review and commit with [Plan and commit a membership change]({{< product-version-root >}}how-to/cluster-lifecycle/plan-and-commit-a-membership-change/). A replacement transfers the old ownership to the new node; if its location differs, plan any required placement correction as a separate completed change.

## Wait before repeating

Wait for transfers and AAE verification, test application requests, and enable the new node's coverage and routing. Only then retire or repurpose the old node and begin another replacement. If a source fails mid-operation, reassess recovery rather than blindly continuing the rolling sequence.
