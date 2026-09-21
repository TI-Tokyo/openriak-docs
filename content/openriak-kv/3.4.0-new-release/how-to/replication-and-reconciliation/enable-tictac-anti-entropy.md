---
title: Enable TicTac anti-entropy
description: Enable TicTac anti-entropy on every cluster member and wait for its initial stores and trees to become
  usable before relying on reconciliation or AAE folds.
weight: 590
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\tutorials\enabling-tictac.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\active-anti-entropy\tictac-aae.md
source_material:
- legacy-3.2.5
- source-code-release-notes-3.4
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience---changing-the-choice
- https://openriak.github.io/riak/InitialDesignDecisions.html#proactive-reconciliation
- https://openriak.github.io/riak/ReplicationGuide.html#configuration-of-all-cluster-reconciliation
- https://openriak.github.io/riak/ReplicationGuide.html#enable-tictac-aae
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/enable-tictac-aae.md
related:
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/rebuild-aae-trees
- reference/configuration/tictac-anti-entropy-settings
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
next_page: how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
---

Enable TicTac anti-entropy on every cluster member and wait for its initial stores and trees to become usable before relying on reconciliation or AAE folds.

## Check storage capacity

A sole Leveled backend can provide the native keystore. Other backend arrangements require a parallel store, adding write, memory, and disk overhead. Reserve that capacity and select the parallel-store options required by your planned folds.

{{< configuration-reference-table >}}
^tictacaae_
^aae_tokenbucket$
{{< /configuration-reference-table >}}

## Enable and validate

Set `tictacaae_active` to `active` in the persistent configuration on each node. Enable stored heads for parallel mode if required by your inspection operations. Validate and roll through the nodes; changing the application environment alone does not enable the startup path.

{{< cli-example key="shell:riak chkconfig" >}}

## Wait for readiness

Monitor initial keystore and tree rebuilds. A running node does not imply that its first AAE coverage is complete. Keep existing protection in place while transitioning from legacy AAE; the two mechanisms can overlap during migration.

## Verify progress

Check that exchanges complete, discrepancies produce bounded repair activity, and client latency remains acceptable. Run a small, known-scope statistics fold before scheduling broader operational scans or inter-cluster reconciliation.
