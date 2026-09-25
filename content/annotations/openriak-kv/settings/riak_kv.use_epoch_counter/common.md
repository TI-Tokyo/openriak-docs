# Description

Enables leased vnode epoch counters used to assign new actor epochs and detect forgotten object history. Disabling it selects the legacy vnode counter behaviour.

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
concept: data-model

# Notes

This is the Erlang application environment key `use_epoch_counter` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L994)

# Reviewed against

3.4.0: 1019a95c1a1754b1409e136e0c12175233a3d87fe41b2ccea47d39916a73b0c1
3.4.1: 4302768a54f70defb23ba80a68509dba05ce9d6bacbc09dd69cc1d29f863a9db
