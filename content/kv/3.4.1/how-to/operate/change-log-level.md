---
title: 'Change runtime log levels'
description: 'Show operators how to change runtime log levels with prechecks, verification, and recovery guidance.'
weight: 5
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\logging.md'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to change runtime log levels with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Enabling and Disabling Debug Logging

If you'd like to enable debug logging on the current node, i.e. set the
console log level to `debug`, you can do so without restarting the node
by accessing the Erlang console directly using the [`riak attach`](/kv/3.4.1/reference/commands/riak/#attach) command. Once you run this command and drop into the console, enter the following:

```erlang
lager:set_loglevel(lager_file_backend, "/var/log/riak/console.log", debug).
```

You should replace the file location above (`/var/log/riak/console.log`)
with your platform-specific location, e.g. `./log/console.log` for a
source installation. This location is specified by the
`log.console.file` parameter explained above.

If you'd like to enable debug logging on _all_ nodes instead of just one
node, you can enter the Erlang console of any running by running `riak
attach` and enter the following:

```erlang
rp(rpc:multicall(lager, set_loglevel, [lager_file_backend, "/var/log/riak/console.log", debug])).
```

As before, use the appropriate log file location for your cluster.

At any time, you can set the log level back to `info`:

```erlang
rp(rpc:multicall(lager, set_loglevel, [lager_file_backend, "/var/log/riak/console.log", info])).
```

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
