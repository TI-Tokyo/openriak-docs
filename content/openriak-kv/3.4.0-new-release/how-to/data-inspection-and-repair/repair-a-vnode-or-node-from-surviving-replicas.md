---
title: Repair a vnode or node from surviving replicas
description: Repair lost vnode or node data from surviving replicas after membership and storage are ready. This
  process cannot recover data for which no valid copy remains.
weight: 1060
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#completing-a-repair
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#repair-an-individual-vnode
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/repair-vnode.md
related:
- how-to/cluster-lifecycle/replace-a-failed-node
- how-to/cluster-lifecycle/monitor-and-control-handoffs
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- reference/commands/repair-and-recovery-commands
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
---

Repair lost vnode or node data from surviving replicas after membership and storage are ready. This process cannot recover data for which no valid copy remains.

## Prepare the recovering node

Complete the rejoin or replacement procedure in [Replace a failed node]({{< product-version-root >}}how-to/cluster-lifecycle/replace-a-failed-node/) or [Recover a failed node or choose replacement]({{< product-version-root >}}how-to/troubleshooting/recover-a-failed-node-or-choose-replacement/). Keep the incomplete node out of coverage queries and temporarily suspend its TicTac exchanges so they do not compete with bulk recovery:

{{< cli-example key="erlang:riak_client:remove_node_from_coverage" >}}
{{< cli-example key="erlang:riak_client:tictacaae_suspend_node" >}}

Run these on the recovering node through [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). Persist the intended coverage policy if a restart during recovery must retain it.

## Submit repair

For all owned vnodes on the recovering node:

{{< cli-example key="erlang:riak_client:repair_node" >}}

For one partition, use the dedicated repair interface in [Repair and recovery commands]({{< product-version-root >}}reference/commands/repair-and-recovery-commands/) with the exact integer partition ID. Keep the scope explicit; a partition ID is not a short node number.

## Follow completion

Repair uses handoffs. Monitor progress using [Monitor and control handoffs]({{< product-version-root >}}how-to/cluster-lifecycle/monitor-and-control-handoffs/) and control resource pressure with [Control repair impact during application traffic]({{< product-version-root >}}how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic/). When transfers complete, resume TicTac AAE:

{{< cli-example key="erlang:riak_client:tictacaae_resume_node" >}}

Wait for verification of the repaired vnodes, then restore the configured coverage state:

{{< cli-example key="erlang:riak_client:reset_node_for_coverage" >}}

Verify application reads and indexes before returning the node to normal routing. If surviving replicas are insufficient, switch to the wider recovery plan in [Recover a cluster after a widespread failure]({{< product-version-root >}}how-to/cluster-lifecycle/recover-a-cluster-after-a-widespread-failure/).
