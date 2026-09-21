---
title: Feature status and deprecations
description: Feature status distinguishes current interfaces from compatibility features that should not be selected
  for new deployments without a specific requirement.
weight: 40
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
- developers
source_material:
- legacy-3.2.5
- source-code-release-notes-3.4
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\deprecated\riak-search.md
- Deprecated or historical feature material is retained for context and must not imply current support.
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/releases/deprecations.md
related:
- reference/orientation-and-compatibility/replication-generation-compatibility
- reference/orientation-and-compatibility/backend-capability-matrix
- reference/extensions-and-specialist-interfaces/write-once-interface
- reference/extensions-and-specialist-interfaces/redis-add-on-commands-and-configuration
- reference/legacy-and-experimental-features/experimental-strong-consistency-interface
- how-to/storage-maintenance/migrate-to-another-storage-backend
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- foundations/overview/what-openriak-kv-is
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Feature status distinguishes current interfaces from compatibility features that should not be selected for new deployments without a specific requirement.

## Current interfaces

The current Object API, Leveled Query API, TicTac AAE, and next-generation replication are the primary interfaces described in these docs. Availability still depends on backend, configuration, and the selected release; check the command and settings metadata for exact details.

## Deprecated features

The 3.4.0 release notes deprecate LevelDB, the memory backend, multi-backend arrangements other than all-Bitcask configurations, MapReduce, ensemble-backed experimental strong consistency, and DTrace. Legacy v1.4 counters and link walking were already deprecated. The write-once path and legacy replication also have deprecation constraints in their interface documentation.

Deprecation does not mean every interface has already been removed. It means existing users should plan a transition and should not assume continued support in later releases. Conditional token-protected PUTs are not a semantic replacement for every strongly consistent application.

## Compatibility features

Legacy AAE and `riak_repl` remain relevant to existing deployments, but future maintenance is not guaranteed by the 3.4 release notes. The historical Redis add-on has no verified current-release compatibility matrix in this documentation. Verify the exact component versions before relying on it.

## Release additions

The release notes describe features introduced by each version. In particular, queued Query API result delivery and the vnode-status command are 3.4.1 additions; a 3.4.0 page must not imply they are available there.
