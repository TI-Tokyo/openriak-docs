---
title: Media types and content encodings
description: Object values are byte sequences. HTTP `Content-Type` describes the representation; `Content-Encoding`
  describes a transformation applied to those bytes.
weight: 350
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
- reference/data/content-types.md
related:
- how-to/application-data/store-and-retrieve-different-content-types
- reference/data-model-contracts/object-metadata
- reference/http-api/fetch-object
- foundations/data-and-consistency/objects-keys-and-buckets
---

Object values are byte sequences. HTTP `Content-Type` describes the representation; `Content-Encoding` describes a transformation applied to those bytes.

## Media types

Use an explicit media type such as `application/json`, `text/plain`, or `application/octet-stream`. The database does not infer a schema or maintain indexes from a JSON document's fields merely because the content type is JSON. Clients must agree on serialization and character encoding.

## Encodings

Only declare a content encoding when the stored body actually uses it. Preserve binary bytes when uploading and downloading files. Application-level compression and backend storage compression are separate; backend compression does not require clients to decompress the value they fetch.

## Siblings

A multipart sibling response can contain different metadata and media types for each version. Decode each part according to its own headers before applying an application merge rule. The resolved object must carry its intended representation metadata.
