---
title: 'Rebuild AAE trees from the command line'
description: 'Show operators how to request an AAE tree rebuild and monitor its status from the command line.'
weight: 31
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-and-controlling-aae---command-line'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to request an AAE tree rebuild and monitor its status from the command line.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Monitoring and Controlling AAE - Command Line

**Available from OpenRiak KV 3.4.0.**

Monitoring and control functions for Tictac AAE are available through the command line interface - `riak admin tictacaae --help`.

```console
riak admin tictacaae rebuildtick|exchangetick|maxresults|rangeboost [-n NODE] [VAL]
riak admin tictacaae rebuild-soon [-n NODE] [-p PARTITION] DELAY
riak admin tictacaae rebuild-now [-n NODE] [-p PARTITION]
riak admin tictacaae storeheads [-n NODE] [-p PARTITION] [VALUE]
riak admin tictacaae tokenbucket [-n NODE] [-p PARTITION] [VALUE]
riak admin tictacaae rebuild_schedule [-n NODE] [-p PARTITION] [RW RD]
riak admin tictacaae treestatus [--format table|json] [--show STATES]
```

Configuration control commands `rebuildtick`, `exchangetick`, `maxresults`, and `rangeboost` are simple set/show commands, reading and setting the corresponding environment variables. The changes are applied to the local node by default, or on another node if specified with option `-n`.

- The `exchangetick` alters the frequency of AAE activity, each vnode runs a tick, and each tick prompts an exchange.
- The `rebuildtick` alters the frequency with which a vnode will check to see if a rebuild is due;
  - The tick does not alter the actual frequency of rebuilds.
- Changes to `rebuildtick` and `exchangetick` will take effect on the next tick, impacting the size of the next-but-one tick.
  - Both the `rebuildtick` and `exchangetick` are set in milliseconds.
- The `maxresults` limit controls the scope of repairs per exchange (a limit on [the segment IDs covered by an exchange](/kv/3.4.0/explanation/replication/active-anti-entropy/)).
  - This is multiplied by the `rangeboost` if the exchange has been seeded with range information auto-discovered in previous exchanges.  For example if all deltas are in a certain modified date range.

> Do not set the value of the `exchangetick` or `rebuildtick` to a value lower than double the riak_core `vnode_inactivity_timeout`.  The default `vnode_inactivity_timeout` is 60s, so setting this to a value lower than `120000` milliseconds would be unsafe.

> If the number of segment IDs being checked within an AAE exchange are significantly over one thousand, then the acceleration associated with the restriction will tend towards zero.  So the combined value of `maxresults * rangeboost` should be kept to a value less than or equal to 1024.

Configuration control commands `storeheads`, `tokenbucket`, `rebuild_schedule` will extract or inject the actual relevant values from or to the state of the running AAE controller processes.

- Changing `storeheads` at runtime will also require a parallel store rebuild to take full effect.
- Care is required when setting the `rebuild_schedule` to use the correct units (hours for `wait` and seconds for `delay`).
- Disabling the `tokenbucket` protection is not recommended.

> It is recommended to control configuration through management of `riak.conf` not via the CLI.  The `riak admin tictacaae` commands should only be used when there is an urgent need to change the configuration on a running node, without requiring a restart.

The action command `rebuild-soon` will set the next rebuild time on all the nodes and vnodes specified, to the `delay` in seconds:

- A rebuild on a parallel-mode AAE vnode will rebuild the parallel keystore from the vnode store, and then rebuild the cached trees from that parallel store.
- A rebuild of a native vnode (i.e. with a single `leveled` backend), will rebuild the cached tree from the [leveled ledger](/kv/3.4.0/explanation/storage/leveled/) keystore (but also checking for presence of the object in the journal).
- Rebuilds are expensive processes: concurrent store rebuilds will be queued on the Best Endeavours [node worker pool](/kv/3.4.0/how-to/operate/monitor-worker-pools/), and tree rebuilds on the AF1 pool.
- After the delay has been set, the rebuild will not be triggered until the next `rebuildtick` on each vnode after the delay.
  - To immediately trigger a `rebuildtick` then use of the `rebuild-now` command is required after the `delay` has been changed.  `rebuild-now` only triggers a rebuild that is due, it will have no impact if a rebuild is not due (e.g. when `rebuild-soon` has not first been used).

The `treestatus` command will collect information from running AAE controllers and produce a report:

```console
                                        Partition ID      Status      Last Rebuild Date     Next Rebuild Date   Controller PID  Key Store Status
----------------------------------------------------  ----------  ---------------------  --------------------  ---------------  ----------------
   1004782375664995756265033322492444576013453623296     unbuilt                  never   2025-03-21T19:14:21       <0.2780.0>            native
                                                   0     unbuilt                  never   2025-03-23T04:59:09       <0.2296.0>            native
   1073290264914881830555831049026020342559825461248     unbuilt                  never   2025-03-16T14:05:43       <0.2763.0>            native
```

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
