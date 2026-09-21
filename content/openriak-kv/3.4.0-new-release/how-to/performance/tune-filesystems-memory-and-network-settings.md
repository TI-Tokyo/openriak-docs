---
title: Tune filesystems, memory, and network settings
description: Tune host storage, memory, and networking only when measurements show they constrain the workload.
  Record the host and kernel versions alongside any persistent change.
weight: 1240
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
- openriak-quickdocs-3.4
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\performance.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/tune/_index.md
related:
- how-to/performance/benchmark-a-representative-workload
- how-to/performance/set-and-verify-file-descriptor-limits
- how-to/performance/tune-the-erlang-vm-for-a-measured-bottleneck
- how-to/performance/tune-a-deployment-on-aws
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/storage-and-performance/capacity-and-growth
---

Tune host storage, memory, and networking only when measurements show they constrain the workload. Record the host and kernel versions alongside any persistent change.

## Inspect the actual environment

Check filesystem type and mount options, device latency and queueing, free space, memory pressure and swap activity, network errors, and the process's resource limits. Include container constraints and cloud volume limits where applicable.

## Change one layer at a time

Prefer fixing insufficient I/O capacity or an unsuitable storage layout over masking it with longer timeouts. Test filesystem and I/O scheduler choices on the actual device. Evaluate memory and huge-page policies with the intended OTP and backend rather than applying a universal sysctl list.

## Verify persistence and behaviour

Apply a candidate change to a pilot, repeat the workload through a maintenance cycle, and verify the setting survives reboot if that is intended. Compare request percentiles, errors, background completion, and memory headroom. Revert changes that improve a microbenchmark but worsen the database workload.
