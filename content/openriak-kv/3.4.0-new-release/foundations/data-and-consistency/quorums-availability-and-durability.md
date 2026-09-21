---
title: Quorums, availability, and durability
description: Request acknowledgements determine how much replica participation a client requires before an operation
  succeeds. Durability also depends on where those replicas live and what their storage acknowledgements mean.
weight: 110
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- developers
- operators
source_material:
- live-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/RiakTheoryGuide.html#quorum-on-read-write-and-query
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/consistency/read-write-quorums.md
- foundations/foundations/availability-and-failure-tolerance.md
related:
- foundations/cluster-architecture/replica-placement-and-failure-domains
- foundations/data-and-consistency/eventual-consistency-and-convergence
- how-to/planning-a-deployment/choose-replication-and-acknowledgement-policies
- reference/http-api/object-request-options
- reference/configuration/bucket-properties-and-defaults
---

Request acknowledgements determine how much replica participation a client requires before an operation succeeds. Durability also depends on where those replicas live and what their storage acknowledgements mean.

## Read and write requirements

Read and write options select the required responses. Primary requirements restrict which responses count; durable-write requirements concern persistence acknowledgements. The effective values come from request options and bucket policy.

The symbols and accepted values are defined in the object-request reference. Consult the generated configuration catalogue for release-specific settings rather than assuming a numerical default.

## Why overlapping counts are not serial execution

Requiring overlapping read and write response counts can reduce stale observations under suitable assumptions. It does not remove concurrency, fallback placement, partitions, or independent coordination. In particular, quorum arithmetic alone does not turn ordinary OpenRiak operations into strongly consistent transactions.

## Choosing a trade-off

Higher requirements can make a request fail when fewer replicas are reachable and can expose the latency of slower replicas. Lower requirements can allow progress through more failures but leave more uncertainty about which copies hold the result.

For example, an application can choose to reject a critical update when its required primary responses are unavailable. That is an explicit application policy, not evidence that the cluster has lost every copy.
