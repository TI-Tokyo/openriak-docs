---
title: Ping and server information messages
description: Ping checks basic protocol responsiveness. Server information returns the node and release strings;
  neither response alone proves healthy membership, complete replicas, or acceptable request latency.
weight: 730
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\ping.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/protocol-buffers/ping.md
- reference/protocol-buffers/server-information.md
related:
- how-to/installation/verify-an-installation
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- reference/http-api/ping
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Ping checks basic protocol responsiveness. Server information returns the node and release strings; neither response alone proves healthy membership, complete replicas, or acceptable request latency.

## Message contract

{{< protocol-message name="RpbPingReq" >}}

{{< protocol-message name="RpbPingResp" >}}

{{< protocol-message name="RpbGetServerInfoReq" >}}

{{< protocol-message name="RpbGetServerInfoResp" >}}

## Framing and failures

All messages use the framing and error response in [Protocol framing, message codes, and errors]({{< product-version-root >}}reference/protocol-buffers-api/protocol-framing-message-codes-and-errors/). Field cardinality and explicitly declared schema defaults are shown above; omitted request options can also be resolved by bucket policy or the server. A `bytes` value is not automatically UTF-8 text.
