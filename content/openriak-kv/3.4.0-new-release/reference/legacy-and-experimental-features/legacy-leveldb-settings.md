---
title: Legacy LevelDB settings
description: 'These LevelDB settings are retained for existing deployments. Check the release and runtime compatibility
  before maintenance or upgrades; a setting appearing here is not a recommendation to choose this backend for a
  new '
weight: 1280
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
- reference/configuration/leveldb.md
- foundations/storage/leveldb.md
related:
- how-to/legacy-and-specialist-workflows/maintain-a-legacy-leveldb-deployment
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

These LevelDB settings are retained for existing deployments. Check the release and runtime compatibility before maintenance or upgrades; a setting appearing here is not a recommendation to choose this backend for a new cluster.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(leveldb\.|multi_backend\.\$name\.leveldb\.)
{{< /configuration-reference-table >}}
