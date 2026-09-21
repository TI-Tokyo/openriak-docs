---
title: Delete object messages
description: 'Delete applies deletion to the identified object. Include the observed vector clock when deleting
  a known version. The successful response has no body; tombstone retention and later reclamation are separate from
  request '
weight: 620
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\delete-object.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/delete-object.md
related:
- how-to/application-data/delete-an-object
- reference/data-model-contracts/deletion-tombstone-and-expiration-states
- reference/http-api/object-request-options
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Delete applies deletion to the identified object. Include the observed vector clock when deleting a known version. The successful response has no body; tombstone retention and later reclamation are separate from request completion.

## Message contract

{{< protocol-message name="RpbDelReq" >}}

{{< protocol-message name="RpbDelResp" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
