---
title: 'Secondary index design'
description: 'Explain secondary index design, its trade-offs, and its effect on application design.'
weight: 8
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'content-specification'
draft: true
audience:
  - 'architects'
  - 'developers'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain secondary index design, its trade-offs, and its effect on application design.

> [!NOTE]
> This page is a content specification. Replace the guidance below with tested OpenRiak KV 3.4.1 documentation before publishing it.

## Purpose and context

Explain the question that **Secondary index design** answers for architects, developers, or operators using OpenRiak KV 3.4.1. Establish the problem and vocabulary before describing the mechanism, and keep task instructions in linked how-to guides.

## Concepts and mental model

Introduce the participating components, data or control flow, important states, and invariants. Add a diagram or worked narrative when relationships would otherwise be difficult to follow, and define all terms used by the rest of the page.

## How it works

Describe the mechanism from input to observable outcome, including distribution, coordination, persistence, and failure behaviour where relevant. Separate guaranteed behaviour from implementation detail and identify assumptions that depend on configuration.

## Trade-offs and operational implications

Explain what the design optimises, what it costs, and how workload, scale, topology, consistency requirements, and failure modes affect the choice. Connect these trade-offs to decisions readers actually make without turning the page into a procedure.

## Worked example to add

Provide a version-correct scenario that traces one request or state transition through the mechanism. Show the normal path and one failure or concurrency case, then connect the result back to the mental model.

## Boundaries and related topics

State what this explanation does not cover, call out 3.4.0 versus 3.4.1 differences, and link to relevant tutorials, how-to guides, and authoritative reference material.

## In this section

- [Bucket types as namespaces and policy]({{< product-version-root >}}explanation/data-model/bucket-types/) — Explain bucket types as namespaces and policy, its trade-offs, and its effect on application design.
- [Causal context]({{< product-version-root >}}explanation/data-model/causal-context/) — Explain causal context, its trade-offs, and its effect on application design.
- [Conflict resolution strategies]({{< product-version-root >}}explanation/data-model/conflict-resolution/) — Explain conflict resolution strategies, its trade-offs, and its effect on application design.
- [Deletion policies and tombstone retention]({{< product-version-root >}}explanation/data-model/deletion-policies/) — Explain how delete mode, tombstones, reaping, erasure, and compaction affect data removal.
- [Conflict-free replicated data types]({{< product-version-root >}}explanation/data-model/distributed-data-types/) — Explain conflict-free replicated data types, its trade-offs, and its effect on application design.
- [Data model concepts]({{< product-version-root >}}explanation/data-model/) — Introduce the concepts and trade-offs behind OpenRiak data modeling.
- [Keys, objects, and buckets]({{< product-version-root >}}explanation/data-model/keys-objects-and-buckets/) — Explain keys, objects, and buckets, its trade-offs, and its effect on application design.
- [Latch objects]({{< product-version-root >}}explanation/data-model/latch-objects/) — Explain how latch objects support conditional requests and which concurrency guarantees they provide.
- [MapReduce in OpenRiak]({{< product-version-root >}}explanation/data-model/mapreduce/) — Explain mapreduce in openriak, its trade-offs, and its effect on application design.
- [Object merge strategies]({{< product-version-root >}}explanation/data-model/merge-strategies/) — Explain how merge strategies resolve concurrent object versions and where application policy is required.
- [Query API design]({{< product-version-root >}}explanation/data-model/query-api/) — Explain the Query API execution pipeline, expressiveness, consistency, and performance trade-offs.
- [Version vectors and siblings]({{< product-version-root >}}explanation/data-model/version-vectors-and-siblings/) — Explain version vectors and siblings, its trade-offs, and its effect on application design.
