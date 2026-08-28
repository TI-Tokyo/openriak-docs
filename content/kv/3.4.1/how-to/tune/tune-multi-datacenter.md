---
title: 'Tune multi-datacenter replication'
description: 'Show performance engineers how to tune multi-datacenter replication using measurable before-and-after checks.'
weight: 7
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'performance-engineers'
  - 'operators'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\performance\multi-datacenter-tuning.md'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show performance engineers how to tune multi-datacenter replication using measurable before-and-after checks.

## Before you begin

A representative workload, a recorded performance baseline, current capacity measurements, and a safe environment in which to test one change at a time.

## Overview

### System Tuning

[perf index]: {{< baseurl >}}kv/3.4.1/how-to/tune/

Depending on the size of your objects and your replication latency
needs, you may need to configure your kernel settings to optimize
throughput.

#### Linux

Refer to the [System Performance Tuning][perf index] document.

#### Solaris

On Solaris, the following settings are suggested:

```bash
/usr/sbin/ndd -set /dev/tcp tcp_ip_abort_interval 60000
/usr/sbin/ndd -set /dev/tcp tcp_keepalive_interval 900000
/usr/sbin/ndd -set /dev/tcp tcp_rexmit_interval_initial 3000
/usr/sbin/ndd -set /dev/tcp tcp_rexmit_interval_max 10000
/usr/sbin/ndd -set /dev/tcp tcp_rexmit_interval_min 3000
/usr/sbin/ndd -set /dev/tcp tcp_time_wait_interval 60000
/usr/sbin/ndd -set /dev/tcp tcp_max_buf 4000000
/usr/sbin/ndd -set /dev/tcp tcp_cwnd_max 4000000
/usr/sbin/ndd -set /dev/tcp tcp_xmit_hiwat 4000000
/usr/sbin/ndd -set /dev/tcp tcp_recv_hiwat 4000000
```

## Verify the result

Repeat the baseline workload and compare latency, throughput, resource use, and error rates before deciding whether to retain the change.
