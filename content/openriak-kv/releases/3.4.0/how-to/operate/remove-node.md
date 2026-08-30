---
title: 'Remove a node from a cluster'
description: 'Show operators how to remove a node from a cluster with prechecks, verification, and recovery guidance.'
weight: 11
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#shrinking-a-cluster'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to remove a node from a cluster with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Shrinking a cluster

Cluster changes to sharing a cluster require the staging of `leave` requests.  These plans may result in a two-phase transition plan - where in the first phase the leaving node simply offloads its vnodes to safe nodes (given the targets), and in the second phase the remaining nodes shuffle vnodes to ensure a better balance of load.

If the first phase creates an unsafe situation, where a remaining node has a higher proportion of the disk space than it can support, an alternative plan can be made by using the `full_rebalance_on_leave` configuration option.  With this option, a single-phase transition is planned based on an ideal plan for the new layout, and a broader shuffle will occur bypassing the first phase.  The `full_rebalance_on_leave` option should always be enabled when using `choose_claim_v4`.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
