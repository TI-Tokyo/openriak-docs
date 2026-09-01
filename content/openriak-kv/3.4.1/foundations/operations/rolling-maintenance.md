---
title: 'Rolling maintenance'
description: 'Explain rolling maintenance, including relevant state transitions, risks, and recovery assumptions.'
weight: 6
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'content-specification'
draft: true
audience:
  - 'operators'
  - 'architects'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain rolling maintenance, including relevant state transitions, risks, and recovery assumptions.

> [!NOTE]
> This page is a content specification. Replace the guidance below with tested OpenRiak KV {{< current-version >}} documentation before publishing it.

## Purpose and context

Explain the question that **Rolling maintenance** answers for architects, developers, or operators using OpenRiak KV {{< current-version >}}. Establish the problem and vocabulary before describing the mechanism, and keep task instructions in linked how-to guides.

## Concepts and mental model

Introduce the participating components, data or control flow, important states, and invariants. Add a diagram or worked narrative when relationships would otherwise be difficult to follow, and define all terms used by the rest of the page.

## How it works

Describe the mechanism from input to observable outcome, including distribution, coordination, persistence, and failure behaviour where relevant. Separate guaranteed behaviour from implementation detail and identify assumptions that depend on configuration.

## Trade-offs and operational implications

Explain what the design optimises, what it costs, and how workload, scale, topology, consistency requirements, and failure modes affect the choice. Connect these trade-offs to decisions readers actually make without turning the page into a procedure.

## Worked example to add

Provide a version-correct scenario that traces one request or state transition through the mechanism. Show the normal path and one failure or concurrency case, then connect the result back to the mental model.

## Boundaries and related topics

State what this explanation does not cover, call out {{< previous-version >}} versus {{< current-version >}} differences, and link to relevant tutorials, how-to guides, and authoritative reference material.

## In this section

- [Backups and restores]({{< product-version-root >}}foundations/operations/backups-and-restores/) — Explain backups and restores, including relevant state transitions, risks, and recovery assumptions.
- [Garbage collection and compaction]({{< product-version-root >}}foundations/operations/garbage-collection/) — Explain how reaping, erasure, backend compaction, and backup-file cleanup reclaim storage.
- [Operational concepts]({{< product-version-root >}}foundations/operations/) — Introduce the system behaviors operators need to understand before changing or recovering a cluster.
- [Node failure and recovery]({{< product-version-root >}}foundations/operations/node-failure-and-recovery/) — Explain node failure and recovery, including relevant state transitions, risks, and recovery assumptions.
- [Object deletion and tombstones]({{< product-version-root >}}foundations/operations/object-deletion-and-tombstones/) — Explain object deletion and tombstones, including relevant state transitions, risks, and recovery assumptions.
- [Store, vnode, range, and object repair]({{< product-version-root >}}foundations/operations/repair-granularity/) — Explain the available repair scopes and how to choose the least disruptive effective option.
- [Ring changes and handoffs]({{< product-version-root >}}foundations/operations/ring-changes-and-handoffs/) — Explain ring changes and handoffs, including relevant state transitions, risks, and recovery assumptions.
- [Upgrade and downgrade behavior]({{< product-version-root >}}foundations/operations/upgrade-and-downgrade/) — Explain upgrade and downgrade behavior, including relevant state transitions, risks, and recovery assumptions.
