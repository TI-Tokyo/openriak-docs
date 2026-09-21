---
title: Repair and recovery commands
weight: 310
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Repair and recovery commands act on different scopes. Choose the interface matching the affected node,
  vnode, backend, or index, and inspect its release-specific arguments before starting work.
related:
- how-to/data-inspection-and-repair/repair-a-selected-key-range
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- how-to/data-inspection-and-repair/repair-inconsistent-secondary-indexes
- how-to/cluster-lifecycle/back-up-node-data-and-cluster-metadata
- how-to/cluster-lifecycle/restore-node-data-from-a-backup
---

Repair and recovery commands act on different scopes. Choose the interface matching the affected node, vnode, backend, or index, and inspect its release-specific arguments before starting work.

## Command entry points

- {{< cli key="erlang:riak_client:repair_node" >}} reconstructs node data from available replicas.
- {{< cli key="erlang:riak_client:aae_fold:repair_keys_range" >}} selects a bounded repair scope.
- {{< cli key="shell:riak admin repair-2i" >}} is the legacy secondary-index repair family; check backend applicability.
- {{< cli key="erlang:riak_client:hotbackup" >}} exposes the hot-backup interface for compatible backends.
- {{< cli key="shell:riak admin restore" >}} has its own backup-format contract and is not a generic command for every backend directory.

Each linked entry contains the syntax, argument definitions, help, and availability from the CLI metadata. A successfully accepted job is not necessarily a completed recovery; follow the operation's completion and data-verification procedure.
