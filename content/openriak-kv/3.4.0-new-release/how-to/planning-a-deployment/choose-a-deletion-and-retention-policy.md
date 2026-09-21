---
title: Choose a deletion and retention policy
description: Choose how long deleted or expired data remains recoverable and how storage is reclaimed. Apply the
  policy consistently across replicating clusters.
weight: 100
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data
- https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data---making-a-choice
- https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---delete-mode
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/plan/choose-deletion-policy.md
related:
- how-to/node-configuration/configure-object-expiration
- how-to/data-inspection-and-repair/locate-tombstones
- how-to/data-inspection-and-repair/reap-eligible-tombstones
- how-to/data-inspection-and-repair/schedule-erasure-and-tombstone-reaping
- reference/configuration/object-expiration-and-reclamation-settings
- foundations/data-and-consistency/deletion-tombstones-and-expiration
- foundations/storage-and-performance/persistence-filesystems-and-space-reclamation
---

Choose how long deleted or expired data remains recoverable and how storage is reclaimed. Apply the policy consistently across replicating clusters.

## Select deletion behaviour

For replicated deployments, retain tombstones long enough for every destination and temporarily unavailable replica to observe deletion. Review the current values rather than assuming a package default:

{{< configuration-reference-item config-name="delete_mode" >}}

Use `keep` when tombstones will be reaped explicitly after reconciliation. Account for that retained storage in capacity planning. A time-based delete mode needs an outage and reconciliation policy compatible with its retention period.

## Decide whether expiration is suitable

Use object expiration only when the application's retention rule matches backend support and the timestamp semantics. Test reads, updates, replication, and reappearance after an outage before enabling it for existing data. Expiration is not a substitute for an application audit or an immutable history.

## Schedule reclamation

First count or list the intended scope. Complete required reconciliation before erasing objects or reaping tombstones, and avoid overlapping reaping with membership changes. Start with a small range and monitor client latency and worker queues.

## Verify

Read known live and deleted samples from all receiving clusters. Check that expired data is handled as expected and that maintenance eventually releases space without resurrecting deleted values.
