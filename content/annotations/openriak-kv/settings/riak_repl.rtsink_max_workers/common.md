# Description

Maximum additional overflow workers for the shared realtime sink pool. The code uses it as Poolboy's `max_overflow`, making total capacity `rtsink_min_workers` plus this value.

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
module: riak_repl2_rtsink_sup
concept: concurrency, cross-cluster-replication

# Notes

This is the Erlang application environment key `rtsink_max_workers` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtsink_sup.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtsink_sup.erl#L21)

# Reviewed against

3.4.0: 15018c1cf39d52ba408dd7c7c69ce5188714b9e765401b368cd00db0983f39a5
3.4.1: 15018c1cf39d52ba408dd7c7c69ce5188714b9e765401b368cd00db0983f39a5
