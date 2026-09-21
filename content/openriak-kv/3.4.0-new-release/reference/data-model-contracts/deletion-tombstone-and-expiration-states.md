---
title: Deletion, tombstone, and expiration states
description: Deletion, tombstone retention, and physical reclamation are different object states. Expiration is
  backend-specific and must not be assumed to have the same propagation behaviour as an explicit object delete.
weight: 400
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\object-deletion.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---delete-mode
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/operations/object-deletion.md
related:
- how-to/planning-a-deployment/choose-a-deletion-and-retention-policy
- how-to/node-configuration/configure-object-expiration
- reference/aae-fold-api/find-tombstones
- reference/aae-fold-api/count-tombstones
- reference/aae-fold-api/erase-keys
- reference/aae-fold-api/reap-tombstones
- foundations/data-and-consistency/deletion-tombstones-and-expiration
---

Deletion, tombstone retention, and physical reclamation are different object states. Expiration is backend-specific and must not be assumed to have the same propagation behaviour as an explicit object delete.

## States

A live object has content and causal history. A delete can leave a tombstone carrying deletion evidence even when an ordinary GET returns missing. Reaping removes retained tombstone state after the deployment's recovery and replication requirements permit it. Backend maintenance later reclaims obsolete storage.

## Configuration

{{< configuration-reference-table >}}
^(delete_mode|repl_reap|tombstone_pause)$
^bitcask\.expiry
^leveldb\.expiration
{{< /configuration-reference-table >}}

## Observable behaviour

A missing-object response does not prove that no tombstone exists. Object counts, tombstone counts, backend bytes, and files can change at different times. Removing deletion evidence before disconnected replicas or destinations catch up can allow old values to reappear.

The AAE fold interfaces distinguish counting, erasing live keys, and reaping tombstones; their change method determines whether the request mutates data.
