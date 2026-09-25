# Description

Allows the `iterator_refresh` fold option to reach backends that advertise support for refreshing iterators. Disabling it removes that option from the fold request.

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

feature: storage-backends
repository: riak_kv
module: riak_kv_vnode
concept: querying, storage

# Notes

This is the Erlang application environment key `iterator_refresh` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L4019)

# Reviewed against

3.4.0: 1f4e2dfa48897d14b0e33ed8d08d06786e03d651eef2ba61a9c2c04670306b44
3.4.1: a2f5f8fa2568d39786c5a02fc9cab26ec6dcb4d87c95613138e485091f36290a
