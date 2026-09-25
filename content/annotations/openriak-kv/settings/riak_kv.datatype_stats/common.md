# Description

List of per-object CRDT statistics to collect from datatype modules that export `stat/2`. Unrecognized or unavailable measures are omitted from the returned statistics.

# Datatype

List

# Constraints

- List of statistic atoms understood by the datatype module's `stat/2` callback, such as `actor_count` for counters or `bytes` and `precision` for HyperLogLog. Unknown statistics returning `undefined` are omitted.

# Inferred default

`[bytes]` for HyperLogLog objects; `[actor_count]` for other CRDT types. A datatype without `stat/2` produces no statistics.

# Tags

feature: data-types
repository: riak_kv
module: riak_kv_crdt
concept: diagnostics

# Notes

This is the Erlang application environment key `datatype_stats` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_crdt.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_crdt.erl#L237)

Additional type/default evidence:

- [riak_kv/include/riak_kv_types.hrl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/include/riak_kv_types.hrl#L46)
- [riak_kv/src/riak_kv_hll.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_hll.erl#L192)

# Reviewed against

3.4.0: 33c6c32451a725da5a74dc9240a72f85503946f812b9880244a083c426aa6eb6
3.4.1: 672eb6846642ff7eccd8bee49c6cfb9a0269a835f86a13c0d80f84c772bd5edd
