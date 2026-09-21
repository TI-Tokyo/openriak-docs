---
title: Re-replicate a selected time window
weight: 360
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Requeue changes from a known time window and confirm that the destination receives them. Complete [[T31]]
  and [[T32]] first.
related:
- how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window
- how-to/troubleshooting/diagnose-stalled-or-incomplete-replication
- reference/aae-fold-api/replicate-keys-in-a-range
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
previous_page: tutorials/replication-and-reconciliation/reconcile-selected-buckets
---

Requeue changes from a known time window and confirm that the destination receives them. Complete [Replicate data between two clusters]({{< product-version-root >}}tutorials/replication-and-reconciliation/replicate-data-between-two-clusters/) and [Catch up after a replication interruption]({{< product-version-root >}}tutorials/replication-and-reconciliation/catch-up-after-a-replication-interruption/) first.

## Record a bounded window

Record a Unix timestamp on the Docker host:

```sh
LOW=$(date -u +%s)
curl --fail -X PUT "$A/buckets/repl-demo/keys/window-check" -H 'Content-Type: text/plain' --data-binary 'time-window example'
HIGH=$(date -u +%s)
printf 'Window: %s to %s\n' "$LOW" "$HIGH"
```

Allow a small margin around the recorded times if node clocks differ or a boundary falls within the same second. Last-modified time is server metadata; it is not an application business timestamp.

## Queue the selected range

In A's remote console, bind `Low` and `High` to your recorded integer seconds. Then submit:

{{< cli-example key="erlang:riak_client:aae_fold:repl_keys_range" args=`{repl_keys_range, <<"repl-demo">>, all, {date, Low, High}, cluster_b}` >}}

The successful result counts references submitted to the queue. Observe the queue and sink logs, then read `window-check` on B. Expect `time-window example`. Requeuing an already delivered object is allowed; this exercise does not require deleting the destination's copy.

## Verify the recovery scope

Prompt a reconciliation check and wait for its completed result. If the cluster still differs, inspect the reported bucket and modified-time bounds before widening the window. Requeuing a time range sends the current stored version of matching objects; it cannot reconstruct historical versions that have been overwritten.

Finish with the cleanup steps in [Replicate data between two clusters]({{< product-version-root >}}tutorials/replication-and-reconciliation/replicate-data-between-two-clusters/) if you no longer need the lab.
