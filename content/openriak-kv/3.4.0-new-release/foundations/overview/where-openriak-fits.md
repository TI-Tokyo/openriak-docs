---
title: Where OpenRiak fits
description: OpenRiak fits applications that can model their data as independently addressable objects and make
  explicit choices about availability, acknowledgement, and concurrent updates.
weight: 20
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\why-riak-kv.md
source_material:
- legacy-3.2.5
- openriak-discussions
- live-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/#what-is-riak
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/foundations/why-openriak.md
- foundations/foundations/use-cases.md
related:
- foundations/data-and-consistency/quorums-availability-and-durability
- foundations/data-and-consistency/resolving-concurrent-updates
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- how-to/planning-a-deployment/map-application-data-to-objects-and-buckets
- how-to/performance/benchmark-a-representative-workload
---

OpenRiak fits applications that can model their data as independently addressable objects and make explicit choices about availability, acknowledgement, and concurrent updates.

## Workloads with natural keys

User preferences, device state, catalog records, and event-derived views often have stable identifiers. A request can find one object directly without coordinating a join across many records. Separate buckets or bucket types let an application apply different policies to distinct datasets.

The fit depends on update semantics as much as on scale. A preference record may tolerate a merge of concurrent edits. A monetary transfer requiring an atomic change to two accounts needs a transaction mechanism outside ordinary OpenRiak object operations.

## Availability has application consequences

Accepting work during failures can leave replicas temporarily different. The application must decide whether to retry, reconcile siblings, use a mergeable data type, or reject an operation whose prerequisites cannot be met. More acknowledgements can improve a request's resilience but do not create a cross-object transaction.

## Access patterns determine the design

Design keys for direct lookups and indexes for specific discovery queries. Large scans, unbounded result sets, and frequent rewriting of large objects have different costs from small keyed requests. Measure a representative workload, including repair and node loss, before committing to a deployment size.
