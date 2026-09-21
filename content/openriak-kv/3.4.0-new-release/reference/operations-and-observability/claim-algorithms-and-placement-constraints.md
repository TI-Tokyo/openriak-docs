---
title: Claim algorithms and placement constraints
description: Claim algorithms assign partitions during a planned membership change. Replica and location constraints
  influence placement but must still be checked against the available members and ring.
weight: 1070
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- architects
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---choose_claim_v2-default
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---choose_claim_v3
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---choose_claim_v4-recommended
tags:
- diataxis
- kv
- reference
- quickdocs
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/operations/cluster-claim-algorithms.md
related:
- how-to/planning-a-deployment/choose-a-ring-size
- how-to/planning-a-deployment/choose-replication-and-acknowledgement-policies
- how-to/cluster-lifecycle/plan-and-commit-a-membership-change
- how-to/cluster-lifecycle/replace-nodes-without-stopping-the-cluster
- foundations/cluster-architecture/replica-placement-and-failure-domains
---

Claim algorithms assign partitions during a planned membership change. Replica and location constraints influence placement but must still be checked against the available members and ring.

## Configuration

{{< configuration-reference-table >}}
^(choose_claim_fun|target_n_val|target_location_n_val|ring_size)$
{{< /configuration-reference-table >}}

## Algorithm families

The release retains multiple claim implementations. Their balancing and location behaviour differ; select the configured implementation deliberately and inspect every proposed plan. A placement target cannot create additional physical failure domains when too few suitable nodes exist.

## Replacement behaviour

A direct replacement inherits the departing node's ownership. Moving the replacement to another location can therefore require a separate completed placement change. Avoid treating a node-location edit as proof that all replicas have already moved to satisfy the new topology.
