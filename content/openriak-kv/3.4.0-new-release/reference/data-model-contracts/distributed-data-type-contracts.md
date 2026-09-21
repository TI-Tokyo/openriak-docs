---
title: Distributed data-type contracts
description: Distributed data types accept operations that the database merges across replicas. Their namespace
  is selected by an active bucket type whose datatype matches the operation.
weight: 380
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\data-types.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#the-data-type-api
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/data/distributed-data-types.md
related:
- reference/http-api/distributed-data-type-operations
- reference/protocol-buffers-api/fetch-data-type-messages
- reference/protocol-buffers-api/update-data-type-messages
- reference/protocol-buffers-api/counter-operations
- reference/protocol-buffers-api/set-operations
- reference/protocol-buffers-api/map-operations
- reference/protocol-buffers-api/grow-only-and-union-operations
- foundations/data-and-consistency/conflict-free-replicated-data-types
---

Distributed data types accept operations that the database merges across replicas. Their namespace is selected by an active bucket type whose datatype matches the operation.

## Value families

- Counter: a signed accumulated integer, updated by increments.
- Set: unique binary members with context-dependent removal.
- Grow-only set: unique binary members with additions only.
- Map: typed fields containing counters, sets, maps, registers, or flags according to the operation schema.
- HyperLogLog: an approximate distinct count updated by adding identifiers.

## Context and retries

Fetch context before removing observed set members or map fields. A fresh operation can be applied more than once if blindly retried after an uncertain timeout, especially increments. Client identity is not a general deduplication token for these operations.

## Limits

One rapidly updated datatype key can become a hot key. Large sets and maps can accumulate substantial metadata; keep object growth bounded. The ordinary secondary-index Query API does not query fields inside these datatype values. Datatype context and ordinary object vector clocks use separate contracts.

The HTTP and PB pages below define the operations and wire representations.
