# Description

Elapsed-time threshold, in milliseconds, below which arriving result batches are counted as fast in index and query timing diagnostics. It affects diagnostic classification, not the query timeout.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer.

# Inferred default

`10`.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_index_fsm, riak_kv_query_server
concept: diagnostics, querying

# Notes

This is the Erlang application environment key `index_fsm_fast_timems` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_index_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_index_fsm.erl#L44)
- [riak_kv/src/riak_kv_query_server.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_query_server.erl#L49)

# Reviewed against

3.4.0: 65245e124b7a9ffe8389c841b21457a2c33d66abc074b773e16687a7e0908c0b
3.4.1: 9cb8c22459657f9669c40d243d52cc1e9f02df376d2ea5fb61765c90f89839ec
