---
title: 'Configure replication'
description: 'Introduce procedures for configuring anti-entropy and replication within and between clusters.'
weight: 1
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#riak-kv---replication-and-reconciliation'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce procedures for configuring anti-entropy and replication within and between clusters.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### OpenRiak KV - Replication and Reconciliation

In the evolution of Riak, there have been two generations of solutions developed to support replication and reconciliation between clusters:

- The now legacy, [`riak_repl` replication](/kv/3.4.1/explanation/replication/v2-and-v3-replication/) which was the recommended replication approach prior to Riak 3.0.10.
  - The `riak_repl` application has evolved through multiple versions of a real-time replication, that supported a push-based model to reliably deliver changes from a source cluster to a sink cluster;
  - The replication approach is backed-up by a reconciliation approach focused on time-consuming key-by-key comparisons, running in the background between clusters on a vnode-by-vnode basis.
- The NextGen replication solution which is the recommended approach in Riak 3.4.
  - The real-time replication approach is by comparison a pull-based model, to allow a sink cluster to fetch results from the source;
  - The replication approach is backed-up with reconciliation through rapid low-cost comparisons between the state of clusters using anti-entropy information, where the comparisons run reliably between clusters with different configurations (e.g. ring-size, node count or n_val).

This guide covers the NextGen replication solution, and further information on alternatives are linked from the [legacy replication section](/kv/3.4.1/explanation/replication/v2-and-v3-replication/).

Replication is considered to have three stages:

- Seeding; populating data in one cluster from another cluster.
  - Not covered in this guide.
  - The recommended approach to seeding using `repl_keys_range` is explained as part of [the AAE Fold API guide](/kv/3.4.1/reference/aae-fold-api/).
- **Real-time replication**; the forwarding of changes between connected clusters as they occur.
- **Reconciliation**; determining if two clusters have the same data at the same version, and automatically resolving any deltas that exist.

Real-time replication is asynchronous in Riak, the availability and performance of one cluster should have no impact on the clusters replicating to it.  With asynchronous replication, under-pinning the system with reconciliation is important to reduce the need for operator intervention.  Simple replication failures should not need to prompt operator activity, as the failure will eventually be automatically resolved.

> The speed and efficiency of inter-cluster reconciliation is a key feature of Riak.  It is normal in production systems to verify clusters are reconciled every few minutes, with the process taking less than 10s, even when clusters contain more than 10 billion objects.

The guide is split into the following sections:

- [An overview of the concepts](/kv/3.4.1/explanation/replication/).
- [Configuration of real-time replication](/kv/3.4.1/how-to/configure/replication/configure-real-time-replication/).
- [Configuration of all-cluster reconciliation](/kv/3.4.1/how-to/configure/replication/configure-fullsync/).
- [Configuration of per-bucket reconciliation](/kv/3.4.1/how-to/configure/replication/per-bucket-reconciliation/).
- [Managing a cluster migration](/kv/3.4.1/how-to/configure/replication/migrate-cluster/).
- [The external Replication API](/kv/3.4.1/reference/replication-api/).
- [Operations and the troubleshooting of replication](/kv/3.4.1/how-to/operate/monitor-reconciliation/).
- [Configuring `riak_repl`](/kv/3.4.1/explanation/replication/v2-and-v3-replication/).
- [Replication scope](/kv/3.4.1/explanation/replication/reconciliation-scope/).

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.

## In this section

- [Configure Fullsync replication](/kv/3.4.1/how-to/configure/replication/configure-fullsync/) — Show operators how to configure fullsync replication and validate data movement.
- [Configure legacy active anti-entropy](/kv/3.4.1/how-to/configure/replication/configure-legacy-aae/) — Show operators how to configure legacy active anti-entropy and validate data movement.
- [Configure next-generation replication](/kv/3.4.1/how-to/configure/replication/configure-next-generation-replication/) — Show operators how to configure next-generation replication and validate data movement.
- [Configure real-time replication](/kv/3.4.1/how-to/configure/replication/configure-real-time-replication/) — Show operators how to configure real-time replication and validate data movement.
- [Configure replication queues](/kv/3.4.1/how-to/configure/replication/configure-replication-queues/) — Show operators how to configure replication queues and validate data movement.
- [Configure replication through NAT](/kv/3.4.1/how-to/configure/replication/configure-replication-through-nat/) — Show operators how to configure replication through nat and validate data movement.
- [Configure replication sink nodes](/kv/3.4.1/how-to/configure/replication/configure-sink-nodes/) — Show operators how to configure replication sink nodes and validate data movement.
- [Configure legacy multi-datacenter replication](/kv/3.4.1/how-to/configure/replication/configure-v2-multi-datacenter/) — Show operators how to configure legacy multi-datacenter replication and validate data movement.
- [Configure current multi-datacenter replication](/kv/3.4.1/how-to/configure/replication/configure-v3-multi-datacenter/) — Show operators how to configure current multi-datacenter replication and validate data movement.
- [Enable TicTac active anti-entropy](/kv/3.4.1/how-to/configure/replication/enable-tictac-aae/) — Show operators how to enable tictac active anti-entropy and validate data movement.
- [Exclude a bucket from cached AAE trees](/kv/3.4.1/how-to/configure/replication/exclude-bucket-from-aae/) — Show operators how to exclude temporary non-replicated bucket data from cached AAE trees.
- [Migrate a cluster with replication](/kv/3.4.1/how-to/configure/replication/migrate-cluster/) — Show operators how to migrate data between compatible clusters with staged validation and rollback points.
- [Configure per-bucket reconciliation](/kv/3.4.1/how-to/configure/replication/per-bucket-reconciliation/) — Show operators how to scope reconciliation to selected buckets and verify convergence.
- [Secure replication connections](/kv/3.4.1/how-to/configure/replication/secure-replication/) — Show operators how to secure replication connections and validate data movement.
