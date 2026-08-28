---
title: 'Practice changing cluster membership'
description: 'Guide an operator through adding and removing disposable nodes while observing ring and handoff behavior.'
weight: 2
diataxis: 'tutorial'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'new-operators'
source_material:
  - 'legacy-3.2.5'
  - 'proposed-kv'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\ring-changes.md'
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\tutorials\add-remove-node.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\adding-removing-nodes.md'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Guide an operator through adding and removing disposable nodes while observing ring and handoff behavior.

## Adding / Removing Nodes

[use running cluster]: /kv/3.4.0/how-to/operate/

This page describes the process of adding and removing nodes to and from
an OpenRiak KV cluster. For information on creating a cluster check out [Running a Cluster][use running cluster].

### Start the Node

Just like the initial configuration steps, this step has to be repeated
for every node in your cluster. Before a node can join an existing
cluster it needs to be started. Depending on your mode of installation,
use either the init scripts installed by the Riak binary packages or
simply the script [`riak`](/kv/3.4.0/reference/commands/riak/):

```bash
/etc/init.d/riak start
```

or

```bash
bin/riak start
```

When the node starts, it will look for a cluster description, known as
the **ring file**, in its data directory. If a ring file does not exist,
it will create a new ring file based on the initially configured
`ring_size` (or `ring_creation_size` if you're using the older,
`app.config`-based configuration system), claiming all partitions for
itself. Once this process completes, the node will be ready to serve
requests.

#### Add a Node to an Existing Cluster

Once the node is running, it can be added to an existing cluster. Note
that this step isn't necessary for the first node; it's necessary only
for nodes that you want to add later.

To join the node to an existing cluster, use the `cluster join` command:

```bash
bin/riak admin cluster join <node_in_cluster>
```

The `<node_in_cluster>` in the example above can be _any_ node in the
cluster you want to join to. So if the existing cluster consists of
nodes `A`, `B`, and `C`, any of the following commands would join the
new node:

```bash
bin/riak admin cluster join A
bin/riak admin cluster join B
bin/riak admin cluster join C
```

To give a more realistic example, let's say that you have an isolated
node named `riak@192.168.2.5` and you want to join it to an existing
cluster that contains a node named `riak@192.168.2.2`. This command
would stage a join to that cluster:

```bash
bin/riak admin cluster join riak@192.168.2.2
```

If the join request is successful, you should see the following:

```
Success: staged join request for 'riak@192.168.2.5' to 'riak@192.168.2.2'
```

If you have multiple nodes that you would like to join to an existing
cluster, repeat this process for each of them.

#### Joining Nodes to Form a Cluster

The process of joining a cluster involves several steps, including
staging the proposed cluster nodes, reviewing the cluster plan, and
committing the changes.

After staging each of the cluster nodes with `riak admin cluster join`
commands, as in the section above, the next step in forming a cluster is
to review the proposed plan of changes. This can be done with the
`riak admin cluster plan` command, which is shown in the example below.

```
=============================== Staged Changes ================================
Action         Nodes(s)
-------------------------------------------------------------------------------
join           'riak@192.168.2.2'
join           'riak@192.168.2.2'
join           'riak@192.168.2.2'
join           'riak@192.168.2.2'
-------------------------------------------------------------------------------

NOTE: Applying these changes will result in 1 cluster transition

###############################################################################
                         After cluster transition 1/1
###############################################################################

================================= Membership ==================================
Status     Ring    Pending    Node
-------------------------------------------------------------------------------
valid     100.0%     20.3%    'riak@192.168.2.2'
valid       0.0%     20.3%    'riak@192.168.2.3'
valid       0.0%     20.3%    'riak@192.168.2.4'
valid       0.0%     20.3%    'riak@192.168.2.5'
valid       0.0%     18.8%    'riak@192.168.2.6'
-------------------------------------------------------------------------------
Valid:5 / Leaving:0 / Exiting:0 / Joining:0 / Down:0

Transfers resulting from cluster changes: 51
  12 transfers from 'riak@192.168.2.2' to 'riak@192.168.2.3'
  13 transfers from 'riak@192.168.2.2' to 'riak@192.168.2.4'
  13 transfers from 'riak@192.168.2.2' to 'riak@192.168.2.5'
  13 transfers from 'riak@192.168.2.2' to 'riak@192.168.2.6'
```

If the plan is to your liking, submit the changes by running `riak admin
cluster commit`.

**Note on ring changes**
The algorithm that distributes partitions across the cluster during membership
changes is non-deterministic. As a result, there is no optimal ring. In the
event that a plan results in a slightly uneven distribution of partitions, the
plan can be cleared. Clearing a cluster plan with `riak admin cluster clear`
and running `riak admin cluster plan` again will produce a slightly different
ring.

#### Removing a Node From a Cluster

A node can be removed from the cluster in two ways. One assumes that a
node is decommissioned, for example, because its added capacity is not
needed anymore or because it's explicitly replaced with a new one. The
second is relevant for failure scenarios in which a node has crashed and
is irrecoverable and thus must be removed from the cluster from another
node.

The command to remove a running node is `riak admin cluster leave`. This
command must be executed on the node that you intend to removed from the
cluster.

Similarly to joining a node, after executing `riak admin cluster leave`
the cluster plan must be reviewed with `riak admin cluster plan` and
the changes committed with `riak admin cluster commit`.

The other command is `riak admin cluster leave <node>`, where `<node>`
is the node name as specified in the node's configuration files:

```bash
riak admin cluster leave riak@192.168.2.1
```

This command can be run from any other node in the cluster.

Under the hood, both commands do basically the same thing. Running
`riak admin cluster leave <node>` selects the current node for you
automatically.

As with `riak admin cluster leave`, the plan to have a node leave the
cluster must be first reviewed with `riak admin cluster plan` and
committed with `riak admin cluster commit` before any changes will
actually take place.

#### Pausing a `join` or `leave`

**Warning**
Pausing may impact cluster health and is not recommended for more than a short period of time.

To pause during `riak admin cluster join` or `riak admin cluster leave`, set the node's transfer-limit to 0:

```bash
riak admin transfer-limit <node> 0
```

The above should produce the following output:

```
Set transfer limit for 'node' to 0
ok
```

## Ring Changes

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.

## Next steps

- [Practice changing a storage backend](/kv/3.4.0/tutorials/operations/change-storage-backend/)
