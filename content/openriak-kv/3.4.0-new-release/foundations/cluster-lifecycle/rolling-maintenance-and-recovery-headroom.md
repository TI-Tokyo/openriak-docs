---
title: Rolling maintenance and recovery headroom
description: Rolling maintenance keeps part of a cluster serving traffic while nodes are changed in stages. Its
  success depends on spare capacity and on waiting for recovery between stages.
weight: 360
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
- architects
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/operations/rolling-maintenance.md
related:
- foundations/cluster-architecture/replica-placement-and-failure-domains
- foundations/storage-and-performance/capacity-and-growth
- how-to/cluster-lifecycle/replace-nodes-without-stopping-the-cluster
- how-to/cluster-lifecycle/perform-a-rolling-restart
- how-to/data-inspection-and-repair/control-repair-impact-during-application-traffic
---

Rolling maintenance keeps part of a cluster serving traffic while nodes are changed in stages. Its success depends on spare capacity and on waiting for recovery between stages.

## A rolling change is a sequence

Stopping a node reduces the available placement and shifts requests to survivors. Restarting it restores a process, but handoff and repair may still be catching up. Starting the next stage too early can overlap those reduced-redundancy periods.

## Define a completion gate

A useful gate includes application health, membership state, relevant handoffs, replication and repair progress, and resource pressure. A service manager reporting “running” is insufficient on its own.

## Failure domains affect the sequence

Placement across locations can support maintenance strategies that account for a whole domain. That requires verified placement and enough surviving capacity; it is not permission to stop an arbitrary group of nodes together.

## Preserve room for an unexpected failure

Maintenance is not the only event the cluster may experience. A second failure, slow disk, or replication backlog can occur during a planned change. Size and schedule the operation so that the agreed application requirements still hold, and stop advancing if the completion gate fails.
