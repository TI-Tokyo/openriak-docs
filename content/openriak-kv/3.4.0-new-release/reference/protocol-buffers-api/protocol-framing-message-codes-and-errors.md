---
title: Protocol framing, message codes, and errors
description: Protocol Buffers requests use a four-byte unsigned big-endian length, followed by a one-byte message
  code and the encoded message body. The length includes the code byte but excludes the four-byte prefix.
weight: 580
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
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\apis-and-clients\APIs\protocol_buffers\protocol-buffers.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/_index.md
related:
- reference/protocol-buffers-api/authentication-messages
- reference/protocol-buffers-api/fetch-object-messages
- reference/protocol-buffers-api/store-object-messages
- reference/protocol-buffers-api/fetch-data-type-messages
- reference/protocol-buffers-api/secondary-index-query-messages
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Protocol Buffers requests use a four-byte unsigned big-endian length, followed by a one-byte message code and the encoded message body. The length includes the code byte but excludes the four-byte prefix.

## Framing

Read the complete length-delimited frame before decoding it. A TCP read can return part of a frame or several frames together. Bodyless messages still carry their length and message code. Streaming operations can produce multiple response frames; use their completion marker rather than closing after the first packet.

For example, the ping request is the five bytes `00 00 00 01 01`: length one, followed by request code one.

## Errors

{{< protocol-message name="RpbErrorResp" >}}

An error response may replace the expected success message. Preserve the server message and request context, distinguish authentication and validation failures from retryable availability failures, and handle uncertain write outcomes explicitly.

## Message codes

{{< configuration-reference-table reference="pb-codes" >}}{{< /configuration-reference-table >}}

## Authentication and values

Use [Authentication messages]({{< product-version-root >}}reference/protocol-buffers-api/authentication-messages/) before ordinary requests when security is enabled. Integers, booleans, repeated fields, and nested messages follow their Protocol Buffers wire types; binary keys, values, context, and continuation tokens must remain byte-preserving. Do not infer text encoding from the field name.
