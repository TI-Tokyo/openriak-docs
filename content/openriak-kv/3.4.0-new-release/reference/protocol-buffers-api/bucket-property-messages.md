---
title: Bucket property messages
description: Bucket-property messages read, override, or reset bucket properties. Reset removes bucket-level overrides;
  it is not an object deletion operation. The `type` field selects the namespace, while `bucket` identifies the
  buc
weight: 630
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\get-bucket-props.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/get-bucket-properties.md
- reference/protocol-buffers/set-bucket-properties.md
- reference/protocol-buffers/reset-bucket-properties.md
related:
- reference/configuration/bucket-properties-and-defaults
- reference/data-model-contracts/buckets-and-bucket-types
- reference/protocol-buffers-api/bucket-type-messages
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Bucket-property messages read, override, or reset bucket properties. Reset removes bucket-level overrides; it is not an object deletion operation. The `type` field selects the namespace, while `bucket` identifies the bucket within it.

## Message contract

{{< protocol-message name="RpbGetBucketReq" >}}

{{< protocol-message name="RpbGetBucketResp" >}}

{{< protocol-message name="RpbSetBucketReq" >}}

{{< protocol-message name="RpbSetBucketResp" >}}

{{< protocol-message name="RpbResetBucketReq" >}}

{{< protocol-message name="RpbResetBucketResp" >}}

{{< protocol-message name="RpbBucketProps" >}}

{{< protocol-message name="RpbCommitHook" >}}

{{< protocol-message name="RpbModFun" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
