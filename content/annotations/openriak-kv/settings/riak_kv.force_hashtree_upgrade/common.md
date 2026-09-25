# Description

Forces the legacy anti-entropy hash-tree startup path to request an upgrade. Only boolean values are accepted; other values are logged and treated as false.

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

feature: legacy-aae
repository: riak_kv
module: riak_kv_index_hashtree
concept: compatibility, replica-repair

# Notes

This is the Erlang application environment key `force_hashtree_upgrade` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_index_hashtree.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_index_hashtree.erl#L539)

# Reviewed against

3.4.0: 8577d37258155b1380afcea1acda14a7509bb4bfae060c01106d31cf7b489fcd
3.4.1: e0d18a17f4988263dc3038aa2d0d656cef6a84e6e1df9ba3d31dda700293368b
