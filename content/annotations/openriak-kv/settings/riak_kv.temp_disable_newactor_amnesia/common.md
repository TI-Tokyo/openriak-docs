# Description

Temporarily bypasses the new-actor epoch protection when an incoming object contains history for a vnode that has forgotten the object. The source reserves this for exceptional repair situations, such as large tombstone differences between clusters, because it removes that protection.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`false`.

# Tags

feature: object-storage
repository: riak_kv
module: riak_kv_vnode
concept: data-model, replica-repair

# Notes

This is the Erlang application environment key `temp_disable_newactor_amnesia` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L4812)

# Reviewed against

3.4.0: 7fa3db976494b83961c1bf4ec9de4cb81ca5de508071548a2e70fbd46fb27650
3.4.1: 7fa3db976494b83961c1bf4ec9de4cb81ca5de508071548a2e70fbd46fb27650
