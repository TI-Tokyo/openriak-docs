---
title: Legacy listing messages
description: 'Legacy listing can scan substantial portions of the database and return large results. Streaming responses
  are complete only when their terminal marker arrives. Prefer bounded indexes or AAE inventory when they meet the '
weight: 740
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\list-buckets.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/list-buckets.md
- reference/protocol-buffers/list-keys.md
related:
- how-to/data-inspection-and-repair/inventory-buckets-using-aae-folds
- reference/http-api/legacy-bucket-and-key-listing
- reference/protocol-buffers-api/secondary-index-query-messages
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Legacy listing can scan substantial portions of the database and return large results. Streaming responses are complete only when their terminal marker arrives. Prefer bounded indexes or AAE inventory when they meet the requirement.

## Message contract

{{< protocol-message name="RpbListBucketsReq" >}}

{{< protocol-message name="RpbListBucketsResp" >}}

{{< protocol-message name="RpbListKeysReq" >}}

{{< protocol-message name="RpbListKeysResp" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
