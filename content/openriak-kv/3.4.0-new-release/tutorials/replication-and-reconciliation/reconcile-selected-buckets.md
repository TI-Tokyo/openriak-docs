---
title: Reconcile selected buckets
weight: 350
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Reconcile only the `repl-demo` bucket and observe that an unrelated bucket is outside the check. Continue
  from the two-cluster replication lab.
related:
- how-to/replication-and-reconciliation/reconcile-selected-buckets
- reference/configuration/next-generation-replication-settings
- reference/replication-interfaces/fullsync-requests-and-results
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
previous_page: tutorials/replication-and-reconciliation/explore-bidirectional-replication
next_page: tutorials/replication-and-reconciliation/re-replicate-a-selected-time-window
---

Reconcile only the `repl-demo` bucket and observe that an unrelated bucket is outside the check. Continue from the two-cluster replication lab.

## Select the bucket

On A, change the fullsync scope to the selected bucket:

{{< settings-example >}}
ttaaefs_scope = bucket
ttaaefs_bucketfilter_name = repl-demo
ttaaefs_bucketfilter_type = default
{{< /settings-example >}}

Keep the peer and queue definitions from [Replicate data between two clusters]({{< product-version-root >}}tutorials/replication-and-reconciliation/replicate-data-between-two-clusters/), restart A, and wait for AAE readiness. For a typed bucket, also supply the matching type using [Next-generation replication settings]({{< product-version-root >}}reference/configuration/next-generation-replication-settings/); this exercise uses the untyped bucket.

## Create an older missing value

Pause B's sink queue as in [Catch up after a replication interruption]({{< product-version-root >}}tutorials/replication-and-reconciliation/catch-up-after-a-replication-interruption/). Write `bucket-check` to A's `repl-demo` bucket and `outside-check` to a separate `outside-demo` bucket. To make a reproducible reconciliation gap, clear A's source queue **only in this disposable lab**, then resume B:

{{< cli-example key="erlang:riak_kv_replrtq_src:clear_rtq" args="cluster_b" >}}

Clearing discards every pending priority in that queue. Confirm both keys are initially absent on B before proceeding.

## Run and observe the scoped check

On A:

{{< cli-example key="erlang:riak_client:ttaaefs_fullsync" args="all_check" >}}

After repairs are delivered, `bucket-check` should appear on B. `outside-check` should remain absent: the configured bucket scope excluded it. Repeat the check until the selected bucket is in sync.

## Restore the lab

Restore `ttaaefs_scope` to `all` and restart A. Prompt another all check and verify that `outside-check` is now delivered as well. Per-bucket checks calculate trees by scanning the selected bucket; they are not necessarily cheaper than cached whole-cluster checks.
