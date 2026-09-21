---
title: Re-replicate a key range or time window
description: Queue existing objects for a destination by bucket, key interval, or last-modified interval. Use this
  to seed a new cluster or recover a known gap.
weight: 670
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ReplicationGuide.html#re-replicating-keys-for-a-given-time-period
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/rereplicate-time-window.md
related:
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/count-objects-in-a-selected-scope
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- reference/aae-fold-api/replicate-keys-in-a-range
- tutorials/replication-and-reconciliation/re-replicate-a-selected-time-window
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
---

Queue existing objects for a destination by bucket, key interval, or last-modified interval. Use this to seed a new cluster or recover a known gap.

## Bound the operation

Confirm the destination queue exists on all source nodes and has active consumers. Record the exact type, bucket, inclusive key bounds, and optional server last-modified interval. Estimate the number of matching objects with a read-only fold before submitting a large range.

## Submit the range

Open the source remote console. This example queues the untyped `events` bucket's keys `event-001` through `event-099` to `cluster_b`:

{{< cli-example key="erlang:riak_client:aae_fold:repl_keys_range" args=`{repl_keys_range, <<"events">>, {<<"event-001">>, <<"event-099">>}, all, cluster_b}` >}}

Use the filter types in [Fold filters]({{< product-version-root >}}reference/aae-fold-api/fold-filters/) for typed buckets and time bounds. For a long-running operation, use [Run and retrieve a long-running AAE fold]({{< product-version-root >}}how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold/) to retain and retrieve its result.

## Verify delivery

The fold result counts queued references, not completed destination writes. Monitor source overflow/discards and sink errors, compare known values at the destination, and complete a reconciliation check. Do not clear a queue to make its length look healthy; doing so discards pending work.

Widen the range only when evidence shows the gap extends beyond the original bounds. The operation sends current stored versions, not a historical snapshot of the selected interval.
