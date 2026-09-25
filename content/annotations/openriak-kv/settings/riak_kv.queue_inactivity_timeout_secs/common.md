# Description

Default inactivity timeout, in seconds, for an HTTP query's result queue. The request can override it with an inactivity timeout, controlling how long unused queued results are retained.

# Datatype

Integer

# Units

- seconds

# Constraints

- Validated as an integer greater than zero.

# Inferred default

`120` in the newer KV consumer.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_wm_query
concept: queueing, querying

# Notes

This is the Erlang application environment key `queue_inactivity_timeout_secs` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_wm_query.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_wm_query.erl#L581)

# Reviewed against

3.4.0: 1bd348614cc9166802635750ada93078fdaab7cc4caa70e4d63067f815627236
3.4.1: 1bd348614cc9166802635750ada93078fdaab7cc4caa70e4d63067f815627236
