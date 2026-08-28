---
title: 'Configure the Leveled compaction window'
description: 'Show operators how to schedule Leveled compaction within an appropriate maintenance window.'
weight: 10
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#leveled-compaction-highlow-hour'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to schedule Leveled compaction within an appropriate maintenance window.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### leveled compaction high/low hour

The leveled backend is split into two parts:

- the Journal which like bitcask is generally an append-only file-based log of writes in the order they were received;
- the Ledger which stores only the keys index entries and object metadata; and is a log-structured merge tree, where immutable files are periodically merged and re-written to preserve an on-disk ordering of the keys by level.

The ledger compaction is continuous and the backend will enter a `slow offer` state if a backlog of compaction occurs due to excessive write activity.   When in this state, new writes will be slowed by pauses until the backend is up-to-date with its ledger compaction work.

The journal is generally immutable, but periodically compaction runs will be made which will compact a set of contiguous journal files, if the volume of space to be freed by that compaction is considered to be of sufficient value relative to the cost of the action.  Unlike the ledger compaction, the journal compaction is non-blocking; a backlog of compaction work will result in overuse of disk space, not a slowing of the storage system.

The leveled backend makes use of randomness to reduce the probability of overlapping compaction activity.  It is possible to configure a compaction window, however, all volume testing of Riak with a leveled backend is performed with continuous compaction activity.  The Journal compaction is relatively efficient and low-impact in comparison to bitcask merge - it is generally considered a safe practice to run compaction continuously throughout the day.

Although not necessary, the compaction high/low hour can be used to provide a window for compaction to take place, if required, such that either:

- journal compaction will take place at different times on different nodes (or locations) so that only a single replica for each partition is impacted by a concurrent journal compaction;
- journal compaction will take place outside of peak hours of database usage.

For information on configuring leveled journal compaction see the `journal.compaction` sections [within the leveled schema file](https://github.com/OpenRiak/leveled/blob/openriak-3.4/priv/leveled.schema).

Each compaction job will output a log with `log_ref=ic003` that gives the compaction score of the run of files which would yield the most benefit.  This score is calibrated so that `0.0` is the threshold for prompting compaction - greater than 0.0 and the benefit is considered sufficient.  If tracking these scores over time, if the scores are almost always `< 0.0`, then this is an indication that many of the compaction runs are unnecessary.  If the scores are consistently `> 0.0`, and especially if the scores are increasing over time - then more compaction runs will be required in the future to ensure there is efficient recovery of space in the store.

A backlog of compaction work within the ledger can be monitored by tracking leveled logs with `log_ref=p0024`.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
