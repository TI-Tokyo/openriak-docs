---
title: Perform a rolling restart
description: Restart cluster members in sequence, waiting for each member's recovery before stopping the next. Confirm
  the cluster can tolerate the unavailable member throughout the operation.
weight: 760
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery\rolling-restart.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#rolling-restart
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/rolling-restart.md
related:
- how-to/cluster-lifecycle/start-stop-or-restart-a-node
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- tutorials/cluster-operations-and-recovery/perform-a-rolling-restart
- foundations/cluster-architecture/membership-gossip-and-handoff
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
---

Restart cluster members in sequence, waiting for each member's recovery before stopping the next. Confirm the cluster can tolerate the unavailable member throughout the operation.

## Prepare

Record membership, outstanding transfers, client latency, and the intended configuration change. Ensure there is no overlapping membership transition or unresolved replica loss. A memory backend loses its local data on restart and needs a different recovery plan.

## Restart one member

Drain it from client routing, stop it gracefully through [Start, stop, or restart a node]({{< product-version-root >}}how-to/cluster-lifecycle/start-stop-or-restart-a-node/), and start it with the intended configuration. Watch startup logs and verify the process responds.

## Wait for recovery

{{< cli-example key="shell:riak admin member-status" >}}
{{< cli-example key="shell:riak admin transfers" >}}

Allow both the triggering and completion of hinted handoffs. Check AAE and representative application operations before returning the node to routing. Pause the sequence if errors, queue growth, or slow recovery exceed the plan.

Repeat for the next member only after the previous one is healthy. At the end, compare effective configuration and health across all members.
