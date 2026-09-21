---
title: Fetch object messages
description: Fetch returns the stored content and causal context, or an error for a missing or unavailable value.
  Multiple content entries represent siblings. Preserve the returned vector clock for a later update; a conditional
  uncha
weight: 600
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\fetch-object.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/fetch-object.md
related:
- how-to/application-data/read-an-object-and-handle-missing-values
- reference/data-model-contracts/causal-context-and-version-vector-representations
- reference/http-api/object-request-options
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Fetch returns the stored content and causal context, or an error for a missing or unavailable value. Multiple content entries represent siblings. Preserve the returned vector clock for a later update; a conditional unchanged response may omit the value.

## Message contract

{{< protocol-message name="RpbGetReq" >}}

{{< protocol-message name="RpbGetResp" >}}

{{< protocol-message name="RpbContent" >}}

{{< protocol-message name="RpbLink" >}}

{{< protocol-message name="RpbPair" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
