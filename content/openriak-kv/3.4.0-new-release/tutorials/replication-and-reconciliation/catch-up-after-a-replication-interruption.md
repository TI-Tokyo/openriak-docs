---
title: Catch up after a replication interruption
weight: 330
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Pause the sink from the preceding replication lesson, write a new object, and watch it catch up after
  resuming. Keep both clusters running throughout the interruption so this first exercise preserves the source queue.
related:
- tutorials/replication-and-reconciliation/replicate-data-between-two-clusters
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- how-to/troubleshooting/diagnose-stalled-or-incomplete-replication
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
previous_page: tutorials/replication-and-reconciliation/replicate-data-between-two-clusters
next_page: tutorials/replication-and-reconciliation/explore-bidirectional-replication
---

Pause the sink from the preceding replication lesson, write a new object, and watch it catch up after resuming. Keep both clusters running throughout the interruption so this first exercise preserves the source queue.

## Pause cluster B's consumer

Complete [Replicate data between two clusters]({{< product-version-root >}}tutorials/replication-and-reconciliation/replicate-data-between-two-clusters/). Open B's remote console and suspend its queue:

{{< cli-example key="erlang:riak_kv_replrtq_snk:suspend_snkqueue" args="cluster_b" >}}

Expect `ok`. `not_found` means the queue name or sink setup does not match the preceding lesson.

## Write during the pause

```sh
curl --fail -X PUT "$A/buckets/repl-demo/keys/during-pause" -H 'Content-Type: text/plain' --data-binary 'queued while paused'
curl -i "$B/buckets/repl-demo/keys/during-pause"
```

B should return `404`. On A, inspect the source queue:

{{< cli-example key="erlang:riak_kv_replrtq_src:length_rtq" args="cluster_b" >}}

The queue should contain pending work. Do not clear it.

## Resume and verify

On B:

{{< cli-example key="erlang:riak_kv_replrtq_snk:resume_snkqueue" args="cluster_b" >}}

Repeat the read until the body is `queued while paused`. Check A's queue again and prompt a fullsync check on A using the preceding lesson. Wait for `in_sync=true`.

A source restart, queue overflow, or lost queue file can remove pending references. In that case resuming the sink is insufficient: use reconciliation, and re-seed a bounded range if the gap is large. The following lessons practise those explicit recovery scopes.
