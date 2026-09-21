---
title: Conditional requests and latch objects
description: Conditional PUTs test absence or an observed object version before accepting a change. Their coordination
  is cluster-local and does not provide a formal cross-object or cross-cluster transaction guarantee.
weight: 450
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#conditional-requests
- https://openriak.github.io/riak/ObjectAPI.html#conditional-requests-and-latch-objects
- https://openriak.github.io/riak/ObjectAPI.html#use-of-request-header---if-none-match
- https://openriak.github.io/riak/ObjectAPI.html#use-of-request-header---x-riak-if-not-modified-non-standard-riak-header
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/conditional-requests.md
related:
- how-to/application-data/make-conditional-reads-and-writes
- how-to/application-data/coordinate-an-update-with-a-latch-object
- tutorials/data-and-concurrency/practise-conditional-updates
- reference/data-model-contracts/causal-context-and-version-vector-representations
- foundations/data-and-consistency/conditional-updates-and-latch-objects
---

Conditional PUTs test absence or an observed object version before accepting a change. Their coordination is cluster-local and does not provide a formal cross-object or cross-cluster transaction guarantee.

## Supported write headers

`If-None-Match` on PUT requests creation only if no object is present. This interface treats a supplied header as the wildcard absence check; use `*` explicitly.

`X-Riak-If-Not-Modified` carries the encoded vector clock obtained by a prior read. It conditions the PUT on that object state. This is the Riak-specific version check; standard `If-Match` and `If-Unmodified-Since` do not provide the same token-protected behaviour.

A rejected condition returns `412 Precondition Failed`. The caller must preserve its intended work and decide whether to refetch, merge, or abandon it.

## Coordination settings

{{< configuration-reference-table >}}
^(conditional_put_mode|token_request_mode)$
{{< /configuration-reference-table >}}

Token modes reduce races, but timeout fallback, failure patterns, and ownership changes can weaken serialization. Unconditional writes do not participate in this protection. Concurrent writes in separate clusters do not coordinate tokens with one another. Applications still need a conflict policy.

## Latch objects

A latch is an application-defined coordination object updated with these conditions. Its owner, expiry, and recovery rules belong to the application. A successful latch update does not atomically lock unrelated objects, and an expired owner can still have work in flight. See [Conditional updates and latch objects]({{< product-version-root >}}foundations/data-and-consistency/conditional-updates-and-latch-objects/) before using a latch to coordinate a workflow.
