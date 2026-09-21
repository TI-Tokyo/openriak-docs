---
title: Replication references and queue payloads
description: A replication source queue contains references to current object changes for one consumer relationship.
  A reference can carry an object or identify an object to fetch later.
weight: 970
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\app-guide\replication-properties.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\multi-datacenter\per-bucket-replication.md
source_material:
- legacy-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ReplicationGuide.html#concepts---replication-references
- https://openriak.github.io/riak/ReplicationGuide.html#concepts---replication-triggers
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/replication/references-and-triggers.md
related:
- reference/replication-interfaces/internal-fetch-and-membership-api
- reference/replication-interfaces/next-generation-replication-runtime-controls
- reference/configuration/next-generation-replication-settings
- how-to/replication-and-reconciliation/configure-replication-queues-and-filters
- foundations/replication-and-repair/replication-sources-queues-and-sinks
---

A replication source queue contains references to current object changes for one consumer relationship. A reference can carry an object or identify an object to fetch later.

## Queue contract

The source assesses each coordinated write against configured filters and adds it to every matching destination queue. Priorities distinguish real-time changes from reconciliation or bulk seeding. A queue can spill references to disk to limit memory use, but its contents remain temporary and can be lost on source restart or discarded at overflow limits.

## Delivery

Sink workers fetch a reference or object, then push the value into the local cluster before requesting another. If a reference requires a fetch, the source resolves the current stored object. The sink push preserves the supplied causal state and does not become an ordinary coordinated write that automatically relays to a third cluster.

## Compatibility boundary

Queue payloads and internal object encodings are release-sensitive internal interfaces. Use the documented replication clients and matching protocol contracts. Independent external consumers must verify their supported encoding and reconciliation behaviour rather than treating queue files as a durable public event log.
