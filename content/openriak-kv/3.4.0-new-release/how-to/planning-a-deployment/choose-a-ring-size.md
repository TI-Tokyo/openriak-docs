---
title: Choose a ring size
description: Choose the partition count before a new cluster receives data. The ring controls how work is divided
  into virtual nodes; see [[F5]] for the model.
weight: 60
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#ring-size
- https://openriak.github.io/riak/InitialDesignDecisions.html#ring-size---making-a-choice
tags:
- diataxis
- kv
- how-to
- quickdocs
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/plan/choose-ring-size.md
related:
- how-to/node-configuration/configure-node-identity-directories-and-the-initial-ring
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
- how-to/replication-and-reconciliation/migrate-to-another-cluster-using-replication
- reference/operations-and-observability/claim-algorithms-and-placement-constraints
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/cluster-architecture/replica-placement-and-failure-domains
---

Choose the partition count before a new cluster receives data. The ring controls how work is divided into virtual nodes; see [Rings, partitions, and virtual nodes]({{< product-version-root >}}foundations/cluster-architecture/rings-partitions-and-virtual-nodes/) for the model.

## Estimate the deployment range

Record the initial and expected maximum number of physical nodes, replication policy, and recovery-time target. Evaluate candidate power-of-two ring sizes in a test cluster with the intended backend. More partitions provide finer placement but also increase per-vnode overhead and maintenance work.

## Set the initial value

Use the same `ring_size` on every new node before starting or joining them:

{{< configuration-reference-item config-name="ring_size" >}}

Do not change this setting on an existing data-bearing cluster as a resizing procedure. If the current partition count is unsuitable, prepare a new cluster and migrate with replication.

## Verify placement

Join the test members, inspect the proposed ownership plan, and wait for handoffs to complete. Measure partition balance, vnode memory, startup time, and recovery under the expected largest deployment. Save the chosen value with the provisioning configuration.
