---
title: DTrace probes and settings
description: DTrace integration requires a build and platform that supply the relevant tracing support. The configuration
  switch alone does not establish that probes are available in the installed package.
weight: 1340
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
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\reference\dtrace.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/configuration/dtrace.md
related:
- reference/orientation-and-compatibility/platforms-architectures-and-erlang-otp-compatibility
- how-to/troubleshooting/investigate-a-running-node-with-erlang-diagnostics
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

DTrace integration requires a build and platform that supply the relevant tracing support. The configuration switch alone does not establish that probes are available in the installed package.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^dtrace$
{{< /configuration-reference-table >}}
