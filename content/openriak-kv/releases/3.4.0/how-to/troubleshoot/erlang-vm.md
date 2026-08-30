---
title: 'Troubleshoot through the Erlang virtual machine'
description: 'Show advanced operators how to use Recon, microstate accounting, Eprof, and tracing during diagnosis.'
weight: 13
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#advanced---troubleshoot-via-the-erlang-vm'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#eprof'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#microstate-accounting'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#recon'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#tracing-with-dbg'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show advanced operators how to use Recon, microstate accounting, Eprof, and tracing during diagnosis.

## Before you begin

The failing request or symptom, timestamps, relevant logs, and a recovery plan. Reproduce the issue safely before changing production state.

## Overview

### Advanced - troubleshoot via the Erlang VM

For more advanced troubleshooting, [the `remote_console`]({{< product-version-root >}}how-to/operate/use-remote-console/) can be used to access specialist troubleshooting tools.

#### Recon

Riak 3.4 includes the recon library, which is primarily useful for troubleshooting memory issues within the Erlang VM.  For guidance on using the library see the [documentation](https://ferd.github.io/recon/overview.html) and the [related book](https://www.erlang-in-anger.com/).

Note that Riak 3.4 uses an OTP version that will free memory from shared carriers using `MADV_FREE` not `MADV_DONTNEED`; and this may lead to false reporting of memory usage of the `beam` by the operating system - some kernel stats packages may not report `MADV_FREE` memory as having been returned until it is required to use it, creating the misleading impression of a memory leak.  Check kernel documentation to be clear on how to correctly monitor when systems use `MADV_FREE`.  [Future Riak versions will switch to enforcing `MADV_DONTNEED`](https://github.com/OpenRiak/riak/issues/20).

The [riak_kv_util module](https://github.com/OpenRiak/riak_kv/blob/openriak-3.4/src/riak_kv_util.erl) also supports some functions helpful for memory analysis, and these functions may be called via `remote_console`:

- `top_n_binary_total_memory/1`
- `summarise_binary_memory_by_initial_call/1`
- `top_n_process_total_memory/1`
- `summarise_process_memory_by_initial_call/1`

All these functions take a single argument N (the N in Top N), though the `summarise` functions can also be directly passed the output of the related top_n function, so that a recalculation of the Top N is not required.

#### Microstate accounting

To examine the spread of CPU-related work by scheduler (there should be one standard erlang scheduler for each CPU core), microstate accounting may be used.  The [erlang documentation](https://www.erlang.org/doc/apps/runtime_tools/msacc.html) gives basic information on analysing the output, but note that the functionality of microstate accounting may vary significantly between OTP releases.

To alter the configuration on the Erlang VM to adjust the operation of schedulers, see the `erlang.schedulers` options within the [Riak schema file](https://github.com/OpenRiak/riak/blob/openriak-3.4/priv/riak.schema).  It is recommended to seek expert advice, and run realistic performance test exercises before adjusting any default settings.

#### Eprof

Within the Riak development process testing with eprof profiling is enabled to discover on which functions CPU is used.  For more information on [eprof see the erlang documentation](https://www.erlang.org/doc/apps/tools/eprof.html).  There exists a helper function in the [riak_kv_util module](https://github.com/OpenRiak/riak_kv/blob/openriak-3.4/src/riak_kv_util.erl) `profile_riak/1` which takes an argument N ms, and will profile riak for N ms.

Note with eprof:

- Riak, especially with the leveled backend, uses a huge amount of (lightweight Erlang) processes both temporary and permanent.  Profiling over all processes may fail, especially when profiling for longer periods.
- There may be measurement effects when profiling functions which respond per call in `< 0.1 microseconds` (i.e. the impact of the function call may be proportionally inflated by the cost of measurement).
- Profiling may record the time spent waiting in receive loops as processing time (e.g. `gen_server:loop/7` may appear to have a processing overhead which is in fact mainly wait time).

#### Tracing with dbg

Erlang has a [tracing utility](https://www.erlang.org/doc/apps/runtime_tools/dbg_guide) which may be useful for tracing function calls within a system, and to understand the path taken to reach certain function calls.

Note that the output from running `dbg` will by default be sent to `erlang.log` files and potentially write a huge volume of information to these log files very rapidly.  When indexing log files, this may impact licensing and CPU constraints in the indexing system.

## Verify the result

Repeat the original check, confirm that the symptom has cleared, and watch logs and service metrics long enough to detect recurrence.
