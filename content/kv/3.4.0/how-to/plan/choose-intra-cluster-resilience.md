---
title: 'Choose intra-cluster data resilience'
description: 'Show architects how to select replication and quorum settings for the required failure tolerance.'
weight: 4
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#data-distribution-guarantees'
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience'
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience---changing-the-choice'
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience---making-a-choice'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show architects how to select replication and quorum settings for the required failure tolerance.

## Before you begin

Access to the affected OpenRiak KV environment, the exact product version, a record of the current state, and a safe rollback plan.

## Overview

### Intra-cluster data resilience - making a choice

There are two primary aspects to data resilience within a cluster:

- [Configuring data distribution guarantees]({{< baseurl >}}kv/3.4.0/how-to/plan/choose-intra-cluster-resilience/);
- [Enabling proactive reconciliation]({{< baseurl >}}kv/3.4.0/explanation/replication/active-anti-entropy/).

Further guidance on the infrastructure requirements for a cluster, and the planning of cluster changes, can be found within the [guide to building and scaling a cluster]({{< baseurl >}}kv/3.4.0/how-to/plan/).

#### Data distribution guarantees

A OpenRiak cluster is a set of nodes (e.g. physical servers or virtual cloud instances), and the nodes within a cluster can be divided into separate locations (e.g. to represent physical racks, cloud placement groups, cloud availability zones or operator-defined maintenance groups).  Guarantees about the safety of data within a cluster can be set for both the nodes and the locations.

There are three configurable elements that control the resilience of the data distribution within a cluster:

- `n_val`; the replication value for the data items within the cluster, i.e how many copies of each object should exist within the cluster.  The `n_val` should preferably be set to the same value across all buckets.  The default `n_val` setting is 3, but in some circumstances this may be changed to 1 (e.g. backup clusters, or development environments) or 5 (e.g. for larger clusters looking to guarantee quorum reads in the presence of triple failures) - although in theory any positive integer value may be supported.
- `target_n_val`; the target for the distribution guarantee.  The `target_n_val` should always be consistently defined across nodes within a cluster.  The default setting is 4.  If the target is equal to the n_val, then all copies of the data stored within Riak in a healthy cluster will be guaranteed to be on separate nodes. If the target is greater than the n_val, then the integer difference represents how many failures can be tolerated before the guarantee is put at risk.
- `target_location_n_val`; the target for the distribution guarantee from the perspective of locations not nodes.  The `target_location_n_val` should always be consistently defined across nodes. This is normally set to 3.  When a `target_location_n_val` and `target_n_val` are both configured then the cluster change process will attempt to uphold both guarantees.

> The use of locations is optional within Riak, but may be useful even when the infrastructure has no physical distinction between nodes; as locations can also be used as a method for defining maintenance groups.  Maintenance groups are collections of nodes within a cluster which can be stopped or changed concurrently, as the loss of the whole group will only lead to the loss of one copy of the data.

The target `n_val` settings are used by the cluster claim algorithm, which is invoked [whenever a cluster change is planned]({{< baseurl >}}kv/3.4.0/how-to/operate/plan-and-commit-cluster-change/) (e.g. joining or leaving a node), to redistribute the vnodes around the cluster where required.  There are three usable versions of the cluster claim algorithm - versions 2, 3 and 4.  To use both `target_location_n_val` and `target_n_val` the cluster claim algorithm should be changed from version 2 (the default) to version 4.

To discover what combinations may be supported given a cluster (given a count of nodes and distribution of nodes around locations), then the [offline ring calculator](https://github.com/OpenRiak/ring_calculator) may be used, to test settings before planning them with version 4 of the algorithm.  The bigger the `target_n_val` and `target_location_n_val` chosen, the more efficient and resilient the eventual cluster setup will be.

> Failure to meet targets during cluster claim will lead to visual warnings when cluster change operations are requested - but not to failures.  If visual warnings are returned the ring calculator can be used to determine a supportable combination of settings.

#### Intra-cluster data resilience - changing the choice

The `n_val` is in theory configurable by bucket, which allows for multiple nvals to be used within the cluster.  However, each unique n_val will increase the overhead of running anti-entropy (anti-entropy comparisons are per n_val, and separate caches are required for each n_val), and the complexity of configuring inter-cluster reconciliation.  Once a `n_val` has been set on a bucket, there is no tested way of reducing it and converging on a clean state - other than replicating to a new cluster and transitioning between clusters.  Increasing the `n_val` should eventually converge into an expected state.

The `target_n_val` and `target_location_n_val` configuration is used each time a cluster change is planned (i.e. adding or removing a node).  So using a new value will take effect once the next change is made within a cluster.

Both anti-entropy mechanisms can be deployed in parallel to help with transition.  Enabling anti-entropy takes time to take effect (as caches are built).  Disabling it is immediate, although garbage collecting any legacy on-disk overhead is a manual operator task.

## Verify the result

Confirm the requested outcome, inspect cluster health and logs, and test the relevant client or operational path.
