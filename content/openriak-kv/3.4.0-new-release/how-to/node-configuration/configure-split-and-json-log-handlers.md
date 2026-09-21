---
title: Configure split and JSON log handlers
description: Route OpenRiak log categories to separate handlers or JSON output, then verify that the intended events
  reach the collector.
weight: 280
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/logging-json-handlers.md
related:
- how-to/node-configuration/configure-logging-and-change-runtime-log-levels
- reference/configuration/logging-and-handler-settings
- reference/operations-and-observability/log-files-and-event-formats
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/cluster-architecture/the-lifecycle-of-a-read-and-a-write
---

Route OpenRiak log categories to separate handlers or JSON output, then verify that the intended events reach the collector.

## Select handlers and format

Inspect the active logging configuration and the release-specific handler settings:

{{< configuration-reference-table >}}
^logger\.
{{< /configuration-reference-table >}}

Choose destinations on a writable filesystem and a rotation policy with enough capacity for an incident. Keep an existing working destination while introducing a new structured handler.

## Apply and verify

Validate configuration, apply it using the supported restart or runtime-change mechanism, and generate a normal service event. Check that the JSON parses as one record per expected event and that timestamps, severity, and message fields survive the collection pipeline.

Check each split category rather than assuming one successful event verifies every handler. Also check what happens when rotation occurs and when the collector reconnects.

## Restore normal operation

Remove duplicate temporary handlers and restore the intended diagnostic level after investigation. Watch disk usage during the change; separate files can still compete for the same filesystem.
