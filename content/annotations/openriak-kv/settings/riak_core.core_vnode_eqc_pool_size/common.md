# Description

Worker-pool size used by the mock vnode in Riak Core's property tests. A positive value creates a mock worker pool; other values skip it. It does not size production vnode pools.

# Datatype

Integer

# Units

- workers

# Constraints

- A positive integer creates that many workers; zero disables the test pool.

# Inferred default

No fallback; the property-test harness must set the key before starting the mock vnode.

# Tags

feature: worker-pools
repository: riak_core
module: mock_vnode
concept: testing

# Notes

This is the Erlang application environment key `core_vnode_eqc_pool_size` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/mock_vnode.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/mock_vnode.erl#L116)

# Reviewed against

3.4.0: f79ea1002e986dc659e4f6264809287769a5ff92397a17dd71afc2c8454984c3
3.4.1: f79ea1002e986dc659e4f6264809287769a5ff92397a17dd71afc2c8454984c3
