---
title: 'Upgrade and downgrade behavior'
description: 'Explain upgrade and downgrade behavior, including relevant state transitions, risks, and recovery assumptions.'
weight: 7
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
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
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#upgrading-a-node'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain upgrade and downgrade behavior, including relevant state transitions, risks, and recovery assumptions.

## Overview

### Upgrading a node

Riak upgrades are all designed to support in-place rolling upgrades across the cluster - a [rolling restart]({{< baseurl >}}kv/3.4.0/how-to/operate/rolling-restart/) with a package deployment between the stop and start.

The following upgrade path has been specifically tested:

`2.2.3` -> `2.2.5` -> `2.9.n` -> `3.0.n` -> `3.2.n` -> `3.4.n`

More direct upgrade paths skipping steps may be possible.  New features are added using either a negotiation of capability within the cluster, or with the feature disabled by default in configuration.  Once a capability is mature, after at least two steps in the path, the negotiation may be retired and replaced with a static assumption of capability.

> When using the eleveldb backend with `snappy` compression (which is the default compression method when eleveldb is used in multi-backend setups), there are potentially multiple broken upgrade paths, even with minor release changes.  The release notes should be checked for issues before progressing with an update, and specific pre-live testing of any upgrade path is essential when using `snappy` compression.

It is not possible via rolling restart to upgrade from an OTP version 22 or prior, to an upgrade with an OTP version of 25 or higher.  For example, direct upgrades from `3.0.n` to `3.4.n` are not supported unless `3.0.n` is built with OTP 22, and `3.4.n` is built with OTP 24.

It is recommended to test all upgrades in pre-production environments.  If no pre-production environment is available, then a pilot node should be upgraded first in the cluster for an agreed time period (e.g. 24 hours).  If there are issues with the upgrade, then the pilot node can be stopped, cleared and [repaired]({{< baseurl >}}kv/3.4.0/how-to/operate/replace-node/).  Most large-scale production users of Riak rely on pre-production testing or pilot nodes to assure changes, and do not depend on a [backup/restore safety net]({{< baseurl >}}kv/3.4.0/explanation/operations/backups-and-restores/) during a rolling upgrade.

If local changes have been made to `riak.conf`, the package manager should leave the `riak.conf` file unchanged during an upgrade.  A release change may alter a default value in configuration, and if that default value was originally added to the `riak.conf` uncommented - the new default will not take effect following the upgrade, as the `riak.conf` is not altered.

> In configuration management of `riak.conf` files, the potential issue of changing defaults needs to be accounted for i.e. ensure the managed version of `riak.conf` is seeded with a new default `riak.conf` file produced for each release, before context-specific changes are applied.

As with other rolling operations, the operations can be accelerated through the use of locations, by changing a location per-cycle not just a node per-cycle.  Awaiting both the triggering and completion of handoffs between cycles is required for a smooth transition.
