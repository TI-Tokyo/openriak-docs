---
title: Causal-context and version-vector representations
description: Causal context identifies the versions a client has observed. Treat it as opaque and return it with
  an update or deletion based on that observed state.
weight: 370
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
- operators
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#version-vector
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/data/version-vectors.md
related:
- how-to/application-data/update-an-object-with-causal-context
- how-to/application-data/resolve-concurrent-object-updates
- reference/http-api/conditional-requests-and-latch-objects
- reference/data-model-contracts/distributed-data-type-contracts
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Causal context identifies the versions a client has observed. Treat it as opaque and return it with an update or deletion based on that observed state.

## Object interfaces

HTTP returns encoded context in `X-Riak-Vclock`. Protocol Buffers carries the binary `vclock` field. Preserve the value without decoding, truncating, or substituting a client-generated clock. When resolving siblings, use the context representing the complete observed sibling set.

## Data-type interfaces

Distributed data types return their own opaque `context`. Pass it in the enclosing data-type update for operations that remove observed state. It is not interchangeable with an ordinary object's vector clock.

## Limits

Context describes causality, not a wall-clock timestamp or a cross-object transaction. A write without the previous context can be concurrent with earlier versions. A timeout can leave the result uncertain even when the client retained context correctly.
