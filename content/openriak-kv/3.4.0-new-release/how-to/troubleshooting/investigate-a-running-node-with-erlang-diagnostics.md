---
title: Investigate a running node with Erlang diagnostics
description: Inspect a running Erlang node when ordinary metrics and logs cannot explain a problem. Keep diagnostic
  scope and duration bounded so investigation does not worsen the incident.
weight: 1340
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#advanced---troubleshoot-via-the-erlang-vm
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#eprof
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#microstate-accounting
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#recon
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#tracing-with-dbg
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/troubleshoot/erlang-vm.md
related:
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console
- how-to/performance/tune-the-erlang-vm-for-a-measured-bottleneck
- how-to/troubleshooting/diagnose-a-slow-or-overloaded-cluster
- reference/operations-and-observability/remote-console-interfaces
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Inspect a running Erlang node when ordinary metrics and logs cannot explain a problem. Keep diagnostic scope and duration bounded so investigation does not worsen the incident.

## Start with inexpensive observations

Record the node, OTP version, workload interval, and symptom. Use [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/) to open a console, then inspect the relevant process or subsystem through [Remote-console interfaces]({{< product-version-root >}}reference/operations-and-observability/remote-console-interfaces/). Avoid dumping all process state or large object values by default.

## Choose a focused diagnostic

Use process mailbox and memory observations for queue growth, scheduler/runtime statistics for CPU questions, and a narrowly scoped trace only when you know the module or process of interest. Profiling and broad tracing can add substantial load; rehearse them outside production and define how to stop them before starting.

## Collect and stop

Capture only the interval needed to correlate the behaviour with the failing request. Stop traces and profilers explicitly, detach the console cleanly, and confirm no diagnostic process continues consuming resources. Protect object contents and credentials in captured output.

Compare the result with client and host observations before changing configuration. Repeat the original symptom check after the fix.
