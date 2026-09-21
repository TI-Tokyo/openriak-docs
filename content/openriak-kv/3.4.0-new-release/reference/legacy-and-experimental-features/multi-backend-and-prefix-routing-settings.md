---
title: Multi-backend and prefix-routing settings
description: Named backend definitions and routing select the store used for a dataset. Changing a route does not
  migrate the data already written through it.
weight: 1300
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
- reference/configuration/multi.md
- reference/configuration/prefix-multi.md
related:
- how-to/legacy-and-specialist-workflows/maintain-multi-backend-and-prefix-routing
- how-to/storage-maintenance/migrate-to-another-storage-backend
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Named backend definitions and routing select the store used for a dataset. Changing a route does not migrate the data already written through it.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(multi_backend\.|storage_backend$)
{{< /configuration-reference-table >}}
