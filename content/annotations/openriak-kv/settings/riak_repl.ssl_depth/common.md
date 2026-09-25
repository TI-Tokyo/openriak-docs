# Description

Certificate-chain depth limit passed to Erlang TLS when validating legacy replication peers. It controls the permitted depth of the peer's certificate chain.

# Datatype

Integer

# Units

- certificates

# Constraints

- Expected to be a non-negative integer maximum certificate-chain depth.

# Inferred default

`1`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_util
concept: authentication, tls

# Notes

This is the Erlang application environment key `ssl_depth` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_util.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_util.erl#L414)

# Reviewed against

3.4.0: 7e1bbf9fbf1ee29de5eb5b515fe7bdf0c8a5dafddda05895026bcc84e2972181
3.4.1: 7e1bbf9fbf1ee29de5eb5b515fe7bdf0c8a5dafddda05895026bcc84e2972181
