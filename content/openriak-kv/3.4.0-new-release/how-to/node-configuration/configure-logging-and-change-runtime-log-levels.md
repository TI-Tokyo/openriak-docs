---
title: Configure logging and change runtime log levels
description: Choose persistent log destinations and temporarily increase detail when investigating a specific problem.
  Record the previous level and the time at which extra logging should end.
weight: 270
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\logging.md
source_material:
- source-code-release-notes-3.4
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/logging.md
- how-to/operate/change-log-level.md
related:
- how-to/node-configuration/configure-split-and-json-log-handlers
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- reference/configuration/logging-and-handler-settings
- reference/operations-and-observability/log-files-and-event-formats
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/cluster-architecture/the-lifecycle-of-a-read-and-a-write
---

Choose persistent log destinations and temporarily increase detail when investigating a specific problem. Record the previous level and the time at which extra logging should end.

## Configure persistent output

Use the release's logging settings to select destinations, levels, and rotation. Ensure the service account can write the log directory and that rotated files fit the available space.

{{< configuration-reference-table >}}
^log\.
^logger\.
{{< /configuration-reference-table >}}

For JSON or separate handler output, use [Configure split and JSON log handlers]({{< product-version-root >}}how-to/node-configuration/configure-split-and-json-log-handlers/). Validate changes and restart only where the selected setting requires it.

## Change detail at runtime

Open the node through [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/) and use the logger interface appropriate to the configured handler. Consult [Logging and handler settings]({{< product-version-root >}}reference/configuration/logging-and-handler-settings/) for the handler and level settings.

Select the intended handler and level using the command's metadata help. Increase verbosity for the shortest useful interval, reproduce the problem, and save logs with node names and timestamps. Avoid broad debug logging across a busy cluster without checking its I/O impact.

## Restore and verify

Return the previous runtime level, confirm rotation still works, and verify that the persistent configuration will produce the intended level after restart. Redact credentials and object contents before sharing logs.
