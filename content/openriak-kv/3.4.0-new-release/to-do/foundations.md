---
title: 'Foundations'
description: 'Proposed Foundations structure: eight subsections and forty explanation pages.'
weight: 10
recommendations: true
product: 'OpenRiak KV'
product_version: '3.4.0'
---

Use Foundations for the [Explanation category in Diátaxis](https://diataxis.fr/explanation/): concepts, mechanisms, rationale, trade-offs, and the mental models readers need to understand OpenRiak KV 3.4.0.

This is the complete proposed Foundations structure: eight subsections and forty explanation pages, including retained, reorganised, and new coverage. Each table row names a proposed content page; each subsection also has a short orientation page. Link explanations to the corresponding task instructions, lookup details, and guided lessons.

## Proposed subsections and pages

| Section | Name | Explanation |
| --- | --- | --- |
| Overview | What OpenRiak KV is | Introduce the system's major components and the responsibilities shared between the database and the application. |
| Overview | Where OpenRiak fits | Explain suitable workloads, strengths, and trade-offs that make other workloads a poor fit. Consolidate “Why OpenRiak” and “Use cases”. |
| Overview | From Dynamo and Riak to OpenRiak | Explain the design's origins and evolution. Replace the lengthy reproduction of the Dynamo paper with an OpenRiak-focused explanation and links to the source material. |
| Cluster architecture | Rings, partitions, and virtual nodes | Explain data distribution and the distinction between logical partitions and physical nodes. Combine the overlapping ring and vnode explanations. |
| Cluster architecture | The lifecycle of a read and a write | Trace a request through the client, coordinator, replicas, storage, and response to establish a common mental model. |
| Cluster architecture | Replica placement and failure domains | Explain preference lists, primary and fallback replicas, placement constraints, and resilience to node or location failures. |
| Cluster architecture | Membership, gossip, and handoff | Explain how nodes learn about membership and how ownership and data move when a cluster changes. |
| Data and consistency | Objects, keys, and buckets | Explain the data model, object boundaries, metadata, and the consequences for application modelling. |
| Data and consistency | Bucket types and data policies | Explain namespaces, shared behaviour, and how bucket properties express data policies. |
| Data and consistency | Eventual consistency and convergence | Describe the promises, observable behaviour, and conditions required for convergence. |
| Data and consistency | Quorums, availability, and durability | Explain replication counts, read and write acknowledgements, primary requirements, and durable writes. Avoid implying that quorum settings alone provide strong consistency. |
| Data and consistency | Causality, version vectors, and siblings | Consolidate causal-context and vector explanations. Explain how the system distinguishes later changes from concurrent changes. |
| Data and consistency | Resolving concurrent updates | Explain application merging, last-write-wins policies, siblings, and information preservation. Consolidate the conflict-resolution and merge-strategy material. |
| Data and consistency | Conflict-free replicated data types | Explain convergence, supported operations, and the constraints on application semantics. |
| Data and consistency | Conditional updates and latch objects | Explain how these mechanisms reduce conflicts, their failure boundaries, and the limits of latch-based coordination. |
| Data and consistency | Deletion, tombstones, and expiration | Connect logical deletion, retention, reaping, expiration, and the risk of deleted data reappearing. Consolidate the two deletion explanations. |
| Indexes and querying | Secondary indexes and projected attributes | Explain index terms, application representations, projections, and the storage and write costs of indexing. |
| Indexes and querying | How distributed queries execute | Explain how scans, filters, combined queries, accumulation, and collation operate across virtual nodes. |
| Indexes and querying | Query consistency and snapshots | Explain index visibility, vnode snapshots, and the boundaries of consistency across a distributed query. |
| Indexes and querying | Query cost and result delivery | Explain selectivity, fan-out, buffering, pagination, and synchronous or asynchronous delivery. Consolidate query-performance material here. |
| Replication and repair | Read repair and TicTac anti-entropy | Explain divergence and the relationship between reactive and background repair. Maintain one current explanation of active anti-entropy. |
| Replication and repair | Replication sources, queues, and sinks | Explain the pipeline, object references, triggers, priorities, consumers, and backpressure. Consolidate the small component pages. |
| Replication and repair | Real-time replication and fullsync | Explain how the two mechanisms complement one another, including discovery, transport, and catching up after interruptions. |
| Replication and repair | Multi-cluster topologies and behaviour | Explain directional, active-active, and cascading arrangements, replication lag, concurrency, and metadata that remains local. |
| Replication and repair | Targeted reconciliation and AAE folds | Explain work bounded by bucket, key range, or time, and how it differs from full reconciliation. |
| Replication and repair | Replication generations and compatibility | Explain the architectural and migration differences between next-generation replication and legacy riak_repl v2/v3. |
| Storage and performance | Storage backend trade-offs | Provide a version-specific comparison of backend choices, distinguishing current recommendations from legacy behaviour. |
| Storage and performance | How Bitcask stores data | Explain append-only storage, the in-memory key directory, reads, merges, and resource implications. Link to separate configuration and maintenance procedures. |
| Storage and performance | How Leveled stores data | Explain the journal, ledger, caches, snapshots, and compaction, connecting them to read, write, and index behaviour. |
| Storage and performance | Multiple backends and prefix routing | Explain why data is routed to different backends and the implications of changing routing policies. |
| Storage and performance | Persistence, filesystems, and space reclamation | Explain buffering, persistence, filesystem behaviour, merges, and compaction. Distinguish storage reclamation from Erlang garbage collection. |
| Storage and performance | Latency, queues, and resource contention | Explain how vnode queues, Erlang scheduling, network and disk contention affect tail latency, overload, and recovery. |
| Storage and performance | Capacity and growth | Connect replicas, keys, values, indexes, caches, and recovery headroom to resource needs. Put sizing procedures in How-to. |
| Cluster lifecycle | Failure and recovery | Explain transient failures, failed nodes, lost storage, and the assumptions behind repair, replacement, and recovery. |
| Cluster lifecycle | Backups, restores, and disaster recovery | Explain what a distributed backup captures, its consistency limits, and the differences between backup, replication, and recovery. |
| Cluster lifecycle | Rolling maintenance and recovery headroom | Explain how taking nodes out of service affects availability, background work, and capacity. |
| Cluster lifecycle | Mixed versions, capabilities, and upgrade boundaries | Connect capability negotiation, mixed-version operation, activation, upgrade and downgrade boundaries, and rollback limits. |
| Security | Security boundaries and trust | Identify clients, administrators, nodes, and remote clusters, and explain which mechanisms protect each boundary. |
| Security | Identities, authentication, and permissions | Explain how users, groups, authentication sources, and permissions combine to make access decisions. |
| Security | TLS and certificate trust | Explain encryption, identity validation, and certificate trust relationships. |

## Content to correct or relocate

- Move the glossary to Reference and link to it from explanations.
- Give historical features, including MapReduce, legacy backends, and experimental strong consistency, explicit version and support context.
- Correct the mismatch in [Merge strategies]({{< product-version-root >}}foundations/data-model/merge-strategies/), whose existing body discusses untyped buckets.
- Replace the placeholder body in [Node failure and recovery]({{< product-version-root >}}foundations/operations/node-failure-and-recovery/).
- Consolidate the duplicated material in [Latency, throughput, and capacity]({{< product-version-root >}}foundations/performance/latency-throughput-and-capacity/) and [Storage and filesystem effects]({{< product-version-root >}}foundations/performance/storage-and-filesystem-effects/).
- Make each subsection landing page a short orientation with a suggested reading order.

## Defaults and reference details

Use the value shortcode whenever an explanation states a default. Use the defaults-table component for product reference tables, following the [Reference proposal](../reference/#reference-tables-and-default-values). Link to the [How-to proposal](../how-to/) and [Tutorials proposal](../tutorials/) for the corresponding tasks and guided lessons.
