---
title: 'Perform a rolling restart'
description: 'Show operators how to perform a rolling restart with prechecks, verification, and recovery guidance.'
weight: 15
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery\rolling-restart.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#rolling-restart'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to perform a rolling restart with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Rolling Restarts

Because Riak functions as a multi-node system, cluster-level [Riak version upgrades]({{< product-version-root >}}how-to/operate/upgrade-cluster/) and restarts can be performed on a node-by-node, "rolling" basis.

The following steps should be undertaken on each OpenRiak node that you wish to restart:

1\. Stop Riak

```bash
riak stop
```

2\. Perform any necessary maintenance, upgrade, or other work in your cluster.

3\. Start Riak again

```bash
riak start
```

4\. Verify that the `riak_kv` service is once again available on the target node

```bash
riak admin wait-for-service riak_kv <nodename>
```

If this responds with `riak_kv is up`, then the service is available and you can move on to the next step. Otherwise, the console will periodically return `riak_kv is not up` until the service is available.

5\. Verify that all in-progress handoffs have been completed

```bash
riak admin transfers
```

If this responds with `No transfers active`, then all handoffs are complete. You can either run this command periodically until no more transfers are active or run the following script, which will run the `riak admin transfers` command every 5 seconds until the transfers are complete:

```bash
while ! riak admin transfers | grep -iqF 'No transfers active'
do
    echo 'Transfers in progress'
    sleep 5
done
```

6\. Repeat the above process for any other nodes that need to be restarted.

#### Rolling restart

A rolling restart may be required for some configuration changes, or as part of a Riak upgrade.  A stop and start of Riak will involve handoffs, just as with replacements.  The volume of data in those handoffs is minimal, just deltas received during the process - but it is important to wait for both the triggering and completion of handoffs before commencing the next batch of restart actions.

The configuration of locations may speed rolling restarts, as all nodes in a location can be safely stopped and started concurrently.

> Caution is required when performing a rolling restart when using the memory backend, as the pre-existing data is not transferred during the restart and is lost by the restart.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
