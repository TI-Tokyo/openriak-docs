---
title: AAE commands
description: TicTac AAE commands inspect trees, schedule rebuilds, adjust runtime controls, and submit folds. Availability,
  flags, and help are taken from the selected release's command metadata.
weight: 290
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-the-command-line
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/commands/aae.md
related:
- how-to/monitoring-and-diagnostics/monitor-anti-entropy-progress
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/data-inspection-and-repair/rebuild-aae-trees
- reference/configuration/tictac-anti-entropy-settings
- reference/aae-fold-api/fold-invocation-and-result-conventions
---

TicTac AAE commands inspect trees, schedule rebuilds, adjust runtime controls, and submit folds. Availability, flags, and help are taken from the selected release's command metadata.

{{< cli-command-index prefix="riak/admin/tictacaae" >}}

Runtime changes and persistent configuration are separate. A submitted rebuild or fold is not proof that its background work has finished.
