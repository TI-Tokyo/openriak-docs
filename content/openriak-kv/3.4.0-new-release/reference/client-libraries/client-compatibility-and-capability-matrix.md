---
title: Client compatibility and capability matrix
description: Client compatibility depends on protocol support, server features, authentication, and the language
  runtime. A client that can read ordinary objects does not necessarily support data types, current queries, or
  every secu
weight: 1120
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\client-libraries.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/client-libraries/_index.md
related:
- reference/http-api/http-conventions-authentication-and-errors
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- reference/protocol-buffers-api/authentication-messages
- reference/query-api/endpoints-and-request-schema
- tutorials/first-application/build-a-small-application-with-csharp
- tutorials/first-application/build-a-small-application-with-python
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Client compatibility depends on protocol support, server features, authentication, and the language runtime. A client that can read ordinary objects does not necessarily support data types, current queries, or every security mode.

## Protocol capabilities

HTTP clients can use the documented Object, datatype, index, Query, and AAE endpoints when the server and policy permit them. PB clients must implement the corresponding message codes and security handshake. Current Query API expressions use their own HTTP contract rather than the legacy PB index request.

## Acceptance checks

For a selected library or runtime, verify causal-context preservation, sibling handling, typed buckets, binary values, streaming/continuations, timeout behaviour, and TLS hostname verification. Record the exact client version and OTP/server combination. Do not infer compatibility from an old library's language name alone.

## Language examples

The language pages in this section describe the small HTTP application examples and their runtime prerequisites. They do not claim that every historical third-party Riak library has been verified with this release.
