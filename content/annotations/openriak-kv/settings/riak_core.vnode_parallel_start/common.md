# Description

Maximum parallelism when the vnode manager starts and waits for a group of vnodes. Values of one or less also switch vnode initialization to the synchronous startup path.

# Datatype

Integer

# Units

- vnodes

# Constraints

- Use a positive integer. Values at most `1` select synchronous initialization; the manager also uses the value as a concurrency limit.

# Inferred default

Consumer-dependent: vnode initialization uses `2` to enable asynchronous starts, while the vnode manager uses `16` as its parallel-start limit.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_vnode, riak_core_vnode_manager
concept: concurrency, runtime

# Notes

This is the Erlang application environment key `vnode_parallel_start` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_vnode.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_vnode.erl#L205)
- [riak_core/src/riak_core_vnode_manager.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_vnode_manager.erl#L747)

# Reviewed against

3.4.0: 6d859f8792524ffe3d5f25c5bbd248600abef88ac32d54e20c75cf2af66b0ec3
3.4.1: 6d859f8792524ffe3d5f25c5bbd248600abef88ac32d54e20c75cf2af66b0ec3
