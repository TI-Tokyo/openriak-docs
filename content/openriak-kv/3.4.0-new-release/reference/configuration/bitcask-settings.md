---
title: Bitcask settings
description: Bitcask settings control local files, synchronisation, merging, expiry, and key-directory behaviour.
  Multi-backend variants apply only inside the corresponding named backend definition.
weight: 140
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
- reference/configuration/bitcask.md
related:
- how-to/storage-maintenance/configure-bitcask
- how-to/storage-maintenance/schedule-bitcask-merges
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Bitcask settings control local files, synchronisation, merging, expiry, and key-directory behaviour. Multi-backend variants apply only inside the corresponding named backend definition.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(bitcask\.|multi_backend\.\$name\.bitcask\.)
{{< /configuration-reference-table >}}
