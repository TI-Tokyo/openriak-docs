---
title: Resource discovery
description: The root HTTP resource can advertise available API resources. Discovery reflects the addressed listener
  and release; it is not a guarantee that every advertised operation is enabled for the caller.
weight: 530
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
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\list-resources.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/list-resources.md
related:
- reference/http-api/http-conventions-authentication-and-errors
- reference/http-api/ping
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

The root HTTP resource can advertise available API resources. Discovery reflects the addressed listener and release; it is not a guarantee that every advertised operation is enabled for the caller.

## Request

`GET /` with `Accept: application/json` requests a machine-readable resource listing. A browser-oriented response may be selected with an HTML accept header.

## Use and limits

Use the returned resource links where the client supports discovery, preserving any proxy base path. Treat authentication, backend capability, deprecated features, and operation-specific permissions separately. Prefer the versioned endpoint contracts for applications that require a stable documented interface.
