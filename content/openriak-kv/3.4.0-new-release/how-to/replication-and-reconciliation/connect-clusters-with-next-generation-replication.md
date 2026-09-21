---
title: Connect clusters with next-generation replication
description: Connect two clusters using current-generation source queues, sink consumers, and reconciliation. Use
  [[H8]] to decide which data moves in each direction before configuring the nodes.
weight: 600
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- source-code-release-notes-3.4
- openriak-discussions
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\next-gen-replication.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/configure-next-generation-replication.md
related:
- how-to/replication-and-reconciliation/enable-real-time-replication
- how-to/replication-and-reconciliation/configure-replication-queues-and-filters
- how-to/replication-and-reconciliation/configure-sink-nodes-and-consumers
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- how-to/replication-and-reconciliation/secure-next-generation-replication-connections
- tutorials/replication-and-reconciliation/replicate-data-between-two-clusters
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
previous_page: how-to/replication-and-reconciliation/enable-tictac-anti-entropy
next_page: how-to/replication-and-reconciliation/configure-replication-queues-and-filters
---

Connect two clusters using current-generation source queues, sink consumers, and reconciliation. Use [Choose a multi-cluster topology]({{< product-version-root >}}how-to/planning-a-deployment/choose-a-multi-cluster-topology/) to decide which data moves in each direction before configuring the nodes.

## Prepare both clusters

Verify healthy membership, compatible object policies, and reachable client listeners. Create matching bucket types on the destination; replication copies objects, not the type definitions, users, certificates, or other cluster metadata.

Enable TicTac AAE using [Enable TicTac anti-entropy]({{< product-version-root >}}how-to/replication-and-reconciliation/enable-tictac-anti-entropy/) and wait for initial stores and trees. Prefer PB transport for efficiency and use [Secure next-generation replication connections]({{< product-version-root >}}how-to/replication-and-reconciliation/secure-next-generation-replication-connections/) when TLS is required. Do not expose unprotected replication endpoints on public networks.

## Establish delivery

Define a dedicated source queue for each destination using [Configure replication queues and filters]({{< product-version-root >}}how-to/replication-and-reconciliation/configure-replication-queues-and-filters/). Enable source queuing on every possible write coordinator, then configure destination consumers with [Configure sink nodes and consumers]({{< product-version-root >}}how-to/replication-and-reconciliation/configure-sink-nodes-and-consumers/). Verify a new write arrives before seeding old data.

## Seed and reconcile

Use [Re-replicate a key range or time window]({{< product-version-root >}}how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window/) to queue the existing buckets or bounded ranges. Monitor source discards, queue growth, sink errors, and destination request latency. Once delivery is healthy, configure scheduled checks with [Configure and schedule fullsync]({{< product-version-root >}}how-to/replication-and-reconciliation/configure-and-schedule-fullsync/). For two-way writes, configure the reverse queues and consumers as a separate relationship.

## Verify recovery

Compare known values and causal histories, including a deletion. Pause a sink, write during the pause, then resume and wait for delivery and a successful in-sync exchange. Keep a record of queue names, peers, scopes, and credentials for later incident diagnosis.
