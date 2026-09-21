---
title: MapReduce messages
description: The MapReduce transport carries an encoded job and streams phase responses. A final response with `done`
  marks completion and may contain no phase payload. MapReduce is deprecated; its presence in the wire schema does
  no
weight: 760
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\mapreduce.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/mapreduce.md
related:
- how-to/legacy-and-specialist-workflows/configure-and-run-a-mapreduce-job
- reference/legacy-and-experimental-features/mapreduce-jobs-and-functions
- reference/http-api/http-mapreduce-transport
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

The MapReduce transport carries an encoded job and streams phase responses. A final response with `done` marks completion and may contain no phase payload. MapReduce is deprecated; its presence in the wire schema does not imply support for every historical execution engine.

## Message contract

{{< protocol-message name="RpbMapRedReq" >}}

{{< protocol-message name="RpbMapRedResp" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
