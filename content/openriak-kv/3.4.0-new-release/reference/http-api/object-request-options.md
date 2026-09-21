---
title: Object request options
description: Object requests can override selected bucket policies for one operation. Prefer a stable bucket-type
  policy when the requirement applies to every request.
weight: 460
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#get-and-put-options
tags:
- diataxis
- kv
- reference
- quickdocs
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/object-request-options.md
related:
- how-to/planning-a-deployment/choose-replication-and-acknowledgement-policies
- reference/configuration/bucket-properties-and-defaults
- reference/protocol-buffers-api/fetch-object-messages
- reference/protocol-buffers-api/store-object-messages
- reference/protocol-buffers-api/delete-object-messages
- foundations/data-and-consistency/quorums-availability-and-durability
---

Object requests can override selected bucket policies for one operation. Prefer a stable bucket-type policy when the requirement applies to every request.

## Policy-backed options

Read acknowledgement uses `r` and `pr`; write acknowledgement uses `w`, `pw`, and `dw`. `node_confirms` adds a distinct-physical-node requirement. `notfound_ok`, `basic_quorum`, `sloppy_quorum`, and durability controls affect their respective request paths. The exact property types and defaults are loaded here:

{{< configuration-reference-table >}}
^(buckets\.)?(default\.)?(n_val|r|pr|w|pw|dw|rw|node_confirms|notfound_ok|basic_quorum|sloppy_quorum|sync_on_write)$
{{< /configuration-reference-table >}}

## HTTP-specific options

- `vtag`: fetch a selected sibling representation.
- `returnbody`: request the resulting content from a store operation.
- `deletedvclock`: request retained deletion context on a missing-object response.
- `timeout`: server operation timeout in milliseconds, where supported by the endpoint.

Wire names differ from some internal or PB field names. The PB request pages give their exact fields. A timeout limits waiting; it does not make a write atomic or prove that no replica accepted it.
