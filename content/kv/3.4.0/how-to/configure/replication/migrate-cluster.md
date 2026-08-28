---
title: 'Migrate a cluster with replication'
description: 'Show operators how to migrate data between compatible clusters with staged validation and rollback points.'
weight: 14
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
  - 'openriak-discussions'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#interconnecting-multiple-clusters---changing-the-choice'
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#ring-size---changing-the-choice'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#migrating-a-cluster'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to migrate data between compatible clusters with staged validation and rollback points.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### Ring size - changing the choice

Once a Ring Size is set, there is no way of updating a cluster in-place.  However the ring-size can be updated using the [cluster migration process]({{< baseurl >}}kv/3.4.0/how-to/configure/replication/migrate-cluster/).

> In environments where the capital cost of hardware is low (e.g. cloud environments), then using cluster migrations to evolve cluster configuration is relatively common.  A cluster migration process requires significant elapsed time, potentially taking multiple days - but is a safe and reliable process, even when a cluster is under application load.

#### Interconnecting multiple clusters - changing the choice

Riak NextGen replication approach is the preferred method for interconnecting multiple clusters, but the legacy `riak_repl` approach to replication continues to be supported in Riak 3.4.  Combining the two approaches is not recommended without an understanding of the underlying code.

The [cluster migration process]({{< baseurl >}}kv/3.4.0/how-to/configure/replication/migrate-cluster/), can be used to migrate from a single cluster environment into a multi-cluster environment.

#### Migrating a cluster

Most operational processes in Riak are supported through simple configuration changes, in-place upgrades or a rolling replacement.  There may be some exceptional changes which require a full cluster migration e.g.: changing the default `n_val`, or resizing the ring.  In a cloud-like environment, where there are no capital costs of temporary infrastructure; this is a relatively simple and low-risk process with replication.

The following stages are required:

- [Initiate a new cluster]({{< baseurl >}}kv/3.4.0/how-to/plan/) with the correct configuration (e.g. alternative ring-size).
- Configure a [new real-time source queue]({{< baseurl >}}kv/3.4.0/how-to/configure/replication/configure-real-time-replication/) on the current cluster for the replacement cluster.
- Enable [sink workers on the new cluster]({{< baseurl >}}kv/3.4.0/how-to/configure/replication/configure-real-time-replication/) to begin to consume real-time changes.
- Use the [AAE folds]({{< baseurl >}}kv/3.4.0/reference/aae-fold-api/) `list_buckets` and `repl_range_keys` to queue up data to seed the new cluster;
  - Ensure that the old cluster is configured with a sufficiently high `replrtq_overflow_limit` per-node, to have a large enough on-disk queue to avoid discarding replication events;
  - [Tune the sink workers]({{< baseurl >}}kv/3.4.0/reference/replication-api/runtime-controls/) on the replacement cluster to avoid overloading the new cluster.
- Enable [reconciliation]({{< baseurl >}}kv/3.4.0/how-to/configure/replication/configure-fullsync/) on the replacement cluster.

Once the two clusters are in an `in_sync = true` state the migration is complete, and application traffic may be switched to the new cluster, and the old cluster can be decommissioned.  It is common for production systems with o(10TB) of data to manage this process in 24 to 72 hours.

> If possible, migrating a cluster should be a rehearsed process, just like any other [repair or replace operational change]({{< baseurl >}}kv/3.4.0/explanation/operations/node-failure-and-recovery/).

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
