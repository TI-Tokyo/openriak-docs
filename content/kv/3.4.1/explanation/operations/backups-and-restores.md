---
title: 'Backups and restores'
description: 'Explain backups and restores, including relevant state transitions, risks, and recovery assumptions.'
weight: 2
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
  - 'architects'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup-options'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain backups and restores, including relevant state transitions, risks, and recovery assumptions.

## Overview

### Backup options

Before considering backups, it is worth noting that as a distributed database there is no single commit position that represents a point of truth.  Therefore there is no way to effectively backup at a point, and restore to a point.  The overall state is eventually consistent.

- Riak is designed to operate as a resilient cluster, and also as a broader system of resilience from having multiple clusters that both replicate between each other and have continuous reconciliation to ensure they are in-sync.
- Major changes to the database will often occur in the application, not the database.  The application is in control of the data schema, and hence the migration of objects between schema versions.
- Self-healing is used to handle repair scenarios - i.e. recovering data from peers within the cluster, and the system is designed to perform predictably during the healing process.

Production users of Riak commonly have relatively lightweight backup and recovery strategies when compared to traditional database management systems; eventual consistency allows the global recovery of state without the need to focus on recovering state first back to a point in time.  In general, greater effort is placed into building the resilience of the system, and also the management of change within the application i.e. ensuring the application adopts lazy migration strategies for schema changes that don't require large point-in-time migration events.

If an individual node fails, do not restore an individual node from backup.  It is generally much more efficient and reliable to use [the `repair` process]({{< baseurl >}}kv/3.4.1/how-to/operate/replace-node/) to recover data on a node.  It is not normal practice to keep backups simply for the purpose of restoring individual nodes, even where those nodes may rely on ephemeral disks.

Note that in cloud environments, if an inefficient backup method is chosen (e.g. snapshots of block-service file-system volumes), then backup costs may consume a dominant proportion of overall Riak infrastructure costs.
