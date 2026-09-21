---
title: Logging and handler settings
description: Logging settings control destinations, levels, rotation, and handler formats. Confirm the service account
  can write the configured paths and that downstream collectors parse the chosen format.
weight: 200
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- source-code-release-notes-3.4
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
- reference/configuration/logging.md
related:
- how-to/node-configuration/configure-logging-and-change-runtime-log-levels
- how-to/node-configuration/configure-split-and-json-log-handlers
- reference/operations-and-observability/log-files-and-event-formats
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Logging settings control destinations, levels, rotation, and handler formats. Confirm the service account can write the configured paths and that downstream collectors parse the chosen format.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(log\.|logger\.|sasl|read_repair_log|log_index_fsm)
{{< /configuration-reference-table >}}
