---
title: Choose replication and acknowledgement policies
description: Choose replica and acknowledgement policies that meet the application's failure and durability requirements.
  Use [[F13]] and [[F14]] if you need the relationship between replicas, causal context, and quorums.
weight: 80
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
- https://openriak.github.io/riak/InitialDesignDecisions.html#data-distribution-guarantees
- https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience
- https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience---changing-the-choice
- https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience---making-a-choice
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/plan/choose-intra-cluster-resilience.md
related:
- how-to/application-data/create-and-activate-bucket-types
- how-to/application-data/make-conditional-reads-and-writes
- how-to/planning-a-deployment/choose-a-multi-cluster-topology
- reference/http-api/object-request-options
- foundations/data-and-consistency/quorums-availability-and-durability
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Choose replica and acknowledgement policies that meet the application's failure and durability requirements. Use [Quorums, availability, and durability]({{< product-version-root >}}foundations/data-and-consistency/quorums-availability-and-durability/) and [Causality, version vectors, and siblings]({{< product-version-root >}}foundations/data-and-consistency/causality-version-vectors-and-siblings/) if you need the relationship between replicas, causal context, and quorums.

## State the failure requirement

Record which node failures the application must tolerate, whether requests may use fallback replicas, and whether successful writes must be persisted to storage before acknowledgement. Quorum settings do not turn ordinary objects into linearizable transactions.

## Define bucket-type policies

Select `n_val` for replica count and the appropriate read/write acknowledgement properties for each data class. Check `r`, `pr`, `w`, `pw`, `dw`, `node_confirms`, and `sync_on_write` in [Bucket properties and defaults]({{< product-version-root >}}reference/configuration/bucket-properties-and-defaults/). Use stricter request overrides only when the operation needs them, and handle timeout or insufficient-replica responses explicitly.

## Test failure and ambiguity

Create and activate a test bucket type, perform concurrent writes, then stop a test node and repeat the workload. Confirm both the accepted operations and rejected operations match the policy. A timed-out write may still have taken effect; retry with the application's idempotency and causal-context rules.

## Apply consistently

Create matching type definitions in every receiving cluster before replicating typed objects. For a change to existing replica placement, rehearse migration or repair rather than assuming a property edit has already copied every object to the new replica set.
