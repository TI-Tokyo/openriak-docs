# Description

Maximum additional overflow workers for a legacy replication TCP client's object-write pool. It is passed as Poolboy's `max_overflow`, so total capacity is `min_put_workers` plus this value.

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
module: riak_repl_tcp_client
concept: concurrency, cross-cluster-replication

# Notes

This is the Erlang application environment key `max_put_workers` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_tcp_client.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_tcp_client.erl#L517)

Additional type/default evidence:

- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: 41bc1ea86da0584ac89821005871d99aa7f8f0b934d3868bcf2d8173510effa2
3.4.1: 41bc1ea86da0584ac89821005871d99aa7f8f0b934d3868bcf2d8173510effa2
