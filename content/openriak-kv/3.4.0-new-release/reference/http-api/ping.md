---
title: Ping
description: '`GET /ping` checks whether the HTTP API responds.'
weight: 510
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\ping.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/ping.md
related:
- how-to/installation/verify-an-installation
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- reference/protocol-buffers-api/ping-and-server-information-messages
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

`GET /ping` checks whether the HTTP API responds.

## Response

A healthy endpoint returns `200 OK` with the body `OK`. Failure to connect, TLS failure, authentication policy, or a server error must be handled separately from that success body.

## Limits

Ping is a liveness check. It does not inspect replica completeness, membership, ownership transfers, or application latency. Use an authenticated application probe and cluster monitoring for readiness.
