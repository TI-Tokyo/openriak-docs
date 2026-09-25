# Description

Optional `{Module, Function}` callback invoked with an object dropped from realtime replication. It allows custom reporting or handling of dropped objects.

# Datatype

Tuple

# Constraints

- `{Module, Function}` atom pair; callback receives the dropped object (arity 1).

# Inferred default

Unset (`undefined`); no dropped-object callback is invoked.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_util
concept: diagnostics, cross-cluster-replication

# Notes

This is the Erlang application environment key `dropped_hook` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_util.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_util.erl#L786)

# Reviewed against

3.4.0: c67239417984fc32aba495b65314fb1c38b7778bf60ff36589aa7fa3ea91a661
3.4.1: c67239417984fc32aba495b65314fb1c38b7778bf60ff36589aa7fa3ea91a661
