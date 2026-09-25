# Description

Common-name access-control patterns checked against a replication peer's TLS certificate. A peer must match the configured ACL and must not have the same common name as the local certificate; certificate-chain validation is also applied.

# Datatype

String or list

# Constraints

- The string `"*"`, or a list of hostname-pattern strings such as `["peer.example.com", "*.example.com"]`. An empty list denies all; a single non-wildcard hostname must be wrapped in a list.

# Inferred default

`"*"`, allowing any peer common name that passes the other certificate checks.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_util
concept: authentication, tls

# Notes

This is the Erlang application environment key `peer_common_name_acl` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_util.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_util.erl#L563)

# Reviewed against

3.4.0: f6fca0e24b8ce247cc078377e992c07a82e292a02fff22f3c7daa3e888774d50
3.4.1: f6fca0e24b8ce247cc078377e992c07a82e292a02fff22f3c7daa3e888774d50
