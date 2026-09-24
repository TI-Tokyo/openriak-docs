---
title: From Dynamo and Riak to OpenRiak
description: OpenRiak continues the Riak family of distributed key/value databases. Its architecture carries forward
  Dynamo's partitioning, replication, and application-visible treatment of concurrent updates, while adding Riak
  and O
weight: 30
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- all-readers
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/#riak-history
tags:
- diataxis
- kv
- explanation
- quickdocs
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-23'
review_scope: Editorial & Technical review
review-by: TI Tokyo/JOM
restructured_from:
- foundations/foundations/history.md
- foundations/foundations/dynamo-model.md
related:
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/replication-generations-and-compatibility
- reference/orientation-and-compatibility/feature-status-and-deprecations
---

OpenRiak continues the Riak family of distributed key/value databases. Its architecture carries forward Dynamo's partitioning, replication, and application-visible treatment of concurrent updates, while adding Riak and OpenRiak implementations of those ideas.

## From a design to an implementation

Dynamo describes a design for a highly available distributed store. Riak applied related principles using Erlang processes, a partitioned ring, configurable request acknowledgements, and pluggable local storage. A Dynamo concept is useful background, but it is not a specification of an OpenRiak command, setting, or failure guarantee.

## OpenRiak today

OpenRiak develops the Riak codebase with current storage, anti-entropy, replication, and query capabilities. Leveled and TicTac anti-entropy are central to the newer storage and repair paths. Next-generation replication uses sources, queues, and sinks; older documentation about `riak_repl` describes a different, older replication implementation.

## Reading older material

Historical Riak examples can help explain the design, but package names, runtime compatibility, backend recommendations, and operational interfaces must be checked for the installed release. The compatibility reference separates current, legacy, and experimental features.

For the original design, see [Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf).
