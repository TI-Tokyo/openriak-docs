# Description

Elapsed-time threshold, in milliseconds, above which arriving result batches are counted as slow in index and query timing diagnostics. It affects diagnostic classification, not the query timeout.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer.

# Inferred default

`200`.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_index_fsm, riak_kv_query_server
concept: diagnostics, querying

# Notes

This is the Erlang application environment key `index_fsm_slow_timems` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_index_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_index_fsm.erl#L43)
- [riak_kv/src/riak_kv_query_server.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_query_server.erl#L48)

# Reviewed against

3.4.0: c93fe2164acfd4f19e7217c907864a53dd42d7a39b6541430e9ddb5ae892e9a5
3.4.1: 9b08af6fb400265e049a6c00247e6eecf8efb0bbbbe6b0984227addb82f46cb4
