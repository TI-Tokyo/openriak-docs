---
title: 'Run a routine operations checklist'
description: 'Show operators how to perform a repeatable health and maintenance review of an OpenRiak cluster.'
weight: 44
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
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#operation-checklist'
tags: ['diataxis', 'kv', 'how-to', 'quickdocs']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to perform a repeatable health and maintenance review of an OpenRiak cluster.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Operation Checklist

In the guide to building and scaling a cluster, the section on [choosing infrastructure]({{< product-version-root >}}how-to/plan/size-cluster/) provides a checklist of things to consider at the design stage, and it is worth considering the issues highlighted in that guide when troubleshooting operational issues:

- The need to avoid the accidental concurrent scheduling of expensive operational processes;
  - Disk trim jobs,
  - Software RAID integrity checks,
  - Security software sweeps.
- Other than operational tools, Riak should be the only software running on a node;
  - By default in Riak, Erlang schedulers are not pinned to CPU cores, but software consuming an entire core can still cause variation in performance.
- Subtle network issues may occur in distributed systems below network bandwidth limits;
  - TCP TIME_WAIT delays leading to port exhaustion and 1s, 3s or 5s SYN connection delays,
  - TCP slow-start triggered by packet loss related to Incast and buffer overflows.
- HTTP limits on request and response header sizes, and character usage may exist throughout the software stack;
  - In application HTTP clients and also in proxies.
- Avoid operating-system optimisations that may cause periodic spikes in activity related to garbage collection or realignment;
  - `transparent_huge_pages` should be disabled to avoid unpredictable resource consumption.

Monitoring of activity related to these issues is important.  Further, it is vital to monitor the key infrastructure limits relevant to Riak environments.

- All critical space limits must be proactively monitored, to react when within 20% of thresholds:
  - Disk space.
  - Memory used by the Riak process,
    - Low thresholds for memory should be used because of the value in over-provisioning memory, and the possibility for large requests to trigger volatile changes in memory demand.
  - Open file descriptors.
- Limits on the Erlang Virtual Machine should be monitored
  - **Available from OpenRiak KV 3.4.1.**The [Riak stats endpoint]({{< product-version-root >}}reference/operations/statistics-and-monitoring/) directly reports the percentage utilisation of key virtual machine statistics.
    - `vm_proc_percent` - controlled via the hidden configuration option `erlang.process_limit` in `riak.conf`. The underlying numbers are reported in `vm_proc_count` and `vm_proc_limit`.  The number of processes will expand with the size of the store in keys per-node - in particular when using the leveled backend - so the limit may require reconfiguration as nodes vertically scale.
    - Also tracked are the hard limits on ports (`vm_port_percent`) and atoms (`vm_atom_percent`), and the soft limit on ETS tables (`vm_ets_percent`).  These numbers should not normally increase significantly as the key count expands.
- Infrastructure utilisation limits should be monitored for trends that cluster expansion is required, due to repeated breaches of thresholds in:
  - Interface bandwidth.
  - CPU utilisation.
  - Disk I/O operations (especially when I/O is limited by cloud providers).
  - Disk `await` times.

> The thresholds for monitoring may vary depending on the speed with which new nodes can be procured, initialised and deployed to.

Riak should be deployed into consistent environments using automation where possible:

- When building Riak, the local SSL library will be used to provide support for TLS security;
  - Consistency of environments between packaging and deployment is important.
- The `riak.conf` file should be under configuration control;
  - the version in configuration management should be updated afresh when Riak is upgraded, to ensure the deployed version reflects new defaults.
- Bucket properties need to be consistent across clusters, and so may be managed through automated configuration.

Automation of Riak operations is recommended where possible.  However, care must be taken to ensure operational scripts wait for node transfers to complete when performing changes - and this must account for the fact that handoffs may not trigger immediately.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
