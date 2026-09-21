---
title: HTTP MapReduce transport
description: '`POST /mapred` submits a legacy MapReduce job. MapReduce is deprecated; the request and execution
  constraints remain relevant to existing clients.'
weight: 570
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\mapreduce.md
source_material:
- legacy-3.2.5
- live-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#the-mapreduce-api
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/mapreduce.md
related:
- how-to/legacy-and-specialist-workflows/configure-and-run-a-mapreduce-job
- reference/legacy-and-experimental-features/mapreduce-jobs-and-functions
- reference/protocol-buffers-api/mapreduce-messages
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

`POST /mapred` submits a legacy MapReduce job. MapReduce is deprecated; the request and execution constraints remain relevant to existing clients.

## Request

The body contains the job's inputs and phases using the selected job encoding, normally JSON with an appropriate content type. Inputs can identify explicit keys or broader sources; broad inputs can cause substantial scans.

## Response

Ordinary responses return the kept phase results. Streaming requests use multipart phase output and must be consumed to completion. Preserve phase identifiers and errors; a partial response is not a completed result.

## Limits

Function availability, code distribution, runtime restrictions, timeout, and memory affect execution. A client timeout does not establish that all distributed work stopped immediately. The job contract is in [MapReduce jobs and functions]({{< product-version-root >}}reference/legacy-and-experimental-features/mapreduce-jobs-and-functions/), with PB transport in [MapReduce messages]({{< product-version-root >}}reference/protocol-buffers-api/mapreduce-messages/).
