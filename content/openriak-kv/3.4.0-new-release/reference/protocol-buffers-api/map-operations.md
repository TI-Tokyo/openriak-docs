---
title: Map operations
description: Map operations address typed fields. Each update selects the matching field datatype and operation;
  removals act on observed state using the enclosing context. Maps may contain nested maps, counters, sets, registers,
  and
weight: 690
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\dt-map-store.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/update-map.md
related:
- how-to/application-data/update-distributed-maps
- reference/protocol-buffers-api/update-data-type-messages
- reference/data-model-contracts/distributed-data-type-contracts
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/conflict-free-replicated-data-types
---

Map operations address typed fields. Each update selects the matching field datatype and operation; removals act on observed state using the enclosing context. Maps may contain nested maps, counters, sets, registers, and flags as defined below.

## Message contract

{{< protocol-message name="MapOp" >}}

{{< protocol-message name="MapUpdate" >}}

{{< protocol-message name="MapField" >}}

{{< protocol-message name="MapEntry" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
