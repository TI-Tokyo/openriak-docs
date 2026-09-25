# Description

Base number of workers in a keylist full-sync source's object-fetch pool. The pool can create additional workers up to the separate `max_get_workers` overflow allowance.

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
module: riak_repl_keylist_server
concept: concurrency, cross-cluster-replication

# Notes

This is the Erlang application environment key `min_get_workers` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_keylist_server.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_keylist_server.erl#L145)

Additional type/default evidence:

- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: 57527f0456653e2aa59af35374cb0bc50b58489cb7e0d03cbc73160dedea6013
3.4.1: 57527f0456653e2aa59af35374cb0bc50b58489cb7e0d03cbc73160dedea6013
