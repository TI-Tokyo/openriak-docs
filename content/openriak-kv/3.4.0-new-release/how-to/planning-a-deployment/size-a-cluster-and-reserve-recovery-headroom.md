---
title: Size a cluster and reserve recovery headroom
description: Estimate capacity from a representative workload, then reserve room for failure recovery and maintenance.
  Use measurements from the intended backend and infrastructure.
weight: 50
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\plan\planning-your-cluster.md
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#choosing-infrastructure
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#nodes
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/plan/size-cluster.md
related:
- how-to/performance/benchmark-a-representative-workload
- how-to/planning-a-deployment/check-production-readiness
- foundations/cluster-architecture/replica-placement-and-failure-domains
- foundations/storage-and-performance/storage-backend-trade-offs
- foundations/storage-and-performance/capacity-and-growth
---

Estimate capacity from a representative workload, then reserve room for failure recovery and maintenance. Use measurements from the intended backend and infrastructure.

## Measure a baseline

Record object count, stored bytes including indexes and metadata, working-set size, peak request rate, request mix, and latency percentiles. Measure disk space and I/O after compaction or merging reaches a steady cycle. Include replica storage and retained tombstones.

## Model a failed member

Calculate the per-node load with the intended number of surviving members. Reserve free space for ownership transfers, backend maintenance, and temporary replication queues. Check memory for Bitcask's key directory or Leveled's caches and concurrent requests; nominal disk capacity alone is insufficient.

## Rehearse the limit

Run a load test with production-like keys and values. Stop one test member, continue traffic, and measure recovery after it returns. Repeat the intended rolling maintenance operation. Choose a node count and resource size that meet the latency and recovery targets in those states, not only at idle.

## Set expansion triggers

Alert on usable disk space, sustained device latency, queue growth, and request percentiles. Include provisioning and handoff time in the trigger threshold. Document the measured bottleneck, expected growth, and the next expansion step.
