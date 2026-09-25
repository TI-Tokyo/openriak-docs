# Description

Allows the vnode to use a storage backend's asynchronous `async_put/5` interface when that backend exports it. Disabling it forces the synchronous write path.

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

feature: object-storage
repository: riak_kv
module: riak_kv_vnode
concept: concurrency, storage

# Notes

This is the Erlang application environment key `allow_async_put` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L1031)

# Reviewed against

3.4.0: ad9d55b4ea7383fcb10b82bec1c176e1a3318f35322eda0dfcc9409709393201
3.4.1: f6c05ecb4da5f5a50e9360b44c91cc3dd780726cb7bf35fd50713b2c21a1685e
