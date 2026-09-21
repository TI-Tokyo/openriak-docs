---
title: Conditional updates and latch objects
description: Conditional updates check that an object is absent or still has the state a client observed before
  accepting a change. They reduce common update races but do not give ordinary OpenRiak objects a formal strong-consistency
weight: 150
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- developers
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#conditional-requests
- https://openriak.github.io/riak/ObjectAPI.html#use-of-request-header---if-none-match
- https://openriak.github.io/riak/ObjectAPI.html#use-of-request-header---x-riak-if-not-modified-non-standard-riak-header
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/consistency/conditional-requests.md
- foundations/data-model/latch-objects.md
related:
- reference/http-api/conditional-requests-and-latch-objects
- how-to/application-data/make-conditional-reads-and-writes
- how-to/application-data/coordinate-an-update-with-a-latch-object
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Conditional updates check that an object is absent or still has the state a client observed before accepting a change. They reduce common update races but do not give ordinary OpenRiak objects a formal strong-consistency guarantee.

## Checks and coordination

An API-only check can race with a concurrent write. Token-based modes coordinate conditional writers more closely, with different placement and failure assumptions. Token waits can expire, unconditioned writers do not participate, and separate clusters do not share a token grant.

The active modes and their release-specific definitions are available in the settings reference:

{{< configuration-reference-table >}}
^conditional_put_mode$
^token_request_mode$
{{< /configuration-reference-table >}}

## Latch objects

A latch is an application-chosen object used to coordinate a larger activity. For example, workers can conditionally create a marker before claiming a batch. The marker does not atomically include the batch's other writes, and a worker can fail after creating it.

The application therefore needs an ownership, expiry or recovery rule and must handle uncertain outcomes. A latch should not be treated as a distributed lock with stronger guarantees than the conditional request itself.

## Conflicts remain possible

Preserve causal context, handle failed preconditions, and retain a conflict strategy. Ordinary concurrent writes, partitions, maintenance, or active/active multi-cluster traffic can invalidate assumptions made from a successful condition check.
