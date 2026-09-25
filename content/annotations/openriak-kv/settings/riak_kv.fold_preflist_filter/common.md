# Description

Adds bucket, partition and replication-factor information to key-fold options so supporting backends can filter by preference-list ownership. When false, the vnode supplies no extra ownership filter.

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

feature: query-processing
repository: riak_kv
module: riak_kv_vnode
concept: partition-placement, querying

# Notes

This is the Erlang application environment key `fold_preflist_filter` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L3846)

# Reviewed against

3.4.0: 2188fac92d5ebd77c12e1d25eba85b3c588623439072f5b87d6be8de17f26a88
3.4.1: 72b0ad4e8ca765594409306669b28b68f81b74f96740b6d06c001f90e1d32b93
