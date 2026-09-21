---
title: Add nodes to a cluster
description: Add empty, configured nodes to an existing cluster, then wait for ownership transfers before relying
  on their capacity.
weight: 720
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
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#forming-and-expanding-a-riak-cluster
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---staging-a-change
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/add-node.md
related:
- how-to/node-configuration/configure-node-identity-directories-and-the-initial-ring
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
- how-to/cluster-lifecycle/monitor-and-control-handoffs
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- tutorials/cluster-operations-and-recovery/add-and-remove-cluster-members
- foundations/cluster-architecture/membership-gossip-and-handoff
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
previous_page: how-to/installation/verify-an-installation
---

Add empty, configured nodes to an existing cluster, then wait for ownership transfers before relying on their capacity.

## Prepare the new members

Install a compatible release, configure unique resolvable identities, matching cookie and initial ring choices, and the intended storage. Verify network reachability and that the new data directories do not contain another deployment's state.

## Stage the join

Run on each new node, replacing the argument with an existing member's exact Erlang name:

{{< cli-example key="shell:riak admin cluster join" args="riak@EXISTING_NODE" >}}

On an existing member, follow [Plan and commit a membership change]({{< product-version-root >}}how-to/cluster-lifecycle/plan-and-commit-a-membership-change/) to review and commit the complete plan. Check placement and location constraints before proceeding.

## Verify completion

{{< cli-example key="shell:riak admin member-status" >}}
{{< cli-example key="shell:riak admin transfers" >}}

Wait for valid membership and completed transfers. Check sample reads, writes, and AAE progress, then add the nodes to client routing. Provision replication consumers and monitoring deliberately; joining does not copy every external service configuration.
