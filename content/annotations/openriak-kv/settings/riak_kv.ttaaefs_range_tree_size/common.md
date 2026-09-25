# Description

Hash-tree size used for Tictac full-sync range comparisons. Accepted sizes are `small`, `medium`, `large` and `xlarge`; invalid or absent values use `small`.

# Datatype

Enum

# Allowed values

- `small`
- `medium`
- `large`
- `xlarge`

# Constraints

- The consumer explicitly accepts only these tree-size atoms.

# Inferred default

`small`; missing or unsupported values also fall back to `small`.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: memory, cross-cluster-replication

# Notes

This is the Erlang application environment key `ttaaefs_range_tree_size` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_ttaaefs_manager.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_ttaaefs_manager.erl#L963)

# Reviewed against

3.4.0: 9427f01cd381ffabb0f895391cbb742dd3a357d16dcdceecc1682d2a8bc95bfb
3.4.1: 9427f01cd381ffabb0f895391cbb742dd3a357d16dcdceecc1682d2a8bc95bfb
