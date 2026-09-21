---
title: Set and verify file-descriptor limits
description: Set the open-file limit for the actual Riak service process, then verify that it inherited the intended
  value. A shell's `ulimit` does not necessarily control a service manager's child process.
weight: 1200
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- performance-engineers
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\performance\open-files-limit.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InstallAndStartGuide.html#setting-ulimit
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/tune/set-open-files-limit.md
related:
- how-to/cluster-lifecycle/start-stop-or-restart-a-node
- how-to/installation/run-openriak-with-persistent-docker-storage
- how-to/troubleshooting/diagnose-a-slow-or-overloaded-cluster
- reference/configuration/erlang-vm-and-runtime-settings
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/storage-and-performance/capacity-and-growth
---

Set the open-file limit for the actual Riak service process, then verify that it inherited the intended value. A shell's `ulimit` does not necessarily control a service manager's child process.

## Measure usage and limits

Identify the Riak BEAM process from the service or container, then inspect `/proc/PID/limits` and `/proc/PID/fd` on Linux. Compare current descriptor use with the backend's files, client connections, and expected recovery workload.

## Configure the owning launcher

For systemd, set `LimitNOFILE` in a service override and reload the manager before a controlled restart. For OpenRC or a direct launcher, use the service's supported limits configuration. For Docker, set the service's `ulimits.nofile` in Compose. Choose a limit based on the workload and host capacity rather than copying an unrelated shell example.

## Verify after restart

Read the running process's limits again and check logs for open-file errors. Exercise expected peak connections and storage activity. Monitor descriptor growth over time; raising the limit does not fix a leak or an unbounded client connection pool.
