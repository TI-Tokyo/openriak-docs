# Description

Base number of workers in the shared realtime sink pool for writing incoming replicated objects. The `rtsink_max_workers` setting supplies the additional overflow allowance.

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
module: riak_repl2_rtsink_sup
concept: concurrency, cross-cluster-replication

# Notes

This is the Erlang application environment key `rtsink_min_workers` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtsink_sup.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtsink_sup.erl#L20)

# Reviewed against

3.4.0: 549c74be400c079f54e358f813cf75358038a7739ea7b07ef7af6dbea0e2e303
3.4.1: 549c74be400c079f54e358f813cf75358038a7739ea7b07ef7af6dbea0e2e303
