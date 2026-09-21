---
title: Write-once interface
description: The historical write-once path optimizes a restricted immutable-object workflow and is deprecated.
  It is not equivalent to a conditional ordinary PUT.
weight: 1250
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\app-guide\write-once.md
source_material:
- legacy-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#write-once-path-api
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/specialized-apis/write-once-api.md
related:
- how-to/application-data/store-immutable-data-through-the-write-once-path
- reference/http-api/store-object
- reference/http-api/conditional-requests-and-latch-objects
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/storage-and-performance/storage-backend-trade-offs
---

The historical write-once path optimizes a restricted immutable-object workflow and is deprecated. It is not equivalent to a conditional ordinary PUT.

## Policy

A dedicated bucket-type property selects the write-once behaviour. Clients must use unique immutable keys and understand the interface's acknowledgement and conflict limitations. Do not change an existing mutable workload to write-once merely to reduce latency.

## Feature constraints

The path does not perform ordinary coordinated PUT processing and is incompatible with real-time replication of those writes. Do not assume indexes, hooks, conditional updates, or repair behaviour match the normal object path.

## Transition

Use ordinary object storage with an explicit key-uniqueness or conditional-write policy for new applications. A migration must preserve the old data and coordinate writers; changing a property or endpoint alone does not prove the existing dataset was converted.
