---
title: Foundations
description: Implemented foundations page inventory and remaining verification.
weight: 10
recommendations: true
product: OpenRiak KV
product_version: 3.4.0
draft: true
hide_provenance: true
layout: single
---

The 40 planned topics have been moved into the current foundations structure and reviewed for their Diátaxis purpose. This inventory links to their current locations; it replaces the earlier proposal table.

## Current page locations

| Section | Page | Review focus |
| --- | --- | --- |
| Overview | [What OpenRiak KV is]({{< product-version-root >}}foundations/overview/what-openriak-kv-is/) | Introduce the system's major components and the responsibilities shared between the database and the application. |
| Overview | [Where OpenRiak fits]({{< product-version-root >}}foundations/overview/where-openriak-fits/) | Explain suitable workloads, strengths, and trade-offs that make other workloads a poor fit. Consolidate “Why OpenRiak” and “Use cases”. |
| Overview | [From Dynamo and Riak to OpenRiak]({{< product-version-root >}}foundations/overview/from-dynamo-and-riak-to-openriak/) | Explain the design's origins and evolution. Replace the lengthy reproduction of the Dynamo paper with an OpenRiak-focused explanation and links to the source material. |
| Cluster architecture | [Rings, partitions, and virtual nodes]({{< product-version-root >}}foundations/cluster-architecture/rings-partitions-and-virtual-nodes/) | Explain data distribution and the distinction between logical partitions and physical nodes. Combine the overlapping ring and vnode explanations. |
| Cluster architecture | [The lifecycle of a read and a write]({{< product-version-root >}}foundations/cluster-architecture/the-lifecycle-of-a-read-and-a-write/) | Trace a request through the client, coordinator, replicas, storage, and response to establish a common mental model. |
| Cluster architecture | [Replica placement and failure domains]({{< product-version-root >}}foundations/cluster-architecture/replica-placement-and-failure-domains/) | Explain preference lists, primary and fallback replicas, placement constraints, and resilience to node or location failures. |
| Cluster architecture | [Membership, gossip, and handoff]({{< product-version-root >}}foundations/cluster-architecture/membership-gossip-and-handoff/) | Explain how nodes learn about membership and how ownership and data move when a cluster changes. |
| Data and consistency | [Objects, keys, and buckets]({{< product-version-root >}}foundations/data-and-consistency/objects-keys-and-buckets/) | Explain the data model, object boundaries, metadata, and the consequences for application modelling. |
| Data and consistency | [Bucket types and data policies]({{< product-version-root >}}foundations/data-and-consistency/bucket-types-and-data-policies/) | Explain namespaces, shared behaviour, and how bucket properties express data policies. |
| Data and consistency | [Eventual consistency and convergence]({{< product-version-root >}}foundations/data-and-consistency/eventual-consistency-and-convergence/) | Describe the promises, observable behaviour, and conditions required for convergence. |
| Data and consistency | [Quorums, availability, and durability]({{< product-version-root >}}foundations/data-and-consistency/quorums-availability-and-durability/) | Explain replication counts, read and write acknowledgements, primary requirements, and durable writes. Avoid implying that quorum settings alone provide strong consistency. |
| Data and consistency | [Causality, version vectors, and siblings]({{< product-version-root >}}foundations/data-and-consistency/causality-version-vectors-and-siblings/) | Consolidate causal-context and vector explanations. Explain how the system distinguishes later changes from concurrent changes. |
| Data and consistency | [Resolving concurrent updates]({{< product-version-root >}}foundations/data-and-consistency/resolving-concurrent-updates/) | Explain application merging, last-write-wins policies, siblings, and information preservation. Consolidate the conflict-resolution and merge-strategy material. |
| Data and consistency | [Conflict-free replicated data types]({{< product-version-root >}}foundations/data-and-consistency/conflict-free-replicated-data-types/) | Explain convergence, supported operations, and the constraints on application semantics. |
| Data and consistency | [Conditional updates and latch objects]({{< product-version-root >}}foundations/data-and-consistency/conditional-updates-and-latch-objects/) | Explain how these mechanisms reduce conflicts, their failure boundaries, and the limits of latch-based coordination. |
| Data and consistency | [Deletion, tombstones, and expiration]({{< product-version-root >}}foundations/data-and-consistency/deletion-tombstones-and-expiration/) | Connect logical deletion, retention, reaping, expiration, and the risk of deleted data reappearing. Consolidate the two deletion explanations. |
| Indexes and querying | [Secondary indexes and projected attributes]({{< product-version-root >}}foundations/indexes-and-querying/secondary-indexes-and-projected-attributes/) | Explain index terms, application representations, projections, and the storage and write costs of indexing. |
| Indexes and querying | [How distributed queries execute]({{< product-version-root >}}foundations/indexes-and-querying/how-distributed-queries-execute/) | Explain how scans, filters, combined queries, accumulation, and collation operate across virtual nodes. |
| Indexes and querying | [Query consistency and snapshots]({{< product-version-root >}}foundations/indexes-and-querying/query-consistency-and-snapshots/) | Explain index visibility, vnode snapshots, and the boundaries of consistency across a distributed query. |
| Indexes and querying | [Query cost and result delivery]({{< product-version-root >}}foundations/indexes-and-querying/query-cost-and-result-delivery/) | Explain selectivity, fan-out, buffering, pagination, and synchronous or asynchronous delivery. Consolidate query-performance material here. |
| Replication and repair | [Read repair and TicTac anti-entropy]({{< product-version-root >}}foundations/replication-and-repair/read-repair-and-tictac-anti-entropy/) | Explain divergence and the relationship between reactive and background repair. Maintain one current explanation of active anti-entropy. |
| Replication and repair | [Replication sources, queues, and sinks]({{< product-version-root >}}foundations/replication-and-repair/replication-sources-queues-and-sinks/) | Explain the pipeline, object references, triggers, priorities, consumers, and backpressure. Consolidate the small component pages. |
| Replication and repair | [Real-time replication and fullsync]({{< product-version-root >}}foundations/replication-and-repair/real-time-replication-and-fullsync/) | Explain how the two mechanisms complement one another, including discovery, transport, and catching up after interruptions. |
| Replication and repair | [Multi-cluster topologies and behaviour]({{< product-version-root >}}foundations/replication-and-repair/multi-cluster-topologies-and-behaviour/) | Explain directional, active-active, and cascading arrangements, replication lag, concurrency, and metadata that remains local. |
| Replication and repair | [Targeted reconciliation and AAE folds]({{< product-version-root >}}foundations/replication-and-repair/targeted-reconciliation-and-aae-folds/) | Explain work bounded by bucket, key range, or time, and how it differs from full reconciliation. |
| Replication and repair | [Replication generations and compatibility]({{< product-version-root >}}foundations/replication-and-repair/replication-generations-and-compatibility/) | Explain the architectural and migration differences between next-generation replication and legacy riak_repl v2/v3. |
| Storage and performance | [Storage backend trade-offs]({{< product-version-root >}}foundations/storage-and-performance/storage-backend-trade-offs/) | Provide a version-specific comparison of backend choices, distinguishing current recommendations from legacy behaviour. |
| Storage and performance | [How Bitcask stores data]({{< product-version-root >}}foundations/storage-and-performance/how-bitcask-stores-data/) | Explain append-only storage, the in-memory key directory, reads, merges, and resource implications. Link to separate configuration and maintenance procedures. |
| Storage and performance | [How Leveled stores data]({{< product-version-root >}}foundations/storage-and-performance/how-leveled-stores-data/) | Explain the journal, ledger, caches, snapshots, and compaction, connecting them to read, write, and index behaviour. |
| Storage and performance | [Multiple backends and prefix routing]({{< product-version-root >}}foundations/storage-and-performance/multiple-backends-and-prefix-routing/) | Explain why data is routed to different backends and the implications of changing routing policies. |
| Storage and performance | [Persistence, filesystems, and space reclamation]({{< product-version-root >}}foundations/storage-and-performance/persistence-filesystems-and-space-reclamation/) | Explain buffering, persistence, filesystem behaviour, merges, and compaction. Distinguish storage reclamation from Erlang garbage collection. |
| Storage and performance | [Latency, queues, and resource contention]({{< product-version-root >}}foundations/storage-and-performance/latency-queues-and-resource-contention/) | Explain how vnode queues, Erlang scheduling, network and disk contention affect tail latency, overload, and recovery. |
| Storage and performance | [Capacity and growth]({{< product-version-root >}}foundations/storage-and-performance/capacity-and-growth/) | Connect replicas, keys, values, indexes, caches, and recovery headroom to resource needs. Put sizing procedures in How-to. |
| Cluster lifecycle | [Failure and recovery]({{< product-version-root >}}foundations/cluster-lifecycle/failure-and-recovery/) | Explain transient failures, failed nodes, lost storage, and the assumptions behind repair, replacement, and recovery. |
| Cluster lifecycle | [Backups, restores, and disaster recovery]({{< product-version-root >}}foundations/cluster-lifecycle/backups-restores-and-disaster-recovery/) | Explain what a distributed backup captures, its consistency limits, and the differences between backup, replication, and recovery. |
| Cluster lifecycle | [Rolling maintenance and recovery headroom]({{< product-version-root >}}foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom/) | Explain how taking nodes out of service affects availability, background work, and capacity. |
| Cluster lifecycle | [Mixed versions, capabilities, and upgrade boundaries]({{< product-version-root >}}foundations/cluster-lifecycle/mixed-versions-capabilities-and-upgrade-boundaries/) | Connect capability negotiation, mixed-version operation, activation, upgrade and downgrade boundaries, and rollback limits. |
| Security | [Security boundaries and trust]({{< product-version-root >}}foundations/security/security-boundaries-and-trust/) | Identify clients, administrators, nodes, and remote clusters, and explain which mechanisms protect each boundary. |
| Security | [Identities, authentication, and permissions]({{< product-version-root >}}foundations/security/identities-authentication-and-permissions/) | Explain how users, groups, authentication sources, and permissions combine to make access decisions. |
| Security | [TLS and certificate trust]({{< product-version-root >}}foundations/security/tls-and-certificate-trust/) | Explain encryption, identity validation, and certificate trust relationships. |

## Remaining verification

Check the explanations with a newcomer and an experienced operator. Confirm that the short examples preserve the distinctions between replica placement, quorums, causal context, and formal consistency.

Use [For Review]({{< product-version-root >}}to-do/for-review/) for per-page technical review status. The machine-readable source-to-destination map is retained in `notes/reports/diataxis-page-map.json`.
