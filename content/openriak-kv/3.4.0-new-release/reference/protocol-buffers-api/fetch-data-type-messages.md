---
title: Fetch data-type messages
description: Fetch a distributed data type from an active type-specific namespace. The returned value union is selected
  by its datatype, and context is opaque. Keep that context when a later operation removes observed state.
weight: 650
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\dt-fetch.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/fetch-data-type.md
related:
- how-to/application-data/update-distributed-counters
- how-to/application-data/add-and-remove-members-of-distributed-sets
- how-to/application-data/update-distributed-maps
- reference/data-model-contracts/distributed-data-type-contracts
- reference/protocol-buffers-api/update-data-type-messages
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Fetch a distributed data type from an active type-specific namespace. The returned value union is selected by its datatype, and context is opaque. Keep that context when a later operation removes observed state.

## Message contract

{{< protocol-message name="DtFetchReq" >}}

{{< protocol-message name="DtFetchResp" >}}

{{< protocol-message name="DtValue" >}}

{{< protocol-message name="MapEntry" >}}

{{< protocol-message name="MapField" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
