---
title: Resolving concurrent updates
description: Concurrent updates need a rule that reflects the meaning of the application data. OpenRiak can retain
  siblings so that resolving a conflict does not silently discard an independent change.
weight: 130
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- architects
- developers
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-24'
review-by: TI Tokyo/JOM
review_scope: editorial & technical
restructured_from:
- foundations/data-model/conflict-resolution.md
- foundations/data-model/merge-strategies.md
related:
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/data-and-consistency/conflict-free-replicated-data-types
- foundations/data-and-consistency/conditional-updates-and-latch-objects
- how-to/application-data/resolve-concurrent-object-updates
---

Concurrent updates need a rule that reflects the meaning of the application data. OpenRiak can retain siblings so that resolving a conflict does not silently discard an independent change.

## Choose a merge rule before conflicts occur

For a shopping collection, a merge may combine independently added items. For a document, it may require a field-level merge or a user's decision. Choosing whichever value has the latest timestamp can discard valid work and depends on clocks as well as application semantics.

A good automatic rule is deterministic and remains correct when applied again. Where possible, it should give the same result regardless of the order in which replicas or retries present the inputs.

## Resolution is another write

Read all siblings and preserve their combined context. Compute the application's resolved content and submit a write with that context. If another writer updates the object concurrently, the result can contain another conflict; resolution is not an exclusive lock over future writes.

## Alternatives

Distributed data types provide defined merge behaviour for supported structures. Conditional updates can reduce ordinary races, but their boundaries still matter. Turning off sibling retention changes how competing content is discarded; it does not make the underlying operations transactional.
