---
title: Status and statistics
description: '`GET /stats` returns node statistics as JSON. The response describes the addressed node; collect and
  label observations from all members when monitoring a cluster.'
weight: 520
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\http\status.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/http-api/status.md
related:
- how-to/monitoring-and-diagnostics/inspect-node-and-cluster-health
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- how-to/monitoring-and-diagnostics/inspect-worker-queues-and-saturation
- reference/operations-and-observability/node-and-cluster-metrics
- reference/operations-and-observability/replication-metrics
- reference/operations-and-observability/aae-repair-and-worker-pool-metrics
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/quorums-availability-and-durability
---

`GET /stats` returns node statistics as JSON. The response describes the addressed node; collect and label observations from all members when monitoring a cluster.

## Request

```sh
curl --fail -H 'Accept: application/json' "$RIAK_HTTP/stats"
```

Authentication and source policy apply according to the deployment. Avoid unnecessarily frequent polling of expensive statistics.

## Interpretation

Use [Node and cluster metrics]({{< product-version-root >}}reference/operations-and-observability/node-and-cluster-metrics/), [Replication metrics]({{< product-version-root >}}reference/operations-and-observability/replication-metrics/), and [AAE, repair, and worker-pool metrics]({{< product-version-root >}}reference/operations-and-observability/aae-repair-and-worker-pool-metrics/) for metric meanings. Counters, rates, queue depths, and latency samples have different units and aggregation rules. Account for node restarts and counter resets before calculating rates or totals.

Do not sum latency percentiles across nodes. Preserve node identity, timestamp, release, and interval in the monitoring system so a cluster-wide view can be interpreted correctly.
