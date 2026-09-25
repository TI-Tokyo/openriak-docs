# Description

Delay before the replication connection manager retries a target for which endpoint discovery returned no addresses. This controls retry scheduling while the remote target has no usable advertised endpoint.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer timer delay.

# Inferred default

`5000` in production builds; `2000` in builds compiled with `TEST`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_core_connection_mgr
concept: connections, scheduling

# Notes

This is the Erlang application environment key `connmgr_no_endpoint_retry` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_core_connection_mgr.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_core_connection_mgr.erl#L501)

# Reviewed against

3.4.0: 901396524763a6f559de7c6b35ac28a7a7a7059ff0b51d6dc0424b8e04c5613b
3.4.1: 901396524763a6f559de7c6b35ac28a7a7a7059ff0b51d6dc0424b8e04c5613b
