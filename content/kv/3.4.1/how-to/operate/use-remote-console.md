---
title: 'Use the remote console'
description: 'Show operators how to enter the remote console and perform supported diagnostic operations safely.'
weight: 21
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
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#remote-console'
  - 'https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-the-remote-console'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to enter the remote console and perform supported diagnostic operations safely.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Remote Console

Advanced information and debugging tools are available from the command line via `riak remote_console`.  This will attach a remote shell to the running node.  With this shell Erlang functions can be called as if on the local node, and this can be used for: [accessing objects]({{< baseurl >}}kv/3.4.1/how-to/operate/inspect-data/), [running AAE folds]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/run-from-command-line/), [access to specific administration commands]({{< baseurl >}}kv/3.4.1/reference/operations/remote-console/) as well as [advanced debugging and troubleshooting]({{< baseurl >}}kv/3.4.1/how-to/troubleshoot/erlang-vm/).

If an active remote_console session is detached in an unexpected way e.g. due to the network timeout of a SSH session over which the remote_console was run; "hanging" console process may be left running.  After a long period, a passive hanging console process may enter a loop and consume an entire CPU core.

It is good practice to monitor for the presence of long-lived hanging sessions, if `remote_console` is used.  Remote console sessions are distinguished with `ps -ef` by the `-progname` switch: Riak applications will have ``--progname <PATH>/bin/riak``; whereas `remote_console` sessions will have ``progname <path>/bin/erl``.

All single commands run from riak remote_console can be scripted from the command line using `riak eval`.  For example, to run the riak_client:repair_node() function from a script:

```console
riak eval "riak_client:repair_node()."
```

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

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
