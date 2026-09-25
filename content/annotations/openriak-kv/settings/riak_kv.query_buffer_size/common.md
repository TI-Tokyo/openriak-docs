# Description

Base result-buffer size used by the query server. The server enforces its minimum buffer size and can reduce the buffer for queries with a small `max_results` limit to limit excess results.

# Datatype

Integer

# Units

- results

# Constraints

- Integer buffer size, clamped to at least `16`; bounded queries can adjust the effective size.

# Inferred default

`320` before per-query sizing.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_query_server
concept: memory, querying

# Notes

This is the Erlang application environment key `query_buffer_size` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_query_server.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_query_server.erl#L619)

# Reviewed against

3.4.0: 634e08111ccbe06294efba0fad439b67066137d18bc7301349a80881ff4b9e44
3.4.1: 94e19151f60fc3ce6b26ba88a68f893195a45fb6a128b91583f838358b0a9f37
