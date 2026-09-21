---
title: Java client
description: The Java client example uses the HTTP API through the language's HTTP library. It does not depend on
  a Riak-specific Protocol Buffers client.
weight: 1160
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/client-libraries/java.md
related:
- tutorials/first-application/build-a-small-application-with-java
- reference/client-libraries/client-compatibility-and-capability-matrix
- reference/http-api/http-conventions-authentication-and-errors
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

The Java client example uses the HTTP API through the language's HTTP library. It does not depend on a Riak-specific Protocol Buffers client.

## Transport and runtime

The accompanying example targets **JDK 17 or newer** and uses [this HTTP client interface](https://docs.oracle.com/en/java/javase/17/docs/api/java.net.http/java/net/http/HttpClient.html). Object addressing, headers, and response statuses follow the shared HTTP reference.

## Operation mapping

Use PUT or POST to store objects, GET to fetch them, DELETE to delete them, and the secondary-index endpoint to discover keys. Preserve `X-Riak-Vclock` on updates, retain the intended index metadata, and distinguish an empty successful response from an error.

For distributed data types and the Query API, use their documented request bodies and endpoints. A successful object CRUD test does not establish support for those additional contracts.

## Authentication and error handling

Configure certificate verification, credentials, timeouts, and connection reuse using the selected library. Production code must handle sibling responses, failed preconditions, missing objects, and uncertain write outcomes explicitly.

## Protocol Buffers alternatives

A dedicated Riak client may provide Protocol Buffers support and convenience APIs. Verify its exact package, runtime, authentication, data-type, and release compatibility before substituting it; no untested third-party client version is implied by the HTTP example.
