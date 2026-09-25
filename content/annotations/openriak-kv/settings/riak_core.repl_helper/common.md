# Description

Registry of `{Application, Module}` replication helpers. Their receive, full-sync send and realtime send callbacks can inspect objects, cancel replication or supply additional objects to replicate.

# Datatype

List

# Constraints

- List of `{Application, Module}` atom pairs. Receiving helpers implement `recv/1`.

# Inferred default

Unset; no replication helper is invoked until applications register helpers.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_util
concept: cross-cluster-replication

# Notes

This is the Erlang application environment key `repl_helper` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_util.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_util.erl#L196)

# Reviewed against

3.4.0: 2fe79e0f571a235bf36366761f7c868bc315395dcc898e2f6478466ee2e47b7c
3.4.1: 2fe79e0f571a235bf36366761f7c868bc315395dcc898e2f6478466ee2e47b7c
