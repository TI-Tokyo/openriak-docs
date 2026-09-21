---
title: Configure and run a MapReduce job
description: Run an existing MapReduce job with explicit inputs and bounded output. MapReduce is deprecated; prefer
  direct keys, secondary indexes, or the Query API for new workloads where they meet the requirement.
weight: 1440
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\mapreduce.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/mapreduce.md
- how-to/develop/run-mapreduce.md
related:
- reference/legacy-and-experimental-features/mapreduce-jobs-and-functions
- reference/http-api/http-mapreduce-transport
- reference/protocol-buffers-api/mapreduce-messages
- how-to/indexes-and-queries/run-exact-and-range-queries-with-the-query-api
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Run an existing MapReduce job with explicit inputs and bounded output. MapReduce is deprecated; prefer direct keys, secondary indexes, or the Query API for new workloads where they meet the requirement.

## Prepare a small job

Use the request contract in [MapReduce jobs and functions]({{< product-version-root >}}reference/legacy-and-experimental-features/mapreduce-jobs-and-functions/). Start with a short explicit list of bucket/key inputs instead of a full bucket scan. Verify every referenced Erlang or JavaScript function is available and permitted on all nodes that may execute it.

## Submit and observe

Send the job using the HTTP transport in [HTTP MapReduce transport]({{< product-version-root >}}reference/http-api/http-mapreduce-transport/) or the PB messages in [MapReduce messages]({{< product-version-root >}}reference/protocol-buffers-api/mapreduce-messages/). Set an application timeout and keep only the phase outputs needed by the caller. Record request scope, result size, errors, and cluster load.

## Verify semantics and capacity

Compare results with a known fixture and test missing keys and function failures. Increase scope gradually while monitoring memory, queues, and latency. Do not assume a distributed job sees an atomic snapshot or that cancelling a client request instantly stops all work.

For an existing JavaScript-heavy workload, record runtime and sandbox requirements before an upgrade. Evaluate a replacement query or application-side computation before investing in new MapReduce dependencies.
