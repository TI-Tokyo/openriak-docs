---
title: Reduce Query API cost
weight: 1250
product: OpenRiak KV
product_version: 3.4.0
diataxis: how-to
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Reduce Query API cost by changing a measured part of the query while preserving its answer.
related:
- how-to/performance/benchmark-a-representative-workload
- how-to/monitoring-and-diagnostics/inspect-worker-queues-and-saturation
- reference/configuration/query-execution-settings
- reference/query-api/accumulation-modes
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/storage-and-performance/capacity-and-growth
---

Reduce Query API cost by changing a measured part of the query while preserving its answer.

## Record a baseline

Save the request body, result, latency distribution, dataset size, and concurrent workload. Measure several executions, including a normal background-work period. Record the index range scanned and result size separately.

## Make one change

- Narrow the ordered range when the current scan examines many irrelevant terms.
- Project attributes needed for filtering to avoid fetching every candidate object.
- Simplify an expensive evaluation or filter expression without changing its predicate.
- Return counts or grouped counts when the caller does not need every key.
- Use the supported bounded delivery mode when response size dominates memory or transport.

## Verify correctness and impact

Compare results against the same known dataset, including boundary and duplicate cases. Measure tail latency, worker queues, backend load, and the effect on writes and repair. Retain a change only when it improves the intended metric without violating the application's result contract.

If extra concurrency merely lengthens queues, reduce offered work or address the constrained resource rather than raising timeouts.
