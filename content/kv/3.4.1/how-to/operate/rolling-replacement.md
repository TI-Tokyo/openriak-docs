---
title: 'Perform a rolling node replacement'
description: 'Show operators how to perform a rolling node replacement with prechecks, verification, and recovery guidance.'
weight: 14
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery\rolling-replaces.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#proactive-replacement'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#rolling-replacement'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to perform a rolling node replacement with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Rolling Replaces

[upgrade]: {{< baseurl >}}kv/3.4.1/how-to/operate/upgrade-cluster/
[rolling restarts]: {{< baseurl >}}kv/3.4.1/how-to/operate/rolling-restart/
[add node]: {{< baseurl >}}kv/3.4.1/tutorials/operations/change-cluster-membership/

OpenRiak KV functions as a multi-node system, so cluster-level [version upgrades][upgrade] and [restarts][rolling restarts] can be performed on a node-by-node or *rolling* basis.

The following steps should be undertaken on each OpenRiak KV node that you wish to replace:

1\. Create a free node:

a\. [Create an additional node][add node] with similar specifications to the other nodes in the cluster.

b\. Or leave a node that is currently in the cluster:

```bash
  riak admin cluster leave »nodename«
  ```

After creating a node or leaving a node, wait for all transfers to complete:

```bash
  riak admin transfers
  ```

2\. Join the free node to your cluster:

```bash
riak admin cluster join »free_node«
```

3\. Next, replace the free node with an existing node:

```bash
riak admin cluster replace »free_node« »nodename«
```

4\. Then review the cluster transition plan:

```bash
riak admin cluster plan
```

5\. And commit the changes:

```bash
riak admin cluster commit
```

6\. Wait for all transfers to complete:

7\. Repeat steps 2-6 above until each node has been replaced.

8\. Join the replaced node back into the cluster or decommission the additional node that was created.

#### Proactive Replacement

It is possible to proactively replace a node in an OpenRiak cluster, for example if:

- a cloud provider intends to withdraw an instance;
- a hardware upgrade is required;
- to change the storage_backend of a cluster node-by-node;
- or to fully vacuum a node's storage backends of garbage.

A proactive replace is a cluster administration change, and [follows the standard five stage process described in the general guidance on amending the cluster make-up]({{< baseurl >}}kv/3.4.1/how-to/operate/add-node/).  In the case of a proactive replace, the first stage, staging, requires the staging of two changes:

- the `join` of a new node, and
- a `replace` to indicate the old node which should be replaced.

The plan should be planned, reviewed, committed and then monitored as with other changes.

The node cannot have its `location` set prior a `replace`, as the location must be ignored by the `replace` i.e. if the replacement node is in a different location to the existing node, this will not be factored in - the replace will transfer all vnodes to the new node, regardless of the `target_location_n_val` constraint.  Staging a location change after the `replace` has completed (i.e. following the `commit` and the transfers), may be used to `plan` a reshuffle of the cluster as a separate change activity.

See `riak admin cluster --help` for further details on the required inputs to cluster change commands.

During the replace operation the replacement node should have [`participate_in_coverage` disabled]({{< baseurl >}}kv/3.4.1/reference/operations/remote-console/), and have coverage support enabled only once all transfers have completed and (if configured) tictac anti-entropy has confirmed that all vnodes are in sync.

After completing a proactive replace operation, it may be necessary to realign node naming with design documents or monitoring systems; to rename a replacement node with the name of the node it replaced.  Once the replace operation is complete, it is possible to rename a node while it is down using `reip_manual` - see `riak admin reip_manual --help`.  The ring_directory is normally named `ring` in the platform data directory.  It will contain files such as `riak_core_ring.default.20221122164111`, where the middle term between the periods (in this case `default`) represents the required cluster name.

#### Rolling Replacement

A rolling replacement is an extension of the [proactive replacement]({{< baseurl >}}kv/3.4.1/how-to/operate/rolling-replacement/) process.  In a rolling replacement, a group of new nodes are installed.  There is then a rolling process where some nodes are proactively replaced by the new nodes; and once those replaced nodes are free - they are use to proactively replace other nodes in the cluster.

A proactive replacement should normally be done with a single node (i.e. a group of one), if location awareness is not configured.  If locations are enabled, then multiple nodes within each location can be safely subject to proactive replacement in the same cluster plan.  With location awareness the group of nodes used can be up to the minimum number of nodes within a location.

The same process can be followed for changing hardware in a cluster, except that the replacements are always made to new hardware (or cloud instance types) rather than recovered nodes.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
