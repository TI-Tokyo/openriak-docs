---
title: Object metadata
description: Object metadata accompanies each content value. On updates, the application must preserve or replace
  the metadata it intends to retain.
weight: 360
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
- https://openriak.github.io/riak/ObjectAPI.html#object-meta-content---the-request-and-response-headers
- https://openriak.github.io/riak/ObjectAPI.html#object-metadata
- https://openriak.github.io/riak/ObjectAPI.html#user-metadata
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/data/object-metadata.md
related:
- how-to/application-data/update-an-object-with-causal-context
- how-to/indexes-and-queries/add-and-query-secondary-indexes
- reference/data-model-contracts/media-types-and-content-encodings
- reference/data-model-contracts/causal-context-and-version-vector-representations
- reference/data-model-contracts/secondary-index-terms-and-projected-attributes
- foundations/data-and-consistency/objects-keys-and-buckets
---

Object metadata accompanies each content value. On updates, the application must preserve or replace the metadata it intends to retain.

## HTTP fields

- `Content-Type` and `Content-Encoding`: representation metadata for the stored bytes.
- `X-Riak-Meta-NAME`: application user metadata.
- `X-Riak-Index-NAME`: secondary-index terms associated with the object.
- `X-Riak-Vclock`: causal context for the object state, returned on reads and supplied on context-preserving writes.
- `ETag` and `Last-Modified`: representation validators and modification metadata; they are not a replacement for the causal-context contract.

Repeated content entries can carry different metadata when siblings exist. A write that changes a JSON field does not automatically change its index term.

## Protocol Buffers representation

{{< protocol-message name="RpbContent" >}}
{{< protocol-message name="RpbPair" >}}

Link metadata is a historical interface; new data discovery should use explicit application references or indexes.
