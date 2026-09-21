---
title: MapReduce jobs and functions
description: A MapReduce job specifies inputs and a sequence of phases. Kept phase outputs form the returned result.
  This interface is deprecated.
weight: 1320
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- developers
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#the-mapreduce-api
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/data-model/mapreduce.md
related:
- how-to/legacy-and-specialist-workflows/configure-and-run-a-mapreduce-job
- reference/http-api/http-mapreduce-transport
- reference/protocol-buffers-api/mapreduce-messages
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

A MapReduce job specifies inputs and a sequence of phases. Kept phase outputs form the returned result. This interface is deprecated.

## JSON job shape

```json
{
  "inputs": [["example", "key-a"], ["example", "key-b"]],
  "query": [
    {"map": {"language":"erlang", "module":"riak_kv_mapreduce", "function":"map_object_value", "keep":true}}
  ]
}
```

This example selects two explicit objects. Broader bucket inputs can cause expensive scans. A phase selects an available function and optional argument; `keep` determines whether that phase's output is included in the response. Supported execution languages and function-loading policy depend on the installed release and configuration.

## Semantics and constraints

Map phases operate on their inputs; reduce phases combine intermediate results. Functions may run on multiple nodes, so required code must be installed consistently. Results are not an atomic snapshot, and retained intermediate data can consume substantial memory. Handle missing inputs and function failures explicitly.

HTTP and PB transports define their own framing and completion signals. A client timeout does not guarantee immediate cancellation of all distributed work.
