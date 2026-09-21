---
title: Evaluate experimental strong consistency
description: Evaluate the deprecated experimental strong-consistency interface only in an isolated cluster with
  a workload that explicitly requires its semantics. Ordinary object quorums do not enable this interface.
weight: 1450
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\strong-consistency.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/strong-consistency.md
related:
- reference/legacy-and-experimental-features/experimental-strong-consistency-interface
- reference/orientation-and-compatibility/feature-status-and-deprecations
- how-to/planning-a-deployment/choose-replication-and-acknowledgement-policies
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Evaluate the deprecated experimental strong-consistency interface only in an isolated cluster with a workload that explicitly requires its semantics. Ordinary object quorums do not enable this interface.

## Check the constraints

Read [Experimental strong-consistency interface]({{< product-version-root >}}reference/legacy-and-experimental-features/experimental-strong-consistency-interface/) for supported operations, feature limitations, and bucket-type requirements. Inventory incompatible indexes, data types, replication, and client features before creating test data. Keep production availability expectations separate from the experiment.

## Prepare a dedicated type

Enable the required experimental configuration from [Experimental strong-consistency interface]({{< product-version-root >}}reference/legacy-and-experimental-features/experimental-strong-consistency-interface/), validate it, and create a dedicated type using [Create and activate bucket types]({{< product-version-root >}}how-to/application-data/create-and-activate-bucket-types/) with the documented consistency property and replica policy. Do not change a populated ordinary type in place and assume its data has become an ensemble-managed dataset.

## Exercise the failure model

Test concurrent writes, missing-key operations, and the application's retry rules. Stop enough test members to cross the available-majority boundary and confirm that requests fail as expected. Inspect ensemble status with the release's available command:

{{< cli-example key="shell:riak admin ensemble-status" >}}

## Decide and clean up

Record both observed consistency and unavailability, along with unsupported features and recovery behaviour. Discard the isolated environment when finished. Do not present a successful single-node demonstration as evidence of a supported production consistency guarantee.
