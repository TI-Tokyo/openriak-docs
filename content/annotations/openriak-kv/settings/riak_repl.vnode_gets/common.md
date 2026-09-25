# Description

Allows keylist full-sync to fetch differing objects directly from the source partition's vnode. Disabling it selects the client GET path through the object-fetch workers.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`true`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_keylist_server
concept: cross-cluster-replication, storage

# Notes

This is the Erlang application environment key `vnode_gets` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_keylist_server.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_keylist_server.erl#L147)

Additional type/default evidence:

- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: 7172511af8f26ba913f27ab3c9ef75c7e88095de96f51fe52a12c389452ce9f4
3.4.1: 7172511af8f26ba913f27ab3c9ef75c7e88095de96f51fe52a12c389452ce9f4
