---
title: Exclude temporary data from cached AAE trees
description: Exclude a bucket's objects from cached AAE trees when they must not participate in all-data comparisons.
  This is a policy change, not a deletion or a general replication filter.
weight: 660
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InstallAndStartGuide.html#property---aae_tree_exclude
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/exclude-bucket-from-aae.md
related:
- how-to/planning-a-deployment/choose-a-deletion-and-retention-policy
- how-to/replication-and-reconciliation/reconcile-selected-buckets
- how-to/cluster-lifecycle/perform-a-rolling-restart
- reference/configuration/bucket-properties-and-defaults
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

Exclude a bucket's objects from cached AAE trees when they must not participate in all-data comparisons. This is a policy change, not a deletion or a general replication filter.

## Confirm the scope

Identify the bucket type or bucket policy to change and every cluster that receives the objects. Plan how excluded data will be reconciled separately if it still needs protection. The objects remain visible to AAE folds even when omitted from cached trees.

The bucket property is `aae_tree_exclude`; it is changed through the bucket-property API rather than a `riak.conf` setting.

## Apply consistently

Set the bucket property using the type or bucket-property interface in [Bucket properties and defaults]({{< product-version-root >}}reference/configuration/bucket-properties-and-defaults/). Coordinate the change with a rolling restart because processes can cache the property. Allow affected AAE trees to rebuild before interpreting all-data comparisons.

## Verify both paths

Check that ordinary object reads still work, that the intended bucket-specific folds can see the data, and that all-data reconciliation no longer reports the deliberately excluded differences. Maintain a separate deletion and retention workflow; exclusion does not prevent stale data from remaining in storage.
