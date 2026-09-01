---
title: 'How Prefix Multi routing works'
description: 'Explain how prefix multi routing works, its constraints, and the workloads for which it is appropriate.'
weight: 9
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'content-specification'
draft: true
audience:
  - 'architects'
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain how prefix multi routing works, its constraints, and the workloads for which it is appropriate.

> [!NOTE]
> This page is a content specification. Replace the guidance below with tested OpenRiak KV {{< current-version >}} documentation before publishing it.

## Purpose and context

Explain the question that **How Prefix Multi routing works** answers for architects, developers, or operators using OpenRiak KV {{< current-version >}}. Establish the problem and vocabulary before describing the mechanism, and keep task instructions in linked how-to guides.

## Concepts and mental model

Introduce the participating components, data or control flow, important states, and invariants. Add a diagram or worked narrative when relationships would otherwise be difficult to follow, and define all terms used by the rest of the page.

## How it works

Describe the mechanism from input to observable outcome, including distribution, coordination, persistence, and failure behaviour where relevant. Separate guaranteed behaviour from implementation detail and identify assumptions that depend on configuration.

## Trade-offs and operational implications

Explain what the design optimises, what it costs, and how workload, scale, topology, consistency requirements, and failure modes affect the choice. Connect these trade-offs to decisions readers actually make without turning the page into a procedure.

## Worked example to add

Provide a version-correct scenario that traces one request or state transition through the mechanism. Show the normal path and one failure or concurrency case, then connect the result back to the mental model.

## Boundaries and related topics

State what this explanation does not cover, note differences from earlier releases, and link to relevant tutorials, how-to guides, and authoritative reference material.

## In this section

- [How Bitcask stores data]({{< product-version-root >}}foundations/storage/bitcask/) — Explain how bitcask stores data, its constraints, and the workloads for which it is appropriate.
- [Storage capacity planning]({{< product-version-root >}}foundations/storage/capacity-planning/) — Explain storage capacity planning, its constraints, and the workloads for which it is appropriate.
- [Choosing a storage backend]({{< product-version-root >}}foundations/storage/choosing-backend/) — Explain choosing a storage backend, its constraints, and the workloads for which it is appropriate.
- [Storage architecture]({{< product-version-root >}}foundations/storage/) — Introduce storage engine design, workload fit, capacity implications, and backend trade-offs.
- [How LevelDB stores data]({{< product-version-root >}}foundations/storage/leveldb/) — Explain how leveldb stores data, its constraints, and the workloads for which it is appropriate.
- [How Leveled stores data]({{< product-version-root >}}foundations/storage/leveled/) — Explain how leveled stores data, its constraints, and the workloads for which it is appropriate.
- [How the Memory backend stores data]({{< product-version-root >}}foundations/storage/memory/) — Explain how the memory backend stores data, its constraints, and the workloads for which it is appropriate.
- [How multiple backends work]({{< product-version-root >}}foundations/storage/multi-backend/) — Explain how multiple backends work, its constraints, and the workloads for which it is appropriate.
