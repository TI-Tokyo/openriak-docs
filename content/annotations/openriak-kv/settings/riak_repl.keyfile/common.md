# Description

Path to the private key corresponding to the local legacy replication TLS certificate. The replication TLS helper includes it in the socket options and checks that the file exists.

# Datatype

File path

# Constraints

- Path string naming a readable PEM private key file for legacy TLS.

# Inferred default

`undefined`; no private key file is configured.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_util
concept: cross-cluster-replication, tls

# Notes

This is the Erlang application environment key `keyfile` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_util.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_util.erl#L412)

# Reviewed against

3.4.0: 707dd8cee54624de0a89aa860622f1fbfa0e46f4d24696a0f41d7cf7e72b0355
3.4.1: 707dd8cee54624de0a89aa860622f1fbfa0e46f4d24696a0f41d7cf7e72b0355
