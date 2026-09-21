---
title: Tune the Erlang VM for a measured bottleneck
description: Tune the Erlang VM only for a measured bottleneck and with a repeatable rollback. Keep the package's
  baseline values until evidence identifies a limit worth changing.
weight: 1210
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- performance-engineers
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\performance\erlang.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/tune/tune-erlang-vm.md
related:
- how-to/performance/benchmark-a-representative-workload
- how-to/troubleshooting/investigate-a-running-node-with-erlang-diagnostics
- how-to/cluster-lifecycle/perform-a-rolling-restart
- reference/configuration/erlang-vm-and-runtime-settings
- foundations/storage-and-performance/latency-queues-and-resource-contention
---

Tune the Erlang VM only for a measured bottleneck and with a repeatable rollback. Keep the package's baseline values until evidence identifies a limit worth changing.

## Capture the baseline

Record the OTP version, scheduler and process activity, memory categories, port usage, distribution pressure, and client latency. Use [Investigate a running node with Erlang diagnostics]({{< product-version-root >}}how-to/troubleshooting/investigate-a-running-node-with-erlang-diagnostics/) for bounded runtime diagnostics and [Erlang VM and runtime settings]({{< product-version-root >}}reference/configuration/erlang-vm-and-runtime-settings/) for the release's VM settings.

## Select one hypothesis

For example, distinguish scheduler saturation from waiting on storage before changing scheduler counts. Check actual process or port usage before increasing limits. Consider container CPU and memory constraints; the VM cannot make unavailable host resources appear.

## Apply to a pilot

Change the persistent VM setting through the supported configuration path, validate, and restart a pilot member. Keep the old configuration and the exact baseline workload. Avoid changing several interacting scheduler, GC, and buffer options at once.

## Compare and roll out

Measure both throughput and tail latency, memory headroom, and recovery behaviour. Revert if the target improves at an unacceptable cost elsewhere. Apply a successful change through a rolling restart and verify the effective VM arguments on every member.
