---
title: Leveled settings
description: Leveled settings control journals, ledgers, caches, compaction, and storage maintenance. Check units
  and restart requirements before changing an active store.
weight: 150
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
- reference/configuration/leveled.md
related:
- how-to/storage-maintenance/configure-leveled
- how-to/storage-maintenance/schedule-leveled-compaction
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Leveled settings control journals, ledgers, caches, compaction, and storage maintenance. Check units and restart requirements before changing an active store.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(leveled\.|multi_backend\.\$name\.leveled\.)
{{< /configuration-reference-table >}}
