# Description

Default sorting choice for secondary-index queries when the request does not specify one. Paginated queries always enable sorting regardless of this default.

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

feature: secondary-indexes
repository: riak_kv
module: riak_kv_index_fsm
concept: querying

# Notes

This is the Erlang application environment key `secondary_index_sort_default` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_index_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_index_fsm.erl#L124)

# Reviewed against

3.4.0: 1dabdce75ccb82eece1289be8b1b7db541ea7ebdfa987704c62e483e4209fbc2
3.4.1: b227081ff11680a53334930b206e6ea2636dae66c8af6739766f2b421ac8edb2
