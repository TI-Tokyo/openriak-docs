---
title: Diagnose unexpected API responses
description: Interpret the response before retrying or changing data. An unexpected status can be correct for the
  request that was sent.
weight: 1300
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- developers
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/troubleshoot/api-errors.md
- how-to/troubleshoot/http-204.md
related:
- reference/http-api/fetch-object
- reference/http-api/store-object
- reference/http-api/delete-object
- reference/http-api/conditional-requests-and-latch-objects
- reference/http-api/object-request-options
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Interpret the response before retrying or changing data. An unexpected status can be correct for the request that was sent.

## Save the exchange

Capture the method, URL, headers, request body, status, response headers, and response body. Remove secrets from shared copies.

## Check the contract

Compare with the operation reference. HTTP 204 means successful completion without a response body; an object PUT need not return the stored value unless the supported return-body option requests it.

## Check namespace and conditions

Verify bucket type, key encoding, causal context, and conditional headers. A precondition failure, a missing object, and a timeout require different application handling.

## Verify the object independently

Fetch the intended object after a successful write and compare its content and metadata. Do not convert every empty body into an application failure or blindly repeat a write.
