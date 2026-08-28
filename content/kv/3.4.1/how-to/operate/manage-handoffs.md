---
title: 'Monitor and manage handoffs'
description: 'Show operators how to monitor and manage handoffs with prechecks, verification, and recovery guidance.'
weight: 10
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\handoff.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---await-handoffs'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to monitor and manage handoffs with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Enabling and Disabling Handoff

OpenRiak KV provides a command-line interface for enabling and disabling handoff on the fly, without needing to set your configuration and restart the node. To
enable handoff:

```bash
riak admin handoff enable <inbound|outbound|both> <nodename>
```

You must specify two things when enabling handoff:

* whether you'd like to enable inbound handoff, outbound handoff, or
    both
* the node to be targeted by the command (or all nodes)

You can select a target node using either the `--node` or the `-n` flag.
You can select a direction by specifying `inbound`, `outbound`, or
`both`. The following equivalent commands would enable outbound handoff
on the node `riak3@100.0.0.1`:

```bash
riak admin handoff enable outbound --node riak3@100.0.0.1
riak admin handoff enable outbound -n riak3@100.0.0.1
```

These two equivalent commands would enable inbound handoff on the node
`riak5@100.0.0.1`:

```bash
riak admin handoff enable inbound --node riak5@100.0.0.1
riak admin handoff enable inbound -n riak5@127.0.0.1
```

Alternatively, you can enable handoff on all nodes at the same time
using either the `-a` or `--all` flag. This command would enable both
inbound and outbound handoff on all nodes:

```bash
riak admin handoff enable both --all
```

Which produces the following:

```
All nodes successfully updated
ok
```
As for enabling handoff, the `riak admin disable` command requires that
you specify both both a node or nodes to be targeted by the command and
whether you'd like to disable inbound handoff, outbound handoff, or
both. The `disable` command works just like `enable`. This command
would disable all forms of handoff on all nodes, to give just one
example:

```bash
riak admin handoff disable both --all
```

```
All nodes successfully updated
ok
```
#### Other Command-line Tools

In addition to enabling and disabling handoff, the
[`riak admin`]({{< baseurl >}}kv/3.4.1/reference/commands/riak-admin/) interface enables you to
retrieve a summary of handoff-related activity and other information.

##### summary

The `summary` command provides high-level information about active
handoffs in a cluster.

```bash
riak admin handoff summary
```

This will return a table that will provide the following information
about each node in your cluster:

Header | Description
:------|:-----------
`Node` | The name of the node
`Total` | Total number of active transfers throughout the entire cluster
`Ownership` | Total number of ownership exchanges
`Resize` | Total handoffs related to ring resizing operations (This should always be 0, as the Resize Ring feature has been deprecated)
`Hinted` | Total number of [hinted handoffs](../../reference/handoff#types-of-handoff)
`Repair` | Total repair-related handoffs. More information can be found [here](https://github.com/basho/riak_core/commit/036e409eb83903315dd43a37c7a93c9256863807).

##### details

This command provides information only about active transfers.
Note: In KV 3.2.5 + this command has been deprecated and no longer functions.

```bash
riak admin handoff details
```

If no transfers are currently underway, this command will output `No
ongoing transfers`. Otherwise, you will something like this:

##### config

This command displays the values for handoff-specific [configurable parameters]({{< baseurl >}}kv/3.4.1/reference/configuration/#intra-cluster-handoff) on each node in
the cluster, including:

* `transfer_limit`
* `handoff.outbound`
* `handoff.inbound`
* `handoff.port`

Descriptions of those parameters can be found in the sections above.

#### Join process - await handoffs

The pace of handoffs within the cluster, where there is a significant volume of data to handoff, is determined by the handoff concurrency limits.  There are two concurrency limits, the `cluster_transfer_limit` and the per-node `transfer_limit`.  Both limits must be lifted to achieve higher concurrent transfers.

When increasing the number of concurrent transfers, it is important to monitor the system for signs of stress related to transfers, such as the `backend_pause` log in the leveled backend.  In some cases, where the recipient node for a handoff cannot process the inbound data fast enough, the handoff will error and exit.  Following exit, when the handoff is re-scheduled it will re-commence from the start and resend all previous handoff work.  Avoiding handoff errors, and hence rework, is critical to overall transfer performance.

The `handoff_batch_threshold_count` may be reduced if handoff errors are occurring.  This controls the size of each handoff batch, and reducing the size of a batch should reduce the risk that a batch cannot be processed within the timeout.

Current handoff status can be tracked with `riak admin transfers` or `riak admin handoff details`, but real-time indexing of the `riak_core_handoff_sender` logs will provide a clearest picture of handoff activity.

There may be extreme scenarios where cluster changes require significant reshuffling to satisfy or optimise the cluster plan, especially with location awareness enabled.  In these cases many vnodes may be transferred as part of one change; and this may create a scenario where an individual node is receiving new vnode handoffs, but has yet been able (due to concurrency controls) release existing data to alternative nodes.

In these circumstances, if a node is under disk space pressure, inbound handoffs can be temporarily disabled, and then re-enabled once outbound handoffs have occurred: see `riak admin handoff --help`.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
