---
title: 'Replace a failed node'
description: 'Show operators how to replace a failed node with prechecks, verification, and recovery guidance.'
weight: 12
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\replacing-node.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#administratively-downing-a-node'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#forcing-a-replace'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#reactive-replacement'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to replace a failed node with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Replacing a Node

At some point, for various reasons, you might need to replace a node in
your OpenRiak cluster (which is different from [recovering a failed node]({{< baseurl >}}kv/3.4.0/explanation/operations/node-failure-and-recovery/)). Here is the recommended way to go
about replacing a node.

1. Back up your data directory on the node in question. In this example
scenario, we'll call the node `riak4`:

```bash
    sudo tar -czf riak_backup.tar.gz /var/lib/riak /etc/riak
    ```

If you have any unforeseen issues at any point in the node
    replacement process, you can restore the node's data from this
    backup.

2. Download and install Riak on the new node you wish to bring into the
cluster and have it replace the `riak4` node. We'll call the new node
`riak7` for the purpose of this example.

3. Start the new `riak7` node with [`riak start`]({{< baseurl >}}kv/3.4.0/reference/commands/riak/):

```bash
    riak start
    ```

4. Plan the join of the new `riak7` node to an existing node already
participating in the cluster; for example `riak0` with the [`riak admin cluster join`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/#cluster) command executed on the new `riak7` node:

```bash
    riak admin cluster join riak0
    ```

5. Plan the replacement of the existing `riak4` node with the new
`riak7` node using the [`riak admin cluster replace`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/#cluster) command:

```bash
    riak admin cluster replace riak4 riak7
    ```

<div class="info">
    <div class="title">Single Nodes</div>
    If a node is started singly using default settings (as, for example,
    you might do when you are building your first test environment), you
    will need to remove the ring files from the data directory after you
    edit `/etc/vm.args`. `riak admin cluster replace` will not work as
    the node has not been joined to a cluster.
    </div>

6. Examine the proposed cluster changes with the [`riak admin cluster plan`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/#cluster) command executed on the new
`riak7` node:

```bash
    riak admin cluster plan
    ```

7. If the changes are correct, you can commit them with the
[`riak admin cluster commit`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/#cluster) command:

```bash
    riak admin cluster commit
    ```

If you need to clear the proposed plan and start over, use [`riak admin cluster clear`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/#cluster):

```bash
    riak admin cluster clear
    ```

Once you have successfully replaced the node, it should begin leaving
the cluster. You can check on ring readiness after replacing the node
with the [`riak admin ringready`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/#ringready)
and [`riak admin member-status`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/#member-status)
commands.

**Ring Settling**
You'll need to make sure that no other ring changes occur between the time
when you start the new node and the ring settles with the new IP info.

The ring is considered settled when the new node reports `true` when you run
the `riak admin ringready` command.

#### Reactive Replacement

If a node temporarily fails, then recovers without a loss of historic delta; the node will automatically rejoin the cluster and have any delta in data patched via anti-entropy mechanisms, without the need for operator intervention.

If a node has failed following an incident, and all data on the node is lost, the cluster can still be recovered back to its previous state without requiring a backup of the failed node.

Recovery of such a lost node requires a reactive replacement.  There are three stages to replace and recover the node:

- [ensuring the node is downed]({{< baseurl >}}kv/3.4.0/how-to/operate/replace-node/);
- [forcing the replace]({{< baseurl >}}kv/3.4.0/how-to/operate/replace-node/);
- [repairing the new node]({{< baseurl >}}kv/3.4.0/how-to/troubleshoot/recover-failed-node/).

#### Administratively Downing a Node

A node that is down, should not have a negative impact on the cluster.  There may be situations though, where a node is impaired, but that issue has not been automatically recognised, and so the node is not considered as down within the cluster.

The status of all nodes in the cluster, from the perspective of another node can be gained by running:

```console
riak admin cluster status
```

There are four states that a node can be considered to be in `up`, `down`, `up!` and `down!`.  The `!` indicates that the health-check status is unexpected given the administrative status - i.e. a node that is `down!` is not functioning as expected, but has not been marked as `down`.

If a node is known to be not operational, it should be marked as down using `riak admin down` from another node; and this should set the status of an unhealthy node to `down` not `down!`.

#### Forcing a Replace

When replacing a failed node, the situation differs depending on whether the new node is to be given the same IP address as the replaced node.  If the new (replacement) node has been built with the same address and naming it can be re-joined by re-staging a join, planning the change and committing it (which should lead to no actual transfers).  If the new node has a different configuration, then the plan will require a `join` and a `force_replace` operation to be staged.

If `force_replace` has been used, then the replacement node can be renamed at a later date using `riak admin reip_manual`.

The new node should be started with [`participate_in_coverage` disabled]({{< baseurl >}}kv/3.4.0/reference/operations/remote-console/), as it will at this stage be a full member of the cluster but have no data.  It is also more efficient to suspend anti-entropy until the repair is complete.

```console
riak eval "riak_client:tictacaae_suspend_node()."
riak eval "riak_client:remove_node_from_coverage()."
```

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
