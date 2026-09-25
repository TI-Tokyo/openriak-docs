# Description

Per-vnode concurrency limit registered with the background manager for subsystems that acquire the KV vnode lock before folding. Only participating background tasks observe this limit, and it has no effect when the background manager is disabled.

# Datatype

Integer

# Units

- folds

# Constraints

- Expected to be a non-negative concurrency limit; zero admits no concurrent locks.

# Inferred default

`1`; non-integer input also falls back to `1`.

# Tags

feature: background-management
repository: riak_kv
module: riak_kv_vnode
concept: concurrency, storage

# Notes

This is the Erlang application environment key `vnode_lock_concurrency` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_vnode.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_vnode.erl#L4536)

# Reviewed against

3.4.0: 1aff83bcf17e86c4894ca54a5561337b5907f79c37d6c7649b5fac34890e8c09
3.4.1: b245958fd0aa4bf523db98155fd5b2c8795b1d73b9844bdbd90626edc7a2c9f9
