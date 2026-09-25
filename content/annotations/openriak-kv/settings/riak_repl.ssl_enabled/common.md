# Description

Enables construction and validation of TLS options for the legacy replication transport. Certificates, private key and CA certificates must also be configured; the helper reports invalid credentials and returns no TLS options when validation fails.

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
module: riak_repl_util
concept: cross-cluster-replication, tls

# Notes

This is the Erlang application environment key `ssl_enabled` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_util.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_util.erl#L423)

# Reviewed against

3.4.0: ea857d75f7358020baf05cd09af024d0a29af9573644c975dd3eba9c34f5812d
3.4.1: ea857d75f7358020baf05cd09af024d0a29af9573644c975dd3eba9c34f5812d
