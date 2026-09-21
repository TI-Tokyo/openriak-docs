---
title: Choose a storage backend
description: Select a backend according to required query features, data size, memory budget, and maintenance behaviour.
  Make the choice before loading a new node's data.
weight: 70
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#database-backend
- https://openriak.github.io/riak/InitialDesignDecisions.html#database-backend---making-a-choice
tags:
- diataxis
- kv
- how-to
- quickdocs
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/plan/choose-storage-backend.md
related:
- how-to/storage-maintenance/configure-bitcask
- how-to/storage-maintenance/configure-leveled
- how-to/storage-maintenance/migrate-to-another-storage-backend
- reference/orientation-and-compatibility/backend-capability-matrix
- foundations/cluster-architecture/replica-placement-and-failure-domains
- foundations/storage-and-performance/storage-backend-trade-offs
- foundations/storage-and-performance/capacity-and-growth
---

Select a backend according to required query features, data size, memory budget, and maintenance behaviour. Make the choice before loading a new node's data.

## Check required capabilities

Use [Backend capability matrix]({{< product-version-root >}}reference/orientation-and-compatibility/backend-capability-matrix/) to check secondary indexes, Query API support, and backup capabilities. Choose Leveled when the application needs the current Query API. Evaluate Bitcask for direct-key workloads where its in-memory key directory fits the resource budget. Treat deprecated backends as compatibility choices for existing deployments.

## Measure with representative data

Compare sustained write and read latency, startup time, disk use, maintenance I/O, and memory at the expected key count. Include deletion and compaction behaviour, not only a short empty-store benchmark.

## Configure and verify

Set the selected backend on empty nodes and validate configuration before startup:

{{< configuration-reference-item config-name="storage_backend" >}}

Write, update, delete, and query sample data through the required interfaces. Record the tested backend and filesystem in the deployment specification. For a populated deployment use [Migrate to another storage backend]({{< product-version-root >}}how-to/storage-maintenance/migrate-to-another-storage-backend/); changing a setting alone does not migrate its files.
