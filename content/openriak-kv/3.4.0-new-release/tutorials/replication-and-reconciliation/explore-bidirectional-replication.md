---
title: Explore bidirectional replication
weight: 340
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Extend the one-way lab so each cluster can receive new writes from the other. Start with [[T31]] and
  keep both datasets small and disposable.
related:
- tutorials/data-and-concurrency/create-and-resolve-concurrent-updates
- how-to/planning-a-deployment/choose-a-multi-cluster-topology
- how-to/replication-and-reconciliation/configure-replication-queues-and-filters
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
previous_page: tutorials/replication-and-reconciliation/catch-up-after-a-replication-interruption
next_page: tutorials/replication-and-reconciliation/reconcile-selected-buckets
---

Extend the one-way lab so each cluster can receive new writes from the other. Start with [Replicate data between two clusters]({{< product-version-root >}}tutorials/replication-and-reconciliation/replicate-data-between-two-clusters/) and keep both datasets small and disposable.

## Add the reverse path

On B, enable a source queue named `cluster_a` using the source settings from the first lesson. On A, enable sink workers for `cluster_a`, pointing at B's bridge address with peer discovery disabled. Keep the existing A-to-B settings as well. Restart each cluster and check both endpoints.

The result is two independent paths: A's `cluster_b` queue is consumed by B; B's `cluster_a` queue is consumed by A. Do not reuse one queue for two independent destinations.

## Write independently on each side

```sh
curl --fail -X PUT "$A/buckets/repl-demo/keys/from-a" -H 'Content-Type: text/plain' --data-binary 'A'
curl --fail -X PUT "$B/buckets/repl-demo/keys/from-b" -H 'Content-Type: text/plain' --data-binary 'B'
curl -i "$B/buckets/repl-demo/keys/from-a"
curl -i "$A/buckets/repl-demo/keys/from-b"
```

Repeat the reads until each returns the other cluster's value. These distinct keys avoid introducing a conflict during the connectivity check.

## Make reconciliation bidirectional

On A set `ttaaefs_queuename_peer` to `cluster_a`. Its local queue remains `cluster_b`. On B configure the reciprocal peer relationship, with local queue `cluster_a` and peer queue `cluster_b`. Use cluster slice 1 on A and 3 on B so their scheduled work is separated.

{{< configuration-reference-table >}}
^ttaaefs_
{{< /configuration-reference-table >}}

Restart, prompt an all check, and wait for a completed in-sync result. A check can now request newer versions in either direction.

## Observe a conflicting update

Use the explicit sibling policy and context-handling steps from [Create and resolve concurrent updates]({{< product-version-root >}}tutorials/data-and-concurrency/create-and-resolve-concurrent-updates/) on both clusters. Pause both sink queues, update the same key independently on A and B from the same starting context, then resume both queues. Read all siblings and resolve them using the combined causal context. Verify the resolved value on both clusters.

Do not infer last-writer ordering from wall-clock timestamps. Application conflict handling is still required when replication is bidirectional.
