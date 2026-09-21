---
title: Keys and object representations
description: An ordinary object is identified by bucket type, bucket, and key. Its value is an opaque byte sequence
  accompanied by content metadata and causal context.
weight: 330
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
- https://openriak.github.io/riak/ObjectAPI.html#object-identifier---the-url
- https://openriak.github.io/riak/ObjectAPI.html#object-value---the-request-body
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/data/keys-and-objects.md
related:
- reference/data-model-contracts/buckets-and-bucket-types
- reference/data-model-contracts/media-types-and-content-encodings
- reference/data-model-contracts/object-metadata
- reference/data-model-contracts/causal-context-and-version-vector-representations
- how-to/application-data/create-and-store-an-object
- foundations/data-and-consistency/objects-keys-and-buckets
---

An ordinary object is identified by bucket type, bucket, and key. Its value is an opaque byte sequence accompanied by content metadata and causal context.

## HTTP addresses

- Typed object: `/types/TYPE/buckets/BUCKET/keys/KEY`.
- Untyped object: `/buckets/BUCKET/keys/KEY`.
- Data-type value: `/types/TYPE/buckets/BUCKET/datatypes/KEY`.

Percent-encode each path component separately. The same bucket/key under different types identifies different data. A bucket is a namespace, not a filesystem directory.

## Values and versions

The request body carries the value; content type describes its interpretation to clients. Multiple concurrent versions can appear as siblings. Preserve the returned context when updating or deleting an observed version. Key generation by the server is available through a POST to the key collection; a client-selected key uses PUT to the full object address.
