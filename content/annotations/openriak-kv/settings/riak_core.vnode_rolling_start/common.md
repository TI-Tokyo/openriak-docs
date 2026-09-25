# Description

Number of vnode-start tokens replenished during vnode-manager management ticks. It bounds how many missing vnodes may be started in a rolling startup pass.

# Datatype

Integer

# Units

- vnodes

# Constraints

- Expected to be a positive integer token budget.

# Inferred default

`max(16, RingCreationSize div 4)`, with a fallback ring size of `64` (giving `16`).

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_vnode_manager
concept: concurrency, runtime

# Notes

This is the Erlang application environment key `vnode_rolling_start` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_vnode_manager.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_vnode_manager.erl#L569)

# Reviewed against

3.4.0: 418ef3bf9220ed799884feacd304b3165453c496ed50ba691cbe695a898ac43f
3.4.1: 418ef3bf9220ed799884feacd304b3165453c496ed50ba691cbe695a898ac43f
