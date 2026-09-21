---
title: Plan and commit a membership change
description: Review and commit staged membership changes as one deliberate cluster operation. Do not commit while
  another operator is staging unrelated changes.
weight: 710
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
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#forming-and-expanding-a-riak-cluster
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---commit-the-plan
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---plan-a-change
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---verify-the-plan
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/plan-and-commit-cluster-change.md
related:
- how-to/cluster-lifecycle/add-nodes-to-a-cluster
- how-to/cluster-lifecycle/remove-a-node-from-a-cluster
- how-to/cluster-lifecycle/replace-a-failed-node
- how-to/cluster-lifecycle/replace-nodes-without-stopping-the-cluster
- how-to/cluster-lifecycle/monitor-and-control-handoffs
- foundations/cluster-architecture/membership-gossip-and-handoff
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
---

Review and commit staged membership changes as one deliberate cluster operation. Do not commit while another operator is staging unrelated changes.

## Check the starting state

Confirm membership, reachability, free space, and outstanding transfers. Record the intended old and new Erlang node names and coordinate an exclusive change window.

{{< cli-example key="shell:riak admin member-status" >}}
{{< cli-example key="shell:riak admin transfers" >}}

## Stage and review

Stage the required join, leave, or replacement using its how-to. Then generate the plan:

{{< cli-example key="shell:riak admin cluster plan" >}}

Check every member added or removed, proposed ownership, location constraints, and any warnings. If the plan contains unexpected work, clear the staged changes and restage the intended operation:

{{< cli-example key="shell:riak admin cluster clear" >}}

## Commit and monitor

{{< cli-example key="shell:riak admin cluster commit" >}}

Watch transfers, membership, client errors, and disk pressure until the final ownership is reached. A successful commit starts the transition; it does not mean data movement is complete. Clearing staged changes is not a rollback of an already committed transition.
