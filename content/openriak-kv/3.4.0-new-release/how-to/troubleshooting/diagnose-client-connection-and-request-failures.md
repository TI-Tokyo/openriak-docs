---
title: Diagnose client connection and request failures
description: Separate a client connectivity problem from an authentication, protocol, or application-request failure.
weight: 1290
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
- how-to/troubleshoot/client-errors.md
related:
- reference/http-api/http-conventions-authentication-and-errors
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- how-to/node-configuration/configure-http-and-protocol-buffers-listeners
- how-to/security/authenticate-an-application-client
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Separate a client connectivity problem from an authentication, protocol, or application-request failure.

## Reproduce at the endpoint

Record the exact host, port, protocol, TLS settings, namespace, method, and response. Compare a direct request with the load-balanced path where allowed.

## Check connection stages

Verify name resolution, routing, listener binding, and firewall access. For TLS, check the peer name and certificate chain before checking application credentials.

## Check the request

Confirm the bucket type and content encoding, client timeout, and supported operation. Compare the request with the HTTP or Protocol Buffers reference.

## Verify both outcomes

Repeat the intended successful operation and a deliberately invalid or denied request. Ensure client retries distinguish uncertain writes from operations that never reached the server.
