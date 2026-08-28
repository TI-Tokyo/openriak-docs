---
title: 'Replication API reference'
description: 'Define replication references, triggers, runtime controls, monitoring fields, and request limits.'
weight: 1
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
  - 'developers'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#repl_keys_range'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#replication-api'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#riak-kv---replication-and-reconciliation'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define replication references, triggers, runtime controls, monitoring fields, and request limits.

## Details

### repl_keys_range

Used to replicate a range of keys to another cluster (or indeed any consumer of a given replication queue).  To be used when seeding new clusters, or if there is a known delta that can be expressed and resolved more quickly by this mechanism rather than by waiting for inter-cluster reconciliation to auto-heal.

- When adding to the replication queue, will be added with a lower priority when compared to real-time replication.
- Each replication queue has a small in-memory part but a large on-disk part.  The size of the on-disk component is controlled in `riak.conf` via `replrtq_overflow_limit`.
- Uses the AF4 queue when running node worker pools in `dscp` mode.

#### OpenRiak KV - Replication and Reconciliation

In the evolution of Riak, there have been two generations of solutions developed to support replication and reconciliation between clusters:

- The now legacy, [`riak_repl` replication]({{< baseurl >}}kv/3.4.1/explanation/replication/v2-and-v3-replication/) which was the recommended replication approach prior to Riak 3.0.10.
  - The `riak_repl` application has evolved through multiple versions of a real-time replication, that supported a push-based model to reliably deliver changes from a source cluster to a sink cluster;
  - The replication approach is backed-up by a reconciliation approach focused on time-consuming key-by-key comparisons, running in the background between clusters on a vnode-by-vnode basis.
- The NextGen replication solution which is the recommended approach in Riak 3.4.
  - The real-time replication approach is by comparison a pull-based model, to allow a sink cluster to fetch results from the source;
  - The replication approach is backed-up with reconciliation through rapid low-cost comparisons between the state of clusters using anti-entropy information, where the comparisons run reliably between clusters with different configurations (e.g. ring-size, node count or n_val).

This guide covers the NextGen replication solution, and further information on alternatives are linked from the [legacy replication section]({{< baseurl >}}kv/3.4.1/explanation/replication/v2-and-v3-replication/).

Replication is considered to have three stages:

- Seeding; populating data in one cluster from another cluster.
  - Not covered in this guide.
  - The recommended approach to seeding using `repl_keys_range` is explained as part of [the AAE Fold API guide]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/).
- **Real-time replication**; the forwarding of changes between connected clusters as they occur.
- **Reconciliation**; determining if two clusters have the same data at the same version, and automatically resolving any deltas that exist.

Real-time replication is asynchronous in Riak, the availability and performance of one cluster should have no impact on the clusters replicating to it.  With asynchronous replication, under-pinning the system with reconciliation is important to reduce the need for operator intervention.  Simple replication failures should not need to prompt operator activity, as the failure will eventually be automatically resolved.

> The speed and efficiency of inter-cluster reconciliation is a key feature of Riak.  It is normal in production systems to verify clusters are reconciled every few minutes, with the process taking less than 10s, even when clusters contain more than 10 billion objects.

The guide is split into the following sections:

- [An overview of the concepts]({{< baseurl >}}kv/3.4.1/explanation/replication/).
- [Configuration of real-time replication]({{< baseurl >}}kv/3.4.1/how-to/configure/replication/configure-real-time-replication/).
- [Configuration of all-cluster reconciliation]({{< baseurl >}}kv/3.4.1/how-to/configure/replication/configure-fullsync/).
- [Configuration of per-bucket reconciliation]({{< baseurl >}}kv/3.4.1/how-to/configure/replication/per-bucket-reconciliation/).
- [Managing a cluster migration]({{< baseurl >}}kv/3.4.1/how-to/configure/replication/migrate-cluster/).
- [The external Replication API]({{< baseurl >}}kv/3.4.1/reference/replication-api/).
- [Operations and the troubleshooting of replication]({{< baseurl >}}kv/3.4.1/how-to/operate/monitor-reconciliation/).
- [Configuring `riak_repl`]({{< baseurl >}}kv/3.4.1/explanation/replication/v2-and-v3-replication/).
- [Replication scope]({{< baseurl >}}kv/3.4.1/explanation/replication/reconciliation-scope/).

#### Replication API

All real-time and full-sync operations are available via the Riak API, and supported by the Riak erlang clients (both PB and HTTP).  They have been used in different systems for replicating and synchronising with third party databases, such as OpenSearch or DynamoDB.

It is recommended to use the PB API for both performance and security reasons (as TLS can be enabled via this API for replication).  The HTTP API is slower, but may be useful where it is easier to set up peer relationships with a HTTP-based load-balancer rather than an individual node.

The replication API consists of [the AAE fold API]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/) and the [fetch API required to access replication queues]({{< baseurl >}}kv/3.4.1/reference/specialized-apis/fetch-api/).

## In this section

- [Replication runtime control reference]({{< baseurl >}}kv/3.4.1/reference/replication-api/runtime-controls/) — List supported source, sink, queue, reconciliation, range, and resynchronization controls.
