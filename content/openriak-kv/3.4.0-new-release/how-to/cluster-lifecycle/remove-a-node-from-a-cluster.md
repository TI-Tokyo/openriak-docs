---
title: Remove a node from a cluster
description: Remove a healthy node through a graceful leave so its owned data can transfer to surviving members.
  Use [[H73]] for a failed node that cannot hand data off.
weight: 730
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
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#shrinking-a-cluster
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/remove-node.md
related:
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
- how-to/cluster-lifecycle/monitor-and-control-handoffs
- how-to/cluster-lifecycle/replace-a-failed-node
- tutorials/cluster-operations-and-recovery/add-and-remove-cluster-members
- foundations/cluster-architecture/membership-gossip-and-handoff
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
---

Remove a healthy node through a graceful leave so its owned data can transfer to surviving members. Use [Replace a failed node]({{< product-version-root >}}how-to/cluster-lifecycle/replace-a-failed-node/) for a failed node that cannot hand data off.

## Check capacity and health

Confirm the remaining cluster can hold the data and meet replica-placement requirements. Complete other ownership changes first and drain client connections from the departing member.

## Stage the leave

Run on the departing node:

{{< cli-example key="shell:riak admin cluster leave" >}}

Review and commit the plan with [Plan and commit a membership change]({{< product-version-root >}}how-to/cluster-lifecycle/plan-and-commit-a-membership-change/). Keep the node running and its storage intact while transfers proceed.

## Verify and decommission

Monitor handoffs until the leave is complete and the node no longer owns partitions. Check surviving membership and application requests before stopping or removing its infrastructure. Preserve any required backup and audit evidence. Do not erase data merely because the leave command was accepted.
