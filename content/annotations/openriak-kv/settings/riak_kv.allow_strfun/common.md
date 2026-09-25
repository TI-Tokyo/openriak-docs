# Description

Allows MapReduce map and reduce functions supplied as Erlang source strings to be compiled and executed, including source loaded from stored objects. This enables execution of supplied code on the node and is disabled in the map-phase fallback.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`false` from `riak_kv.app.src` and the map phase fallback.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_mrc_map, riak_kv_w_reduce
concept: querying

# Notes

This is the Erlang application environment key `allow_strfun` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_mrc_map.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_mrc_map.erl#L114)
- [riak_kv/src/riak_kv_w_reduce.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_w_reduce.erl#L233)

Additional type/default evidence:

- [riak_kv/src/riak_kv.app.src](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv.app.src)

# Reviewed against

3.4.0: dd74a907712c5942844f88d1d5e9e4d47f10aab3fbe028dc0aad67c292af3630
3.4.1: 421965d9c0459ace559d77b96536a6193168790dc4674fe5d6af5e9bf06a6dcf
