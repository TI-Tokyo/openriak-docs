# Description

Base number of workers in a legacy replication TCP client's pool for storing incoming objects. The pool can create additional workers up to the separate `max_put_workers` overflow allowance.

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
module: riak_repl_tcp_client
concept: concurrency, cross-cluster-replication

# Notes

This is the Erlang application environment key `min_put_workers` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_tcp_client.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_tcp_client.erl#L516)

Additional type/default evidence:

- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: 8700e141c21ee20a5b53a0e1eba24d27d6168e1bf9eb9a3b9611c0403a073142
3.4.1: 8700e141c21ee20a5b53a0e1eba24d27d6168e1bf9eb9a3b9611c0403a073142
