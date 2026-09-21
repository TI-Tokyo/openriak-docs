---
title: Fullsync requests and results
weight: 990
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: TicTac fullsync requests select a comparison between the configured local and remote datasets. A request
  can report agreement, identify repair work, or fail before establishing agreement.
related:
- reference/configuration/next-generation-replication-settings
- reference/replication-interfaces/next-generation-replication-runtime-controls
- reference/operations-and-observability/aae-repair-and-worker-pool-metrics
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- foundations/replication-and-repair/real-time-replication-and-fullsync
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
---

TicTac fullsync requests select a comparison between the configured local and remote datasets. A request can report agreement, identify repair work, or fail before establishing agreement.

## Client entry point

{{< cli-command key="erlang:riak_client:ttaaefs_fullsync" >}}

## Selection and scheduling

The generated fullsync settings define dataset scope, peer transport, local and remote replica counts, queue names, schedules, and limits. Runtime range overrides and pause/resume controls are listed with the next-generation runtime interfaces.

## Interpreting results

A dispatched request is not evidence that the comparison completed. Inspect its returned result and the associated fullsync metrics and logs. A repair count describes work identified or submitted by that exchange; verify convergence through subsequent comparisons and representative data checks.
