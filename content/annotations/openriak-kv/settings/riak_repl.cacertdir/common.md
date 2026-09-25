# Description

Directory from which legacy replication loads trusted CA certificates for peer verification. TLS configuration validation requires the directory to yield a nonempty certificate list.

# Datatype

Directory path

# Constraints

- Directory path string containing CA certificates. Required for a usable legacy TLS configuration.

# Inferred default

`undefined`; no CA certificate directory is configured.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_util
concept: cross-cluster-replication, tls

# Notes

This is the Erlang application environment key `cacertdir` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_util.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_util.erl#L413)

# Reviewed against

3.4.0: 61ef4afe0ee0f4f89bb0f75d443fa1f22513024065791b3613f7bf6e3cc6dfc5
3.4.1: 61ef4afe0ee0f4f89bb0f75d443fa1f22513024065791b3613f7bf6e3cc6dfc5
