---
title: Replace a failed node
description: Replace a node whose storage is lost or cannot be trusted, then repair the new member from surviving
  replicas. First determine whether the original node can simply return with intact data using [[H132]].
weight: 740
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\replacing-node.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#administratively-downing-a-node
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#forcing-a-replace
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#reactive-replacement
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/replace-node.md
related:
- how-to/troubleshooting/recover-a-failed-node-or-choose-replacement
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
- foundations/cluster-architecture/membership-gossip-and-handoff
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
---

Replace a node whose storage is lost or cannot be trusted, then repair the new member from surviving replicas. First determine whether the original node can simply return with intact data using [Recover a failed node or choose replacement]({{< product-version-root >}}how-to/troubleshooting/recover-a-failed-node-or-choose-replacement/).

## Isolate the failed member

Prevent the failed process from returning unexpectedly. Inspect cluster status and mark the known failed member down from a healthy node when necessary:

{{< cli-example key="shell:riak admin cluster status" >}}
{{< cli-example key="shell:riak admin down" args="riak@FAILED_NODE" >}}

Confirm enough surviving data exists to repair the affected partitions. Preserve failed storage for investigation rather than overwriting it.

## Prepare and stage the replacement

Configure a new empty node with compatible release, cookie, and storage. Keep it out of coverage queries while it has no complete data. For a replacement with a new name, stage its join, then force replacement of the failed member:

{{< cli-example key="shell:riak admin cluster join" args="riak@HEALTHY_NODE" >}}
{{< cli-example key="shell:riak admin cluster force-replace" args="riak@FAILED_NODE riak@NEW_NODE" >}}

Run join on the new node and the replacement command on a participating member. Review and commit using [Plan and commit a membership change]({{< product-version-root >}}how-to/cluster-lifecycle/plan-and-commit-a-membership-change/). For same-identity recovery, follow the rejoin path in [Recover a failed node or choose replacement]({{< product-version-root >}}how-to/troubleshooting/recover-a-failed-node-or-choose-replacement/); never run two nodes with the same identity.

## Repair and return to service

Follow [Repair a vnode or node from surviving replicas]({{< product-version-root >}}how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas/) to repair the empty node, monitor transfers, resume AAE, and wait for convergence before enabling coverage and application traffic. A committed replacement is not evidence that the new node already holds its data.
