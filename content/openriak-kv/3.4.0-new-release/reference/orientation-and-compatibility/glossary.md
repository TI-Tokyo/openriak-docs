---
title: Glossary
description: Definitions of terms used throughout OpenRiak KV. Each entry links to the relevant explanation or interface
  contract.
weight: 10
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- operators
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\glossary.md
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/foundations/glossary.md
related:
- foundations/overview/what-openriak-kv-is
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/data-and-consistency/objects-keys-and-buckets
---

Definitions of terms used throughout OpenRiak KV. Each entry links to the relevant explanation or interface contract.

## Active Anti-Entropy (AAE)

Background comparison and repair of replicas, including data that applications rarely read. See [Read repair and TicTac anti-entropy]({{< product-version-root >}}foundations/replication-and-repair/read-repair-and-tictac-anti-entropy/).

## Basho Bench

A historical configurable workload generator used for database benchmarking. See [Benchmark a representative workload]({{< product-version-root >}}how-to/performance/benchmark-a-representative-workload/).

## Bucket

A named namespace for keys, optionally within a bucket type. See [Objects, keys, and buckets]({{< product-version-root >}}foundations/data-and-consistency/objects-keys-and-buckets/).

## Bucket type

A named policy applied to buckets in its namespace. See [Bucket types and data policies]({{< product-version-root >}}foundations/data-and-consistency/bucket-types-and-data-policies/).

## Causal context

Opaque metadata describing the object versions a client has observed. See [Causality, version vectors, and siblings]({{< product-version-root >}}foundations/data-and-consistency/causality-version-vectors-and-siblings/).

## Cluster

A set of cooperating physical nodes sharing ownership and metadata. See [Rings, partitions, and virtual nodes]({{< product-version-root >}}foundations/cluster-architecture/rings-partitions-and-virtual-nodes/).

## Consistent hashing

Mapping keys and partition ownership into a ring to distribute data. See [Rings, partitions, and virtual nodes]({{< product-version-root >}}foundations/cluster-architecture/rings-partitions-and-virtual-nodes/).

## Data types

Structured replicated values updated through mergeable operations. See [Conflict-free replicated data types]({{< product-version-root >}}foundations/data-and-consistency/conflict-free-replicated-data-types/).

## Eventual consistency

Convergence of replicas when changes can propagate and conflicts are handled. See [Eventual consistency and convergence]({{< product-version-root >}}foundations/data-and-consistency/eventual-consistency-and-convergence/).

## Gossip

Exchange of cluster state between members. See [Membership, gossip, and handoff]({{< product-version-root >}}foundations/cluster-architecture/membership-gossip-and-handoff/).

## Hinted handoff

Transfer of updates held by temporary fallback replicas back to their intended owners. See [Membership, gossip, and handoff]({{< product-version-root >}}foundations/cluster-architecture/membership-gossip-and-handoff/).

## Key

The identifier of an object within its type and bucket namespace. See [Objects, keys, and buckets]({{< product-version-root >}}foundations/data-and-consistency/objects-keys-and-buckets/).

## Lager

An Erlang logging framework used by parts of the release and historical integrations. See [Logging and handler settings]({{< product-version-root >}}reference/configuration/logging-and-handler-settings/).

## Latch

An application coordination object managed with conditional updates. See [Conditional updates and latch objects]({{< product-version-root >}}foundations/data-and-consistency/conditional-updates-and-latch-objects/).

## MapReduce

A deprecated distributed job interface with map and reduce phases. See [MapReduce jobs and functions]({{< product-version-root >}}reference/legacy-and-experimental-features/mapreduce-jobs-and-functions/).

## Node

A running Erlang instance participating in the deployment. See [Rings, partitions, and virtual nodes]({{< product-version-root >}}foundations/cluster-architecture/rings-partitions-and-virtual-nodes/).

## Object

A key-addressed value with metadata and causal history, potentially containing siblings. See [Objects, keys, and buckets]({{< product-version-root >}}foundations/data-and-consistency/objects-keys-and-buckets/).

## Partition

A range of the ring owned and served through virtual nodes. See [Rings, partitions, and virtual nodes]({{< product-version-root >}}foundations/cluster-architecture/rings-partitions-and-virtual-nodes/).

## Quorum

An acknowledgement threshold derived from the configured replica policy. See [Quorums, availability, and durability]({{< product-version-root >}}foundations/data-and-consistency/quorums-availability-and-durability/).

## Read repair

Repair prompted when a read discovers differing replica states. See [Read repair and TicTac anti-entropy]({{< product-version-root >}}foundations/replication-and-repair/read-repair-and-tictac-anti-entropy/).

## Replica

One stored copy of an object under the placement policy. See [Replica placement and failure domains]({{< product-version-root >}}foundations/cluster-architecture/replica-placement-and-failure-domains/).

## Riak Core

The cluster infrastructure used for rings, membership, placement, and vnode management. See [Rings, partitions, and virtual nodes]({{< product-version-root >}}foundations/cluster-architecture/rings-partitions-and-virtual-nodes/).

## OpenRiak KV

The distributed key-value database documented here. See [What OpenRiak KV is]({{< product-version-root >}}foundations/overview/what-openriak-kv-is/).

## Riak Pipe

Infrastructure used by historical distributed processing paths, including MapReduce. See [MapReduce jobs and functions]({{< product-version-root >}}reference/legacy-and-experimental-features/mapreduce-jobs-and-functions/).

## Ring

The logical partition and ownership structure of a cluster. See [Rings, partitions, and virtual nodes]({{< product-version-root >}}foundations/cluster-architecture/rings-partitions-and-virtual-nodes/).

## Secondary index (2i)

Stored terms that let clients discover object keys by indexed values. See [Secondary indexes and projected attributes]({{< product-version-root >}}foundations/indexes-and-querying/secondary-indexes-and-projected-attributes/).

## Sibling

One of several concurrent content versions retained for an object. See [Causality, version vectors, and siblings]({{< product-version-root >}}foundations/data-and-consistency/causality-version-vectors-and-siblings/).

## Sloppy quorum

A request policy that can use fallback replicas when intended primaries are unavailable. See [Quorums, availability, and durability]({{< product-version-root >}}foundations/data-and-consistency/quorums-availability-and-durability/).

## Strong consistency

A stronger ordering guarantee than ordinary eventual-consistency requests; the ensemble interface has separate constraints. See [Conditional updates and latch objects]({{< product-version-root >}}foundations/data-and-consistency/conditional-updates-and-latch-objects/).

## Tombstone

Retained deletion evidence used to prevent older values from reappearing during repair. See [Deletion, tombstones, and expiration]({{< product-version-root >}}foundations/data-and-consistency/deletion-tombstones-and-expiration/).

## Value

The bytes or structured datatype state stored at an object address. See [Objects, keys, and buckets]({{< product-version-root >}}foundations/data-and-consistency/objects-keys-and-buckets/).

## Vector clock

A representation of causal history used by object operations. See [Causal-context and version-vector representations]({{< product-version-root >}}reference/data-model-contracts/causal-context-and-version-vector-representations/).

## Vnode

A virtual-node process serving a partition and its backend state. See [Rings, partitions, and virtual nodes]({{< product-version-root >}}foundations/cluster-architecture/rings-partitions-and-virtual-nodes/).
