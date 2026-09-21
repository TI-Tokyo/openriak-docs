---
title: Internal fetch and membership API
description: The internal replication API exposes membership discovery, source-queue consumption, and requests to
  queue object references. It is release-sensitive and is not a general durable messaging API.
weight: 980
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#the-fetch-api
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/specialized-apis/fetch-api.md
related:
- reference/replication-interfaces/replication-references-and-queue-payloads
- reference/replication-interfaces/next-generation-replication-runtime-controls
- how-to/replication-and-reconciliation/secure-next-generation-replication-connections
- reference/protocol-buffers-api/protocol-framing-message-codes-and-errors
- foundations/replication-and-repair/replication-sources-queues-and-sinks
---

The internal replication API exposes membership discovery, source-queue consumption, and requests to queue object references. It is release-sensitive and is not a general durable messaging API.

## HTTP resources

`GET /membership_request` returns listener addresses and ports for cluster members.

`GET /queuename/QUEUE` consumes the next queue item. `object_format` selects the supported internal object representation, including the AAE-hash variant where supported.

`POST /queuename/QUEUE` submits key/clock references to be queued for later consumption.

## Protocol Buffers contract

{{< protocol-message name="RpbMembershipReq" >}}
{{< protocol-message name="RpbMembershipResp" >}}
{{< protocol-message name="RpbClusterMemberEntry" >}}
{{< protocol-message name="RpbFetchReq" >}}
{{< protocol-message name="RpbFetchResp" >}}
{{< protocol-message name="RpbPushReq" >}}
{{< protocol-message name="RpbPushResp" >}}

## Constraints

Protect source access and use PB for the documented secured replication transport. A consumed queue item and a destination-confirmed object are different stages. Recovery from lost references relies on reconciliation or explicit re-seeding.
