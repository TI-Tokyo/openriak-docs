---
title: Bucket-type messages
description: Bucket-type messages inspect or update an existing type. The server uses the bucket-property response/acknowledgement
  messages for these operations. Creating and activating a type are administrative operations; these mes
weight: 640
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\get-bucket-type.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/get-bucket-type.md
- reference/protocol-buffers/set-bucket-type.md
related:
- how-to/application-data/create-and-activate-bucket-types
- reference/configuration/bucket-properties-and-defaults
- reference/protocol-buffers-api/bucket-property-messages
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Bucket-type messages inspect or update an existing type. The server uses the bucket-property response/acknowledgement messages for these operations. Creating and activating a type are administrative operations; these messages do not replace that lifecycle.

## Message contract

{{< protocol-message name="RpbGetBucketTypeReq" >}}

{{< protocol-message name="RpbSetBucketTypeReq" >}}

{{< protocol-message name="RpbGetBucketResp" >}}

{{< protocol-message name="RpbSetBucketResp" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
