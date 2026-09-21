---
title: Experimental strong-consistency interface
description: The ensemble-backed strong-consistency interface is experimental and deprecated in this release family.
  It has a separate availability and feature model from ordinary eventually consistent objects.
weight: 1350
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\app-guide\strong-consistency.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\strong-consistency.md
source_material:
- legacy-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#strong-consistency-api
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/specialized-apis/strong-consistency-api.md
- foundations/consistency/strong-consistency.md
related:
- how-to/legacy-and-specialist-workflows/evaluate-experimental-strong-consistency
- reference/orientation-and-compatibility/feature-status-and-deprecations
- reference/http-api/conditional-requests-and-latch-objects
- foundations/data-and-consistency/conditional-updates-and-latch-objects
---

The ensemble-backed strong-consistency interface is experimental and deprecated in this release family. It has a separate availability and feature model from ordinary eventually consistent objects.

## Configuration and namespace

Use a dedicated consistent bucket type and the release's strong-consistency configuration. The replica policy determines the ensemble's majority requirement; loss of sufficient peers makes operations unavailable rather than allowing ordinary fallback writes.

{{< configuration-reference-table >}}
^strong_consistency
{{< /configuration-reference-table >}}

## Client contract

Use a client and operation supported by the interface. Do not assume ordinary siblings, secondary indexes, CRDT updates, MapReduce, or inter-cluster replication have equivalent support. Conditional operations and returned context must follow the consistent-object interface rather than an ordinary object's merge policy.

## Status

{{< cli-example key="shell:riak admin ensemble-status" >}}

Inspect the intended ensemble and peers, not just general node liveness. Rehearse majority loss and recovery in isolation before relying on any observed behaviour. Token-protected ordinary PUTs reduce races but do not provide the same formal semantics.
