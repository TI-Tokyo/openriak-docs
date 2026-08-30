---
title: 'Remote console reference'
description: 'List supported remote-console commands, arguments, return values, risks, and version applicability.'
weight: 11
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\runtime-interaction.md'
source_material:
  - 'legacy-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#remote-console'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#riak_client-remote_console-commands'
  - 'https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-the-remote-console'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

List supported remote-console commands, arguments, return values, risks, and version applicability.

## Details

### Runtime Interaction Reference

[config reference]: {{< product-version-root >}}reference/configuration/
[concept clusters]: {{< product-version-root >}}explanation/foundations/clusters-rings-and-partitions/

OpenRiak's [configuration files][config reference] provide a variety of parameters that
enable you to fine-tune how Riak interacts with two important elements
of the underlying operating system: distribution ports and OS
processes/garbage collection.

#### Ports

Distribution ports connect Riak nodes within a [cluster][concept clusters]. The
following port-related parameters are available:

* `runtime_health.triggers.distribution_port` - Whether distribution
  ports with full input buffers will be counted as busy.
  * Default: `on`
* `runtime_health.triggers.port` - Whether ports with full input
  buffers will be counted as busy. Ports can represent open files or network sockets.
  * Default: `on`
* `runtime_health.thresholds.busy_ports` - The threshold at which a
  warning will be triggered about the number of ports that are overly
  busy. Ports with full input buffers count toward this threshold.
  * Default: `2`

#### Processes

Riak will log warnings related to busy operating system processes and
garbage collection. You can specify the conditions in which warnings are
triggered using the following parameters:

* `runtime_health.thresholds.busy_processes` - The threshold at which
  a warning will be triggered about the number of processes that are
  overly busy. Processes with large heaps or that take a long time to
  garbage collect will count toward this threshold.
  * Default: `30`
* `runtime_health.triggers.process.heap_size` - A process will be
  marked as busy when its size exceeds this size (in bytes).
  * Default: `160444000`
* `runtime_health.triggers.process.garbage_collection` - A process
  will be marked as busy when it exceeds this amount of time doing
  garbage collection. Enabling this setting can cause performance
  problems on multi-core systems.
  * Default: `off`
  * Example when enabled: `50ms`
* `runtime_health.triggers.process.long_schedule` - A process will
  become busy when it exceeds this length of time during a single
  process scheduling and execution cycle.
  * Default: `off`
  * Example when enabled: `20ms`

#### Remote Console

Advanced information and debugging tools are available from the command line via `riak remote_console`.  This will attach a remote shell to the running node.  With this shell Erlang functions can be called as if on the local node, and this can be used for: [accessing objects]({{< product-version-root >}}how-to/operate/inspect-data/), [running AAE folds]({{< product-version-root >}}how-to/operate/aae-fold/run-from-command-line/), [access to specific administration commands]({{< product-version-root >}}reference/operations/remote-console/) as well as [advanced debugging and troubleshooting]({{< product-version-root >}}how-to/troubleshoot/erlang-vm/).

If an active remote_console session is detached in an unexpected way e.g. due to the network timeout of a SSH session over which the remote_console was run; "hanging" console process may be left running.  After a long period, a passive hanging console process may enter a loop and consume an entire CPU core.

It is good practice to monitor for the presence of long-lived hanging sessions, if `remote_console` is used.  Remote console sessions are distinguished with `ps -ef` by the `-progname` switch: Riak applications will have ``--progname <PATH>/bin/riak``; whereas `remote_console` sessions will have ``progname <path>/bin/erl``.

All single commands run from riak remote_console can be scripted from the command line using `riak eval`.  For example, to run the riak_client:repair_node() function from a script:

```console
riak eval "riak_client:repair_node()."
```

#### riak_client remote_console commands

The `riak_client` is an Erlang module within Riak that provides the internal API functions used by the external user-facing API.  The `riak_client` module also includes administration functions:

- `participate_in_coverage/1`, `remove_node_from_coverage/0`, `reset_node_for_coverage/0` - used to change the `participate_in_coverage` status of the node.  When a node is known to have a potential data issue (i.e. it is being recovered from a failure), it can be removed from coverage, and reset back into coverage once the data has been proven to be fully populated.
- `replrtq_reset_all_peers/1` - used to force all active and available nodes in the cluster to reset their peer discovery (used in real-time repl), to be used after adding a new node to a remote cluster.
- `replrtq_reset_all_workercounts/2` - used to force all active and available nodes to change their worker counts and per-peer limits, which may be required when a sink cluster cannot keep up fetching the remote replication traffic and so requires more sink workers (or sink workers per peer).

#### AAE Folds via the Remote Console

The AAE Fold API is accessible via `remote_console`.  Using the remote_console is an operator action, but it can be helpful when writing [Erlang functions](https://www.erlang.org/doc/readme.html) that take action based on AAE Folds.

To run an aae_fold via `remote_console`, a query definition is required and then that definition can be called using:

```erlang
FoldResult = riak_client:aae_fold(QueryDefinition).
```

The different inputs to an aae_fold are described in the specification:

```erlang
-type segment_filter() :: list(integer()).
-type tree_size() :: leveled_tictac:tree_size().
-type branch_filter() :: list(integer()).
-type key_range() :: {riak_object:key(), riak_object:key()}|all.
-type bucket() :: riak_object:bucket().
-type n_val() :: pos_integer().
-type riak_client_modified_range() ::
    {date, calendar:datetime(), calendar:datetime()}.
    %% If using riak_client:aae_fold/1 -
    %% will be auto-converted to modified_range().
-type modified_range() ::
    {date, non_neg_integer(), non_neg_integer()}.
-type hash_method() :: pre_hash|{rehash, non_neg_integer()}.
    %% Use pre_hash unless there is specific concern about hash collision
-type change_method() :: {job, pos_integer()}|local|count.
    %% Should generally just use count or local only
-type query_types() ::
    merge_root_nval|merge_branch_nval|fetch_clocks_nval|
    merge_tree_range|fetch_clocks_range|repl_keys_range|repair_keys_range|
    find_keys|object_stats|
    find_tombs|reap_tombs|erase_keys|
    list_buckets.

-type query_definition() ::
    {merge_root_nval, n_val()} |
    {merge_branch_nval, n_val(), branch_filter()} |
    {fetch_clocks_nval, n_val(), segment_filter()} |
    {fetch_clocks_nval, n_val(), segment_filter(), modified_range()} |
    {merge_tree_range, bucket(), key_range(), tree_size(), {segments, segment_filter(), tree_size()} | all, modified_range() | all, hash_method()} |
    {fetch_clocks_range, bucket(), key_range(), {segments, segment_filter(), tree_size()} | all, modified_range() | all} |
    {repl_keys_range, bucket(), key_range(), modified_range() | all, riak_kv_replrtq_src:queue_name()} |
    {repair_keys_range, bucket(), key_range(), modified_range() | all, all} |
    {find_keys, bucket(), key_range(), modified_range() | all, {sibling_count, pos_integer()}|{object_size, pos_integer()}} |
    {find_tombs, bucket(), key_range(), {segments, segment_filter(), tree_size()} | all, modified_range() | all} |
    {erase_keys, bucket(), key_range(), {segments, segment_filter(), tree_size()} | all, modified_range() | all, change_method()} |
    {reap_tombs, bucket(), key_range(), {segments, segment_filter(), tree_size()} | all, modified_range() | all, change_method()} |
    {object_stats, bucket(), key_range(), modified_range() | all} |
    {list_buckets, n_val()}.
```
