---
title: Store object messages
description: Store writes an object value and metadata. Supply the previously fetched vector clock for an update.
  A missing key requests server assignment; `return_body` controls whether the response includes the stored representatio
weight: 610
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\store-object.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/store-object.md
related:
- how-to/application-data/create-and-store-an-object
- how-to/application-data/update-an-object-with-causal-context
- reference/http-api/object-request-options
- reference/http-api/conditional-requests-and-latch-objects
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Store writes an object value and metadata. Supply the previously fetched vector clock for an update. A missing key requests server assignment; `return_body` controls whether the response includes the stored representation. Timeout does not prove that a write had no effect.

## Message contract

{{< protocol-message name="RpbPutReq" >}}

{{< protocol-message name="RpbPutResp" >}}

{{< protocol-message name="RpbContent" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
