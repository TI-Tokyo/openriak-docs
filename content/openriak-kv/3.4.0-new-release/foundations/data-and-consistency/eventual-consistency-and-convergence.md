---
title: Eventual consistency and convergence
description: Eventual consistency allows replicas to differ temporarily. When updates stop and the required communication
  and repair work succeeds, replicas can converge on the same object state.
weight: 100
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- architects
- developers
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\eventual-consistency.md
source_material:
- legacy-3.2.5
- live-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/RiakTheoryGuide.html#eventual-consistency
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-22'
review-by: TI Tokyo/JOM
review_scope: editorial & technical
restructured_from:
- foundations/consistency/eventual-consistency.md
related:
- foundations/data-and-consistency/quorums-availability-and-durability
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/data-and-consistency/resolving-concurrent-updates
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/real-time-replication-and-fullsync
---

Eventual consistency allows replicas to differ temporarily. When updates stop and the required communication and repair work succeeds, replicas can converge on the same object state.

## Different does not always mean conflicting

A replica may simply be behind: one version causally follows another, and the older copy can be replaced. Two independently created versions may instead be concurrent. Convergence then requires the configured object semantics or the application to combine them.

Read repair reacts to differences observed during reads. Active anti-entropy looks for differences independently of application reads, including objects that are rarely accessed. Replication between clusters adds another asynchronous path with its own queues and reconciliation.

## What a successful request tells you

A write acknowledgement confirms the request's acknowledgement conditions, not that all replicas everywhere already contain the result. A read reflects the responses available under its policy. Stronger acknowledgement requirements change the trade-off between availability, latency, and surviving particular failures; they do not automatically provide serial execution.

