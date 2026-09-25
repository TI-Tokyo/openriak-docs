# Description

Maximum additional overflow workers for a keylist full-sync source's object-fetch pool. It is passed as Poolboy's `max_overflow`, so total capacity is `min_get_workers` plus this value.

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
module: riak_repl_keylist_server
concept: concurrency, cross-cluster-replication

# Notes

This is the Erlang application environment key `max_get_workers` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_keylist_server.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_keylist_server.erl#L146)

Additional type/default evidence:

- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: 7c2f031cebd30dd252002ec5eed490998ae711157e006342aeaa0ae074226b07
3.4.1: 7c2f031cebd30dd252002ec5eed490998ae711157e006342aeaa0ae074226b07
