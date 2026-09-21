---
title: Reconcile selected buckets
description: Restrict a fullsync manager to one bucket when the receiving cluster intentionally stores only a subset
  of the source. Bucket-scoped checks build trees from the selected data and can cost more than cached all-data
  checks
weight: 650
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
- https://openriak.github.io/riak/ReplicationGuide.html#configuration-of-per-bucket-reconciliation
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/per-bucket-reconciliation.md
related:
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- how-to/replication-and-reconciliation/exclude-temporary-data-from-cached-aae-trees
- tutorials/replication-and-reconciliation/reconcile-selected-buckets
- reference/configuration/next-generation-replication-settings
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
---

Restrict a fullsync manager to one bucket when the receiving cluster intentionally stores only a subset of the source. Bucket-scoped checks build trees from the selected data and can cost more than cached all-data checks.

## Set the scope and bucket

Keep the peer and queue settings from [Configure and schedule fullsync]({{< product-version-root >}}how-to/replication-and-reconciliation/configure-and-schedule-fullsync/). For the untyped bucket `events`, use:

{{< settings-example >}}
ttaaefs_scope = bucket
ttaaefs_bucketfilter_name = events
ttaaefs_bucketfilter_type = default
{{< /settings-example >}}

For a typed bucket, replace `default` with its active type name. Configure the same object policy on both sides. Do not set `ttaaefs_scope` to the bucket name: `bucket` is the scope value and the name belongs in its own setting.

## Apply and verify

Validate and restart the affected manager's node. Prompt an `all_check` through [Fullsync requests and results]({{< product-version-root >}}reference/replication-interfaces/fullsync-requests-and-results/), wait for queued repairs, and inspect the completed exchange. Test a known difference inside the selected bucket and confirm unrelated buckets are outside the comparison.

## Cover older changes

Recent-range checks can miss old changes such as resurrected values outside their time interval. Include periodic whole-bucket checks in the schedule and measure their cost. When changing the scope back to `all`, verify that the cached trees include the intended buckets and that the replication filters can deliver their repairs.
