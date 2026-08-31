---
title: 'Restore an OpenRiak node'
description: 'Show operators how to restore an openriak node with prechecks, verification, and recovery guidance.'
weight: 13
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
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#leveled---restore-a-backup'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to restore an openriak node with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Leveled - restore a backup

If the database is stopped, and the contents of the `data/leveled` folders replaced by the content of the `data/backup` folders, then when Riak is restarted each vnode on each node will [rebuild the leveled ledger]({{< product-version-root >}}how-to/operate/repair-leveled-store/), as the ledger is not part of the backup. The cluster will then return to the same distributed consensus as when the backup was taken (given the constraint that the backup coverage plan took time to be distributed).

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
