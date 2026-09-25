# Description

Maximum additional overflow workers for the shared full-sync sink pool. The code passes this as Poolboy's `max_overflow`, so total capacity is `fssink_min_workers` plus this value.

# Datatype

Integer

# Units

- workers

# Constraints

- Non-negative integer passed as Poolboy `max_overflow`: additional workers above the base pool size.

# Inferred default

`100`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_fssink_pool
concept: concurrency, cross-cluster-replication

# Notes

This is the Erlang application environment key `fssink_max_workers` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_fssink_pool.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_fssink_pool.erl#L9)

# Reviewed against

3.4.0: a1639b2eba5e0e2c47d9897ade119653af202b39bf8b5e1b8c45e0210b514e3a
3.4.1: a1639b2eba5e0e2c47d9897ade119653af202b39bf8b5e1b8c45e0210b514e3a
