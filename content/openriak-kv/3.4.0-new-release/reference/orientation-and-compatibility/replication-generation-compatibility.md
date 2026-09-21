---
title: Replication-generation compatibility
description: Current-generation replication and legacy `riak_repl` are separate protocols with different configuration,
  transport, and fullsync controls.
weight: 50
diataxis: reference
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\multi-datacenter\comparison.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/operations/multi-datacenter-comparison.md
related:
- reference/replication-interfaces/next-generation-replication-runtime-controls
- reference/replication-interfaces/legacy-riak-repl-runtime-controls
- reference/legacy-and-experimental-features/legacy-aae-and-riak-repl-settings
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- how-to/legacy-and-specialist-workflows/maintain-legacy-v2-replication
- how-to/legacy-and-specialist-workflows/maintain-legacy-v3-replication
- foundations/overview/what-openriak-kv-is
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Current-generation replication and legacy `riak_repl` are separate protocols with different configuration, transport, and fullsync controls.

## Current generation

Source queues and sink workers use the `replrtq_*` configuration family. TicTac fullsync uses `ttaaefs_*`. Relationships can connect clusters with different node counts, ring sizes, replica values, and backends when their object policies and supported interfaces are compatible. Configure the actual local and remote replica values for reconciliation.

## Legacy generations

Legacy v2 and v3 use `riak_repl` controls. Their peer, queue, NAT, TLS, and fullsync configuration is not interchangeable with current-generation settings. Legacy replication has ring-size compatibility constraints and is deprecated. Presence of an old command in a package does not make an arbitrary cross-generation relationship supported.

## Shared limits

Replication transfers objects, not complete deployment configuration. Create compatible bucket types and security policy separately. Verify datatype, conflict, deletion, and feature compatibility before upgrading one side or migrating between protocols.
