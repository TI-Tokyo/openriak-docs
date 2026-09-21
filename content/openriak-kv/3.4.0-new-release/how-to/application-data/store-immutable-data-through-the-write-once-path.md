---
title: Store immutable data through the write-once path
description: Maintain an existing write-once application while planning migration to the normal object PUT path.
  The write-once interface is deprecated and lacks feature parity with coordinated writes, including real-time replication
weight: 520
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#write-once-path-api
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/use-write-once-path.md
related:
- how-to/application-data/create-and-store-an-object
- how-to/application-data/make-conditional-reads-and-writes
- how-to/replication-and-reconciliation/migrate-to-another-cluster-using-replication
- reference/extensions-and-specialist-interfaces/write-once-interface
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/bucket-types-and-data-policies
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Maintain an existing write-once application while planning migration to the normal object PUT path. The write-once interface is deprecated and lacks feature parity with coordinated writes, including real-time replication.

## Confirm the application's assumptions

Inventory bucket types using the write-once property and verify that keys are truly immutable. Identify any reliance on indexes, conditional updates, replication, or repair before changing the policy. Use [Write-once interface]({{< product-version-root >}}reference/extensions-and-specialist-interfaces/write-once-interface/) for the interface constraints.

## Test the normal write path

Create a separate test type using ordinary object properties, write representative immutable values through [Create and store an object]({{< product-version-root >}}how-to/application-data/create-and-store-an-object/), and compare latency and required features. Preserve the application's key uniqueness rule; the normal PUT path does not by itself prevent an accidental replacement.

## Migrate deliberately

Move or replay the data into the intended type or cluster and validate known keys and counts. Update clients to the normal endpoint and policy, retaining the original data until verification is complete. Do not enable replication on an old write-once workload and assume previously uncoordinated writes have been delivered.
