---
title: Causality, version vectors, and siblings
description: Causal context records which object history a write has observed. OpenRiak uses version information
  to distinguish a later update from an update made independently of another writer.
weight: 120
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\causal-context.md
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-22'
review-by: TI Tokyo/JOM
review_scope: editorial & technical
restructured_from:
- foundations/data-model/causal-context.md
- foundations/data-model/version-vectors-and-siblings.md
related:
- foundations/data-and-consistency/resolving-concurrent-updates
- how-to/application-data/update-an-object-with-causal-context
- how-to/application-data/resolve-concurrent-object-updates
- reference/data-model-contracts/causal-context-and-version-vector-representations
---

Causal context records which object history a write has observed. OpenRiak uses version information to distinguish a later update from an update made independently of another writer.

## Read, modify, and preserve context

A client reads an object and receives its context. Returning that context with the next write lets the database relate the new value to the versions the client saw. Treat the encoded context as opaque; copying a timestamp or an ETag into its place is not equivalent.

## Concurrent writes

Suppose two clients read the same profile and each makes a different edit. Neither write has observed the other. With sibling-preserving policy, both contents can survive as siblings. They share one object identity; they are not two independently keyed records.

Resolving siblings means applying an merge rule at the application level and writing the combined value with the context covering the versions being resolved. A fresh concurrent update can still arrive while that happens.

## Missing context

A blind overwrite discards information needed to distinguish an intentional replacement from an independent update. The consequences depend on bucket policy, but the client should not assume it has safely superseded all earlier work.

Version metadata is also used by repair to compare replicas. Matching wall-clock timestamps alone cannot establish the same causal relationship.
