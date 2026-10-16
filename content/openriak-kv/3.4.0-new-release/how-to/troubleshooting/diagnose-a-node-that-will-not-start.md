---
title: Diagnose a node that will not start
description: Diagnose a node that does not reach a usable running state. Preserve the first startup error before
  repeatedly restarting it.
weight: 1260
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- developers
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: complete
last_reviewed: '2026-10-15'
review_scope: content review
review-by: TI Tokyo/JOM
restructured_from:
- how-to/troubleshoot/startup-failures.md
related:
- how-to/node-configuration/validate-configuration-before-startup
- how-to/installation/verify-an-installation
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- reference/configuration/node-identity-directories-and-ring-settings
- reference/operations-and-observability/log-files-and-event-formats
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
features: ["observability"]
concepts: ["diagnostics"]
---

Diagnose a node that does not reach a usable running state. Preserve the first startup error before repeatedly restarting it.

## Check configuration

Run the configuration check below and correct the first reported syntax or schema error. Inspect both riak.conf and advanced.config, plus service overrides.

{{< cli-example key="shell:riak chkconfig" >}}

## Check the host

Verify file ownership, available disk space, file-descriptor limits, and that another process is not already using the configured listeners. Confirm the node hostname resolves as intended.

## Check backend startup

Read the startup log for the first backend failure. Preserve the affected files; a missing directory and a corrupt existing store require different actions.

## Verify the correction

Start once, check node response and listeners, then perform a write/read round trip. If the cause remains unclear, collect the diagnostic record before another change.

## Diagnostic commands

To check your config

{{< cli-example key="shell:riak chkconfig" >}}

To ping the node

{{< cli-example key="shell:riak ping" >}}
