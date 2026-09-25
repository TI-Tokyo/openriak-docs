# Description

Batch size used to apply backpressure while generating keylist full-sync differences. The Bloom-fold path uses it directly; the older path scales it by the number of acknowledgements allowed in flight.

# Datatype

Integer

# Units

- objects

# Constraints

- Non-negative integer batch size. The source explicitly permits `0` to remove this batching backpressure.

# Inferred default

`100`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_keylist_server
concept: queueing, cross-cluster-replication

# Notes

This is the Erlang application environment key `diff_batch_size` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_keylist_server.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_keylist_server.erl#L148)

Additional type/default evidence:

- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: 344c3ab4748b19edfd25a770eb9bf0f3f8f82595ecdf822796621210e667d417
3.4.1: 344c3ab4748b19edfd25a770eb9bf0f3f8f82595ecdf822796621210e667d417
