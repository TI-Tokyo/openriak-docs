---
title: Coverage-plan messages
description: A coverage request returns endpoints and opaque coverage contexts for partitioned extraction. A client
  must preserve each context and handle unavailable endpoints and replacement coverage; this is not a list of independe
weight: 720
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\coverage-queries.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/coverage-queries.md
related:
- reference/protocol-buffers-api/secondary-index-query-messages
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

A coverage request returns endpoints and opaque coverage contexts for partitioned extraction. A client must preserve each context and handle unavailable endpoints and replacement coverage; this is not a list of independent full-database query endpoints.

## Message contract

{{< protocol-message name="RpbCoverageReq" >}}

{{< protocol-message name="RpbCoverageResp" >}}

{{< protocol-message name="RpbCoverageEntry" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
