# Description

Interval, in milliseconds, between claimant maintenance ticks. The KV ensemble manager also uses this interval when checking whether strongly consistent ensembles need bootstrapping.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer timer delay.

# Inferred default

`10000`.

# Tags

feature: cluster-management
repository: riak_core, riak_kv
module: riak_core_claimant, riak_kv_ensembles
concept: scheduling, consensus

# Notes

This is the Erlang application environment key `claimant_tick` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_claimant.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_claimant.erl#L706)
- [riak_kv/src/riak_kv_ensembles.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_ensembles.erl#L128)

# Reviewed against

3.4.0: 2720df4323b2bd157b78297f5c1aefb2a4b7ffb07d0912536236c632ff8bb00d
3.4.1: 8f5031a3a7be18b29aaf8559ce2f7ee6ac5baf0b342f374ab56a8341f6ac26df
