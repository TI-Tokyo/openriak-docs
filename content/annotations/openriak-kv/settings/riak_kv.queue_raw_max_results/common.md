# Description

Default maximum result count when fetching raw results from a named HTTP query result queue. An explicit `max_results` query parameter overrides it.

# Datatype

Integer

# Units

- results

# Constraints

- Non-negative integer maximum result count, matching the HTTP query parameter contract.

# Inferred default

`1000` in the newer KV consumer.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_wm_query
concept: queueing, querying

# Notes

This is the Erlang application environment key `queue_raw_max_results` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_wm_query.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_wm_query.erl#L327)

# Reviewed against

3.4.0: 266267afe35bfba26c6e64b24b36a68a7e8020a934381e1fcfd4d29989a93ecc
3.4.1: 266267afe35bfba26c6e64b24b36a68a7e8020a934381e1fcfd4d29989a93ecc
