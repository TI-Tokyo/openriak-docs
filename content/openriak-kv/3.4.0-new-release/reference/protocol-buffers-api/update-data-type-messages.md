---
title: Update data-type messages
description: Update applies data-type operations rather than replacing an ordinary object body. Supply context for
  observed removals. The response may be empty unless a key was assigned or a returned body was requested. Retrying
  non-
weight: 660
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\dt-store.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/store-data-type.md
related:
- reference/protocol-buffers-api/fetch-data-type-messages
- reference/protocol-buffers-api/counter-operations
- reference/protocol-buffers-api/set-operations
- reference/protocol-buffers-api/map-operations
- reference/protocol-buffers-api/grow-only-and-union-operations
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Update applies data-type operations rather than replacing an ordinary object body. Supply context for observed removals. The response may be empty unless a key was assigned or a returned body was requested. Retrying non-idempotent operations after an uncertain timeout can apply them again.

## Message contract

{{< protocol-message name="DtUpdateReq" >}}

{{< protocol-message name="DtUpdateResp" >}}

{{< protocol-message name="DtOp" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
