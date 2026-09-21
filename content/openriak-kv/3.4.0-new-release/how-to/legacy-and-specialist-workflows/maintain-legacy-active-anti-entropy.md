---
title: Maintain legacy active anti-entropy
description: Maintain legacy active anti-entropy where an existing workload still depends on it, and transition
  deliberately to TicTac AAE for current-generation operations.
weight: 1380
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\active-anti-entropy\legacy-aae.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/configure-legacy-aae.md
related:
- how-to/replication-and-reconciliation/enable-tictac-anti-entropy
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- reference/legacy-and-experimental-features/legacy-aae-and-riak-repl-settings
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Maintain legacy active anti-entropy where an existing workload still depends on it, and transition deliberately to TicTac AAE for current-generation operations.

## Inspect the existing configuration

{{< configuration-reference-table >}}
^anti_entropy
{{< /configuration-reference-table >}}

Record tree storage, build schedules, exchange concurrency, and resource use. Legacy AAE uses separate stores and is distinct from TicTac AAE; changing one subsystem's setting does not tune the other.

## Apply and verify a change

Validate the configuration and deploy it to a pilot node. Observe tree builds and exchanges over a full scheduled cycle, checking client latency and disk capacity. Keep rebuild and exchange pressure bounded rather than increasing concurrency after every timeout.

## Transition protection

Enable TicTac using [Enable TicTac anti-entropy]({{< product-version-root >}}how-to/replication-and-reconciliation/enable-tictac-anti-entropy/) and wait for its initial stores and trees before disabling the old mechanism. The mechanisms can overlap during a transition. Verify current repair and reconciliation requirements, then remove obsolete legacy files only after the deployment no longer uses them and the recovery plan permits it.
