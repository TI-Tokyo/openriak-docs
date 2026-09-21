---
title: Map application data to objects and buckets
description: Design object keys, bucket boundaries, and query paths before committing to a storage layout. Start
  with the application's reads and updates, including how it will resolve concurrent changes.
weight: 40
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\data-modeling.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\key-value-modeling.md
source_material:
- legacy-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#mapping-data-to-objects
- https://openriak.github.io/riak/InitialDesignDecisions.html#mapping-data-to-objects---changing-the-choice
- https://openriak.github.io/riak/InitialDesignDecisions.html#mapping-data-to-objects---making-a-choice
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/plan/map-data-to-objects.md
related:
- how-to/application-data/create-and-activate-bucket-types
- how-to/indexes-and-queries/add-and-query-secondary-indexes
- reference/data-model-contracts/keys-and-object-representations
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Design object keys, bucket boundaries, and query paths before committing to a storage layout. Start with the application's reads and updates, including how it will resolve concurrent changes.

## List access patterns

For each operation, record the identifier supplied by the caller, the fields returned, expected object size, read/write rate, and acceptable staleness. Prefer direct key lookups when the caller already has an identifier. For discovery by attributes, identify the required secondary indexes and confirm the backend capability in [Backend capability matrix]({{< product-version-root >}}reference/orientation-and-compatibility/backend-capability-matrix/).

## Choose the object boundary

Keep fields together when they are normally read and updated together. Separate independently updated or unbounded collections so one growing object does not become a contention or memory problem. Do not assume a transaction spans several keys.

Choose stable keys that the application can reconstruct. Include a tenant or other namespace in the key or bucket when necessary, and apply one encoding consistently in every client. Store an explicit schema version if the value format will evolve.

## Assign policies

Use bucket types to group data requiring the same conflict, durability, or data-type policy. Avoid creating a type per customer unless each truly needs a distinct policy. Define what a missing key means and how the application handles siblings, retries, and partial multi-object operations.

## Test the design

Create representative objects, query them through each access path, then issue concurrent updates from two clients. Measure payload size and response latency with realistic distributions. Confirm that the application can merge conflicts and read both old and new schema versions before adopting the layout.
