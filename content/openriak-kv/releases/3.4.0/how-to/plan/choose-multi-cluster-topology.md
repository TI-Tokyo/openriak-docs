---
title: 'Choose a multi-cluster topology'
description: 'Show architects how to choose between locations, multiple clusters, and replication topologies for resilience and scale.'
weight: 16
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
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#interconnecting-multiple-clusters'
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#interconnecting-multiple-clusters---making-a-choice'
tags: ['diataxis', 'kv', 'how-to', 'quickdocs']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show architects how to choose between locations, multiple clusters, and replication topologies for resilience and scale.

## Before you begin

Access to the affected OpenRiak KV environment, the exact product version, a record of the current state, and a safe rollback plan.

## Overview

### Interconnecting multiple clusters - making a choice

Riak clusters can be configured to replicate to other clusters, and further it is possible to continuously reconcile that the replication is correct (and prompt activity to resolve any deltas caused by replication failures).  Multiple clusters are generally used to:

- replicate into different physical locations to provide for disaster protection (e.g. between cloud regions, cloud providers, cloud availability zones, physical data centres, on and off-premises).
- provide clusters that support off-line usage of the data (e.g. reporting or backup), potentially with lower replication values (e.g. `n_val` of 1).
- replicate to additional clusters to provide for scale, or more efficient read activity in alternative locations.

The process of replication and reconciliation between the clusters is identical regardless of how multiple clusters are to be used.  An application cluster may consider two Riak clusters to be Active/Active, Active/Ready-Standby or Active/Passive; but these configurations must be managed in the broader system architecture as Riak clusters are by default Active/Active. Riak is an eventually consistent database, and as such does not by default prevent concurrent writes.  Concurrent updates will lead to multiple-values being retained, with default settings, and merging those values should be managed within the application.

It is possible to manage the potential for consistency issues [using conditional PUT logic (with token-based consensus)]({{< product-version-root >}}reference/http-api/conditional-requests/) that will block all but one of a concurrent update when the cluster is in a non-exceptional state.  However this control is only possible within a single cluster, there are no controls possible to block the creation of multi-value siblings when concurrent updates are allowed by the application into different clusters.

There are different design options available between using locations for resilience, and using multiple clusters.  For instance, in a cloud environment, potentially valid configurations for resilience would be:

- to deploy two clusters (`n_val` 3), one each in two separate availability zones, and a backup (`n_val` 1) cluster in a third availability zone - with locations aligned to placement groups for the nodes in the data-resilient clusters.  This provides the ability to switch the application between availability zones on failure without loss of resilience, and provides a total of 7 copies of the data all guaranteed to be in separate physical zones.
- to deploy a single cluster (`n_val` 5) spread across three availability zones (with locations aligned with availability zones).  This means that one cluster can be used to manage consistency (e.g. using conditional PUTs with token-based consensus), whilst guaranteeing there will always be at least two copies of the data available even if an entire Availability Zone is lost.  It would also be likely in this scenario that object GETs would generally not require the object value to traverse across availability zones (when using the leveled backend).
- to add to the above an additional cluster in an alternative cloud provider or cloud region.

Topologies of clusters are possible, but topologies are constrained in that it is not possible to forward updates through clusters; each cluster must subscribe to updates from every other cluster, so a full mesh is generally preferred.

When splitting a cluster across physical locations, it should be noted that the network latency between nodes will delay client response to both read and write requests.  The latency impact should not impact cluster throughput.  If there are network bandwidth costs between those physical locations, these costs will be minimised by running separate clusters in each location.  Using location definitions (for cluster claim) within a cluster will not be as optimal as separate clusters, but will reduce bandwidth costs for reads relative to configuring a multi-cluster without locations - as generally the local fetch will be preferred.

## Verify the result

Confirm the requested outcome, inspect cluster health and logs, and test the relevant client or operational path.
