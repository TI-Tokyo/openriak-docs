---
title: Legacy AAE and riak_repl settings
weight: 1310
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: These settings belong to legacy active anti-entropy and legacy multi-datacenter replication. Use the
  current TicTac and next-generation replication catalogues for the corresponding newer implementations.
related:
- how-to/legacy-and-specialist-workflows/maintain-legacy-active-anti-entropy
- how-to/legacy-and-specialist-workflows/maintain-legacy-v2-replication
- how-to/legacy-and-specialist-workflows/maintain-legacy-v3-replication
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

These settings belong to legacy active anti-entropy and legacy multi-datacenter replication. Use the current TicTac and next-generation replication catalogues for the corresponding newer implementations.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(anti_entropy|mdc\.)
{{< /configuration-reference-table >}}
