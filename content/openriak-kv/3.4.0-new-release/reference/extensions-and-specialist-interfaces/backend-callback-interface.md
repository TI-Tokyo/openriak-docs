---
title: Backend callback interface
description: A storage backend implements the callback contract used by the KV vnode. Capability declarations determine
  which optional query, fold, and maintenance paths the vnode may use.
weight: 1220
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- backend-developers
source_material:
- legacy-3.2.5
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\backend.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/specialized-apis/backend-api.md
related:
- reference/orientation-and-compatibility/backend-capability-matrix
- how-to/installation/build-and-install-from-source
- foundations/storage-and-performance/storage-backend-trade-offs
---

A storage backend implements the callback contract used by the KV vnode. Capability declarations determine which optional query, fold, and maintenance paths the vnode may use.

## Core responsibilities

The backend starts and stops partition-local state, reads and writes object representations, deletes keys, folds over keys or objects, reports status and size where supported, and handles backend-specific commands. Return forms and state threading must match the release's behaviour module.

## Capability contract

Capabilities such as indexes, asynchronous folds, native AAE heads, hot backup, and complex queries must correspond to implemented semantics. Advertising a capability without its required behaviour can cause incorrect query or recovery results. See [Backend capability matrix]({{< product-version-root >}}reference/orientation-and-compatibility/backend-capability-matrix/) for the built-in backends.

## Callback signatures

The following signatures and types come from the matching release's behaviour definition. `state()` is private backend state. Preserve the updated state returned by each operation. Callbacks listed as optional need only be implemented when their corresponding capabilities are supported.

{{< backend-contract >}}

## Versioned definitions

The definitive callbacks are in the release's `riak_kv_backend` behaviour and built-in backend modules. Compile and test against the exact pinned release source, including missing keys, concurrent access, fold cancellation, restart recovery, handoff, and corrupted data. An older backend plugin is not automatically compatible with a new callback or object format.
