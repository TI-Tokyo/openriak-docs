---
title: Conflict-free replicated data types
description: Conflict-free replicated data types define operations whose concurrent effects can be merged. They
  are useful when the application's required behaviour matches the supplied counter, set, map, grow-only set, or
  HyperLogLo
weight: 140
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- architects
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\crdts.md
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
review-by: TI Tokyo/JOM
review_scope: editorial & technical'
restructured_from:
- foundations/data-model/distributed-data-types.md
related:
- reference/data-model-contracts/distributed-data-type-contracts
- how-to/application-data/update-distributed-counters
- how-to/application-data/add-and-remove-members-of-distributed-sets
- how-to/application-data/update-distributed-maps
- tutorials/data-and-concurrency/build-a-shared-counter-and-collection
---

Conflict-free replicated data types define operations whose concurrent effects can be merged. They are useful when the application's required behaviour matches the supplied counter, set, map, grow-only set, or HyperLogLog semantics.

## Operations carry meaning

Incrementing a distributed counter expresses a change, rather than replacing the last value the client read. Concurrent increments can therefore be combined. Set additions and removals have their own rules; removing an observed member is different from replacing an entire collection with a local snapshot.

Maps contain typed fields whose changes can be merged using the field's data-type semantics. A map is not a transaction spanning unrelated objects.

## Context still matters

Some operations, particularly removals, need context from a previous fetch. You should preserve that context and use the matching data-type API. An ordinary object PUT is not a substitute for a data-type update.

## Choose the right structure

A grow-only set cannot remove an element. HyperLogLog estimates distinct observations rather than returning an exact list or exact cardinality. A counter records increments and decrements but does not enforce a non-negative balance across independent writers.

These structures remove some application merge work, while retaining the availability and convergence considerations of a replicated system.
