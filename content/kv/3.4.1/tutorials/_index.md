---
title: 'Tutorials'
description: 'Introduce the guided learning paths and state what readers will build in each one.'
weight: 1
diataxis: 'tutorial'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'content-specification'
draft: true
audience:
  - 'learners'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce the guided learning paths and state what readers will build in each one.

> [!NOTE]
> This page is a content specification. Replace the guidance below with tested OpenRiak KV 3.4.1 documentation before publishing it.

## Learning outcome

State the concrete artefact or working OpenRiak KV behaviour that the reader will produce, the concepts they will encounter, and the approximate scope of the exercise. Keep this a guided learning path rather than a catalogue of every available option.

## Scenario and prerequisites

Define a realistic, disposable scenario for **Tutorials**. List the exact OpenRiak KV 3.4.1 environment, client tools, permissions, sample data, and prior knowledge required, including a safe way to reset the exercise.

## Guided exercise to write

Provide sequential, tested steps that start from a known state. Each step should explain what the reader is doing, show version-correct commands or code, describe the expected result, and build directly on the previous step without unexplained alternatives.

## Verify the result

Add observable success criteria: the expected client response, stored data or cluster state, and the logs or status output that demonstrate the exercise succeeded. Include one deliberate check of the most likely failure mode.

## Troubleshooting and cleanup

Document the errors a learner is likely to make, how to diagnose them without destructive changes, and how to remove sample data or return the environment to its starting state.

## Next steps

Link to the relevant how-to guides for real tasks, explanation pages for the underlying design, and reference pages for complete options and constraints.

## In this section

- [Build a first OpenRiak application](/kv/3.4.1/tutorials/first-application/) — Introduce language-specific learning paths for storing, reading, updating, querying, and deleting data.
- [Learn OpenRiak with a first cluster](/kv/3.4.1/tutorials/first-cluster/) — Introduce supported learning environments for creating a disposable first cluster.
- [Learn cluster operations](/kv/3.4.1/tutorials/operations/) — Introduce safe practice scenarios for common OpenRiak cluster operations.
- [Learn the Query API](/kv/3.4.1/tutorials/query-api/) — Introduce a guided learning path for indexing, querying, and interpreting a small search dataset.
- [Learn multi-cluster replication](/kv/3.4.1/tutorials/replication/) — Introduce a guided two-cluster environment for learning TicTac AAE and next-generation replication.
- [Learn OpenRiak security](/kv/3.4.1/tutorials/security/) — Introduce a guided environment for learning OpenRiak authentication, TLS, and authorization.
