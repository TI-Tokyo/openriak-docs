# Description

Base number of workers retained in the shared full-sync sink pool to write incoming replicated objects. `fssink_max_workers` allows extra workers during bursts.

# Datatype

Integer

# Units

- workers

# Constraints

- Non-negative integer passed as Poolboy `size`: base worker count.

# Inferred default

`5`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_fssink_pool
concept: concurrency, cross-cluster-replication

# Notes

This is the Erlang application environment key `fssink_min_workers` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_fssink_pool.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_fssink_pool.erl#L8)

# Reviewed against

3.4.0: 506cbbfec5bb32e8f57a40c762316048cdb4438b71e86250b61d85d8151b956a
3.4.1: 506cbbfec5bb32e8f57a40c762316048cdb4438b71e86250b61d85d8151b956a
