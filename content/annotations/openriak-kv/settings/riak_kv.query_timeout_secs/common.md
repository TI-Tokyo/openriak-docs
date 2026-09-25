# Description

Default query execution timeout, in seconds, for the HTTP query interface. An explicit timeout in the query request overrides it; the value must be a positive integer.

# Datatype

Integer

# Units

- seconds

# Constraints

- Validated as an integer greater than zero.

# Inferred default

`60`.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_wm_query
concept: querying

# Notes

This is the Erlang application environment key `query_timeout_secs` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_wm_query.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_wm_query.erl#L575)

# Reviewed against

3.4.0: 4665cb52517e09ae072f56592e3fbfca5eaf08f958c83373f09d683188badc8a
3.4.1: 172b0218179063c698e7dc4fb93a7c5ae74a242cbddf888cc948bbe1da5a1ebb
