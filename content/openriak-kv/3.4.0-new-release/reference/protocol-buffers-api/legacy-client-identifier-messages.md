---
title: Legacy client identifier messages
description: Legacy client-identifier messages get or set a connection-associated client ID. They are not authentication
  messages and do not replace the causal context returned by object reads. New clients should follow the object
  an
weight: 750
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\get-client-id.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\set-client-id.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/client-id.md
related:
- reference/data-model-contracts/causal-context-and-version-vector-representations
- reference/protocol-buffers-api/authentication-messages
- reference/protocol-buffers-api/fetch-object-messages
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Legacy client-identifier messages get or set a connection-associated client ID. They are not authentication messages and do not replace the causal context returned by object reads. New clients should follow the object and data-type context contracts.

## Message contract

{{< protocol-message name="RpbGetClientIdReq" >}}

{{< protocol-message name="RpbGetClientIdResp" >}}

{{< protocol-message name="RpbSetClientIdReq" >}}

{{< protocol-message name="RpbSetClientIdResp" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
