# Description

Enables asynchronous backend folds where the storage backend supports them. Such folds can run through worker pools instead of occupying the vnode while listing or scanning data.

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
concept: concurrency, querying

# Notes

This is the Erlang application environment key `async_folds` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L1002)

# Reviewed against

3.4.0: b907b98dbeb76d8f2f042bbf21893e0cfb42dd6f1578f85e97011c5bf1bdaa82
3.4.1: 333d2f054464b5b0e877fab5fff79d07fcd816d5dcb6880058b03d712dac260d
