---
title: Log files and event formats
description: Log destinations, levels, formats, and rotation are controlled by the selected release's settings.
  Text and JSON handlers can represent the same event differently.
weight: 1040
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\logging.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\logging.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging-and-statistics
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/operations/log-files.md
related:
- how-to/node-configuration/configure-logging-and-change-runtime-log-levels
- how-to/node-configuration/configure-split-and-json-log-handlers
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- reference/configuration/logging-and-handler-settings
- reference/operations-and-observability/error-and-diagnostic-message-catalogue
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Log destinations, levels, formats, and rotation are controlled by the selected release's settings. Text and JSON handlers can represent the same event differently.

## Settings

{{< configuration-reference-table >}}
^log\.
^logger\.
^platform_log_dir$
{{< /configuration-reference-table >}}

## Event identity

Preserve timestamp, node, severity, process, module/function, and structured event reference when present. Backend and replication logs can include operation-specific identifiers, queue names, partition IDs, and durations. Correlate these fields rather than matching a complete human-readable line that can change between releases.

## Operational boundaries

Container stdout/stderr rotation is separate from Riak's own log files. A crash dump is not an ordinary rotated event log and can be large. JSON output must be parsed as JSON rather than split on spaces; text stack traces can span lines. Treat credentials and object contents in diagnostic output as application data with the same access controls.
