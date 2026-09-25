# Description

Path to the local certificate used for legacy replication TLS connections. Its common name is also used by the replication peer-certificate verification callback.

# Datatype

File path

# Constraints

- Path string naming a readable PEM certificate file for legacy TLS.

# Inferred default

`undefined`; no certificate file is configured.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_util
concept: cross-cluster-replication, tls

# Notes

This is the Erlang application environment key `certfile` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_util.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_util.erl#L411)

# Reviewed against

3.4.0: 73f3892b7069bf067ce7d8a023bb1785456f21554588a88f7b2ca1470b7eed16
3.4.1: 73f3892b7069bf067ce7d8a023bb1785456f21554588a88f7b2ca1470b7eed16
