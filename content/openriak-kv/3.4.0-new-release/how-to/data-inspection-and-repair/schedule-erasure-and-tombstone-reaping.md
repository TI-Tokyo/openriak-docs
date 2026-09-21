---
title: Schedule erasure and tombstone reaping
description: Schedule erasure and tombstone reaping as separate bounded jobs with clear retention and convergence
  requirements.
weight: 1040
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
- https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data---changing-the-choice
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#garbage-collection---reap-erase-and-scheduled-compaction
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#riak-kv-eraser-and-riak-kv-reaper
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/schedule-object-reaping.md
related:
- how-to/planning-a-deployment/choose-a-deletion-and-retention-policy
- how-to/data-inspection-and-repair/erase-a-selected-set-of-keys
- how-to/data-inspection-and-repair/reap-eligible-tombstones
- how-to/monitoring-and-diagnostics/monitor-replication-and-inter-cluster-reconciliation
- reference/configuration/object-expiration-and-reclamation-settings
- foundations/data-and-consistency/deletion-tombstones-and-expiration
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Schedule erasure and tombstone reaping as separate bounded jobs with clear retention and convergence requirements.

## Define the job scope

Record the bucket/type, key or modified-time bounds, retention rule, and expected count. Run the count-only form first. Keep the job's scope immutable once reviewed so a later configuration change cannot silently broaden a destructive run.

## Coordinate the clusters

Allow deletions to replicate and reconciliation to complete before reaping their tombstones. Configure reap replication where required, or coordinate independent jobs on each cluster. Do not overlap large reap jobs with joins, leaves, or replacements in any connected cluster.

{{< configuration-reference-table >}}
^(delete_mode|repl_reap|tombstone_pause|eraser_overflow_limit|reaper_overflow_limit)$
{{< /configuration-reference-table >}}

## Submit and monitor

Use [Erase a selected set of keys]({{< product-version-root >}}how-to/data-inspection-and-repair/erase-a-selected-set-of-keys/) for erasure and [Reap eligible tombstones]({{< product-version-root >}}how-to/data-inspection-and-repair/reap-eligible-tombstones/) for reaping. Limit each batch so queue capacity and client latency remain acceptable. Track overflow/discards, processing progress, and completion before submitting another batch.

## Keep evidence

Retain the counted scope, submitted operation, completed result, and post-run checks. An accepted request or an empty source queue alone does not prove that every required replica applied the reclamation.
