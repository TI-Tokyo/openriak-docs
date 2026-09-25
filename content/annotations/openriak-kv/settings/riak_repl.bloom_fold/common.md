# Description

Allows keylist full-sync to use a Bloom-filter-assisted backend fold when all nodes advertise that capability. Setting it to false keeps the older per-key difference processing path.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`true`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_keylist_server
concept: cross-cluster-replication, storage

# Notes

This is the Erlang application environment key `bloom_fold` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_keylist_server.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_keylist_server.erl#L839)

# Reviewed against

3.4.0: 4fb5da418fbe1f6ed9024520fcdbf81d379fc6dbfa450b3410d797fc64bdde8e
3.4.1: 4fb5da418fbe1f6ed9024520fcdbf81d379fc6dbfa450b3410d797fc64bdde8e
