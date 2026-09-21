---
title: Configure a load-balancing proxy
description: Put a proxy in front of client listeners when applications need a stable endpoint or coordinated connection
  draining. Keep Erlang distribution and administrative commands on their own network path.
weight: 260
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\load-balancing-proxy.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\load-balancing.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#load-balancing
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/load-balancing-proxy.md
related:
- how-to/node-configuration/configure-http-and-protocol-buffers-listeners
- how-to/cluster-lifecycle/perform-a-rolling-restart
- how-to/troubleshooting/diagnose-client-connection-and-request-failures
- reference/http-api/http-conventions-authentication-and-errors
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/cluster-architecture/the-lifecycle-of-a-read-and-a-write
---

Put a proxy in front of client listeners when applications need a stable endpoint or coordinated connection draining. Keep Erlang distribution and administrative commands on their own network path.

## Choose the proxy mode

Use HTTP-aware proxying for the HTTP API, or TCP proxying for Protocol Buffers. Configure TLS termination or passthrough according to where authentication and certificate validation occur. Forward authorization, causal-context, conditional-request, and content-type headers unchanged.

## Configure upstreams

Add the intended client listeners as upstreams. Use `/ping` for a basic HTTP liveness check, and supplement it with cluster monitoring; liveness does not prove healthy replicas or an acceptable workload. Choose connection and response timeouts long enough for the application's supported operations, with explicit limits for long-running queries.

Do not enable automatic retries of non-idempotent writes merely because an upstream timed out. The write may already have succeeded. Preserve streaming responses and avoid buffering an unbounded listing or query into proxy memory.

## Verify the real client path

Through the proxy, test an authenticated read, a write with causal context, a conditional failure, a missing key, and the largest expected response. Test PB connections separately if used. Confirm that a failed upstream is removed and that healthy members still serve requests.

## Drain for maintenance

Remove one node from the proxy's active upstreams, allow existing connections to finish, and perform the node maintenance. Return it only after process, membership, and application checks pass. Keep enough healthy upstream capacity for the remaining workload.
