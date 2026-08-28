---
title: 'Recover a failed node'
description: 'Show practitioners how to recover a failed node from evidence gathering through verification.'
weight: 7
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
  - 'developers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery\failed-node.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#completing-a-repair'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#reactive-replacement'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#replace-repair-and-recover'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show practitioners how to recover a failed node from evidence gathering through verification.

## Before you begin

The failing request or symptom, timestamps, relevant logs, and a recovery plan. Reproduce the issue safely before changing production state.

## Overview

### Recovering a Failed Node

#### General Recovery Notes

A OpenRiak node can fail for many reasons, but a handful of checks enable you to
uncover some of the most common problems that can lead to node failure,
such as checking for RAID and filesystem consistency or faulty memory and
ensuring that your network connections are fully functioning.

When a node fails and is then brought back into the cluster, make sure that it has the same node name that it did before it crashed. If the name has changed, the cluster will assume that the node is entirely new and that the crashed node is still part of the cluster.

During the recovery process, hinted handoff will kick in and update the data on
the recovered node with updates accepted from other nodes in the cluster. Your
cluster may temporarily return `not found` for objects that are currently
being handed off (see our page on [Eventual Consistency](../../../learn/concepts/eventual-consistency) for more details on
these scenarios, in particular how the system behaves while the failed node is
not part of the cluster).

#### Node Name Changed

If you are recovering from a scenario in which node name changes are out of
your control, you'll want to notify the cluster of its *new* name using the
following steps:

1. Stop the node you wish to rename:

```bash
    riak stop
    ```

2. Mark the node down from another node in the cluster:

```bash
    riak admin down <previous_node_name>
    ```

3. Update the node name in OpenRiak's configuration files:

```riakconf
    nodename = <updated_node_name>
    ```

```vmargs
    -name <updated_node_name>
    ```

4. Delete the ring state directory (usually `/var/lib/riak/ring`).

5. Start the node again:

```bash
    riak start
    ```

6. Ensure that the node comes up as a single instance:

```bash
    riak admin member-status
    ```

The output should look something like this:

```
    ========================= Membership ==========================
Status     Ring    Pending    Node
---------------------------------------------------------------
valid     100.0%      --      'dev-rel@127.0.0.1'
---------------------------------------------------------------
Valid:1 / Leaving:0 / Exiting:0 / Joining:0 / Down:0
    ```

7. Join the node to the cluster:

```bash
    riak admin cluster join <node_name_of_a_member_of_the_cluster>
    ```

8. Replace the old instance of the node with the new:

```bash
    riak admin cluster force-replace <previous_node_name> <new_node_name>
    ```

9. Review the changes:

```bash
    riak admin cluster plan
    ```

Finally, commit those changes:

```bash
    riak admin cluster commit
    ```

#### Replace, Repair and Recover

There are seven potential repair and recovery processes for handling different scenarios:

- [Proactive replacement]({{< baseurl >}}kv/3.4.0/how-to/operate/rolling-replacement/)
- [Reactive replacement]({{< baseurl >}}kv/3.4.0/how-to/operate/replace-node/)
- [Rolling replacement]({{< baseurl >}}kv/3.4.0/how-to/operate/rolling-replacement/)
- [Rolling restart]({{< baseurl >}}kv/3.4.0/how-to/operate/rolling-restart/)
- [Leveled backend repair]({{< baseurl >}}kv/3.4.0/how-to/operate/repair-leveled-store/)
- [Repairing a single vnode]({{< baseurl >}}kv/3.4.0/how-to/operate/repair-vnode/)
- [Repairing a key range]({{< baseurl >}}kv/3.4.0/how-to/operate/aae-fold/repair-key-range/)

The most common repair requirements are for proactive replace, and reactive replace: testing these processes under load prior to production deployment of Riak is recommended.

> All repair and replace operations are designed to be conducted under load.  In non-functional testing of Riak 3.4, an 8-node cluster is saturated with load (both Object API and Query API requests) to 100% CPU utilisation; and then a node is killed, cleared, re-joined and repaired under that load - with the target of never losing more 1/8th of the throughput.

#### Reactive Replacement

If a node temporarily fails, then recovers without a loss of historic delta; the node will automatically rejoin the cluster and have any delta in data patched via anti-entropy mechanisms, without the need for operator intervention.

If a node has failed following an incident, and all data on the node is lost, the cluster can still be recovered back to its previous state without requiring a backup of the failed node.

Recovery of such a lost node requires a reactive replacement.  There are three stages to replace and recover the node:

- [ensuring the node is downed]({{< baseurl >}}kv/3.4.0/how-to/operate/replace-node/);
- [forcing the replace]({{< baseurl >}}kv/3.4.0/how-to/operate/replace-node/);
- [repairing the new node]({{< baseurl >}}kv/3.4.0/how-to/troubleshoot/recover-failed-node/).

#### Completing a Repair

The data can then be recovered from the other nodes in the cluster issuing the `riak admin node repair start [-n NODE]` command.  This will prompt all vnodes which partially overlap the data held in the vnodes on the replacement node to race to play a role in repairing the node.  Each vnode will only repair the data which overlaps, filtering out any data that another vnode has already repaired (or is in the process of repairing).

**Available from OpenRiak KV 3.4.0.**To improve the performance of repair, the `repair_span` configuration in the [riak_core schema section of riak.conf](https://github.com/OpenRiak/riak_core/blob/openriak-3.4/priv/riak_core.schema) can be changed to `double_pair`, and this has been proven to be more effective when used with the leveled backend together with the enablement of the `repair_deferred` option in the [riak_kv schema section of riak.conf](https://github.com/OpenRiak/riak_kv/blob/openriak-3.4/priv/riak_kv.schema).

The combination of `repair_span = double_pair, repair_deferred = enabled` is significantly more effective when repairing under load.  With these configuration options, it should be noted that repairs will happen in key order, not in reverse order of receipt (the default).  With these changes, using the leveled backend, non-functional testing demonstrates that repairs can complete efficiently even when nodes are persistently at 100% CPU utilisation due to the handling of application requests.

Repair uses handoffs, and so can be tracked as with other cluster change operations.  Once handoffs are complete, Tictac AAE should be re-enabled, e.g. by using `riak_client:tictacaae_resume_node().`.  Once Tictac AAE confirms all vnodes are in-sync - then [`participate_in_coverage` can be re-enabled]({{< baseurl >}}kv/3.4.0/reference/operations/remote-console/).

The progress of repairs can be inspected with `riak admin node repair status`, and stopped with `riak admin node repair stop`.

## Verify the result

Repeat the original check, confirm that the symptom has cleared, and watch logs and service metrics long enough to detect recurrence.
