# Description

Advertises TLS support in the cluster service connection handshake used by legacy replication. The client and service connection code use the peers' advertised flags when negotiating a TLS upgrade.

# Datatype

Boolean

# Allowed values

- `true`
- `false`

# Constraints

- Use the Erlang atoms `true` or `false`.

# Inferred default

`false`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_core_connection, riak_core_service_conn, riak_core_service_mgr
concept: cross-cluster-replication, tls

# Notes

This is the Erlang application environment key `ssl_enabled` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_core_connection.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_core_connection.erl#L170)
- [riak_repl/src/riak_core_service_conn.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_core_service_conn.erl#L91)
- [riak_repl/src/riak_core_service_mgr.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_core_service_mgr.erl#L307)

# Reviewed against

3.4.0: 487a9b930e09a62bdb7ee2b114ba0f0327d3621577dc08512d1c3de0b696cb05
3.4.1: 487a9b930e09a62bdb7ee2b114ba0f0327d3621577dc08512d1c3de0b696cb05
