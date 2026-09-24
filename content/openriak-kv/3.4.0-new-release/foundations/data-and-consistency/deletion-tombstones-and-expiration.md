---
title: Deletion, tombstones, and expiration
description: Deleting an object first changes its replicated state. Reclaiming the disk space used by old values
  and deletion markers is a separate operation.
weight: 160
diataxis: Reviewed
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
source_material:
- openriak-quickdocs-3.4
- openriak-discussions
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-22'
review-by: TI Tokyo/JOM
review_scope: editorial & technical
restructured_from:
- foundations/data-model/deletion-policies.md
- foundations/operations/object-deletion-and-tombstones.md
related:
- how-to/planning-a-deployment/choose-a-deletion-and-retention-policy
- how-to/data-inspection-and-repair/reap-eligible-tombstones
- how-to/data-inspection-and-repair/schedule-erasure-and-tombstone-reaping
- reference/data-model-contracts/deletion-tombstone-and-expiration-states
- reference/configuration/object-expiration-and-reclamation-settings
---

Deleting an object changes its replicated state. The reclamation of disk space used by old values and deletion markers is a separate operation.

## Tombstones preserve deletion history

A tombstone allows replicas and replication partners to distinguish a deletion from an object they have not yet received. If that history disappears while an older live copy can still return, repair or replication can make the value reappear.

Retention must therefore account for offline replicas, replication interruptions, backups, and the time required to reconcile them. A short retention interval cannot compensate for a recovery path that reintroduces older data much later.

## Expiration and reclamation

Expiration is a policy for making data eligible to expire. Its scope and behaviour depend on the backend and configuration. Reaping removes eligible tombstones; compaction or merging reclaims storage occupied by obsolete records. These mechanisms have different prerequisites and should not be used interchangeably.

## Application observations

A client can receive a missing-object response while deletion metadata remains stored. Conversely, reducing the number of visible objects does not immediately reduce filesystem usage. Monitoring must distinguish logical data, retained history, and physical storage.

The creation of a lifecycle policy should be done in tandem with replication and restore procedures, rather than in isolation where the two may conflict.
