---
title: 'Repair an individual vnode'
description: 'Show operators how to identify, repair, and verify an unhealthy vnode.'
weight: 20
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
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#completing-a-repair'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#repair-an-individual-vnode'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to identify, repair, and verify an unhealthy vnode.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Completing a Repair

The data can then be recovered from the other nodes in the cluster issuing the `riak admin node repair start [-n NODE]` command.  This will prompt all vnodes which partially overlap the data held in the vnodes on the replacement node to race to play a role in repairing the node.  Each vnode will only repair the data which overlaps, filtering out any data that another vnode has already repaired (or is in the process of repairing).

**Available from OpenRiak KV 3.4.0.**To improve the performance of repair, the `repair_span` configuration in the [riak_core schema section of riak.conf](https://github.com/OpenRiak/riak_core/blob/openriak-3.4/priv/riak_core.schema) can be changed to `double_pair`, and this has been proven to be more effective when used with the leveled backend together with the enablement of the `repair_deferred` option in the [riak_kv schema section of riak.conf](https://github.com/OpenRiak/riak_kv/blob/openriak-3.4/priv/riak_kv.schema).

The combination of `repair_span = double_pair, repair_deferred = enabled` is significantly more effective when repairing under load.  With these configuration options, it should be noted that repairs will happen in key order, not in reverse order of receipt (the default).  With these changes, using the leveled backend, non-functional testing demonstrates that repairs can complete efficiently even when nodes are persistently at 100% CPU utilisation due to the handling of application requests.

Repair uses handoffs, and so can be tracked as with other cluster change operations.  Once handoffs are complete, Tictac AAE should be re-enabled, e.g. by using `riak_client:tictacaae_resume_node().`.  Once Tictac AAE confirms all vnodes are in-sync - then [`participate_in_coverage` can be re-enabled]({{< baseurl >}}kv/3.4.1/reference/operations/remote-console/).

The progress of repairs can be inspected with `riak admin node repair status`, and stopped with `riak admin node repair stop`.

#### Repair an individual vnode

Storage backends make use of CRC checks to detect and respond to corruption (by impacting individual objects not the whole store).  If an object, or a block of keys, becomes corrupted due to an issue with file storage then this should be detected by CRC checks.  The result of a failed CRC check, will be to respond as if the object in question is missing, rather than trigger a failure of the whole vnode.

Where such corruption is limited to a leveled ledger, then [a repair via leveled rebuild]({{< baseurl >}}kv/3.4.1/how-to/operate/repair-leveled-store/) can be used to recover.  However, in other backends, or with a corruption in the leveled journal - it may be preferable to repair a whole vnode rather than wait for other anti-entropy processes to eventually resolve the impact of the corruption (by repairing each impacted object).

The process to [complete a full node repair]({{< baseurl >}}kv/3.4.1/how-to/troubleshoot/recover-failed-node/) can be targeted at an individual vnode to repair just that vnode.  To prompt the repair of an individual vnode, the partition number - the [integer identifier of a vnode]({{< baseurl >}}kv/3.4.1/explanation/foundations/clusters-rings-and-partitions/) - must be passed to the vnode repair function.  The vnode repair function (`riak_kv_vnode_repair/1`) can be called by using the [`remote_console`]({{< baseurl >}}kv/3.4.1/how-to/operate/use-remote-console/) or directly from the command line through the `riak eval` CLI call:

```console
riak eval "riak_kv_vnode:repair(<partition_number>)."
```

The repair node will replace any object which the store does not presently hold.  However, following corruption, that validation may not be accurate and the store may incorrectly report presence.  So it is normally better to delete all the data on the vnode following corruption before triggering the repair.  Data will always be repaired eventually, deleting the store first ensures the time to repair is bounded and not dependent on long-running background recovery jobs.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
