---
title: Maintain legacy v3 replication
description: Operate an existing legacy v3 `riak_repl` relationship with version-matched commands. Current-generation
  replication uses a different queue and fullsync system.
weight: 1400
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v3-multi-datacenter.md
- Legacy multi-datacenter replication terminology and commands require compatibility review.
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/configure-v3-multi-datacenter.md
related:
- how-to/legacy-and-specialist-workflows/maintain-legacy-v2-replication
- how-to/legacy-and-specialist-workflows/configure-legacy-replication-through-nat
- how-to/legacy-and-specialist-workflows/secure-legacy-replication-connections
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- reference/replication-interfaces/legacy-riak-repl-runtime-controls
- reference/legacy-and-experimental-features/legacy-aae-and-riak-repl-settings
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Operate an existing legacy v3 `riak_repl` relationship with version-matched commands. Current-generation replication uses a different queue and fullsync system.

## Inspect the relationship

{{< cli-example key="shell:riak repl status" >}}

Record remote cluster names, enabled real-time and fullsync relationships, connection failures, and pending work. Compare both ends and check [Replication-generation compatibility]({{< product-version-root >}}reference/orientation-and-compatibility/replication-generation-compatibility/) for compatibility constraints.

## Change one relationship

Use the available command help in [Legacy riak_repl runtime controls]({{< product-version-root >}}reference/replication-interfaces/legacy-riak-repl-runtime-controls/) for the exact remote cluster and operation. Preserve the existing settings and avoid mixing v2 listener configuration with v3 cluster-manager configuration. For certificate changes use [Secure legacy replication connections]({{< product-version-root >}}how-to/legacy-and-specialist-workflows/secure-legacy-replication-connections/), and for translated addresses use [Configure legacy replication through NAT]({{< product-version-root >}}how-to/legacy-and-specialist-workflows/configure-legacy-replication-through-nat/).

## Verify delivery and reconciliation

Write, update, and delete a sample through the normal application path. Confirm arrival and completed legacy fullsync; a connected status alone is insufficient. Monitor the workload during fullsync and investigate repeated rebuild or exchange failures.

For a new relationship or a migration away from deprecated replication, follow [Connect clusters with next-generation replication]({{< product-version-root >}}how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication/) and verify the new path before retiring this one.
