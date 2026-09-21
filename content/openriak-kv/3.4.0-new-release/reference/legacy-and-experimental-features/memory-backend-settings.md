---
title: Memory backend settings
description: The memory backend keeps data in memory. Its lifecycle and capacity limits differ from durable backends;
  use it only where the application can tolerate the documented loss of in-memory state.
weight: 1290
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/configuration/memory.md
- foundations/storage/memory.md
related:
- how-to/legacy-and-specialist-workflows/maintain-an-in-memory-backend-deployment
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

The memory backend keeps data in memory. Its lifecycle and capacity limits differ from durable backends; use it only where the application can tolerate the documented loss of in-memory state.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(memory_backend\.|multi_backend\.\$name\.memory_backend\.)
{{< /configuration-reference-table >}}
