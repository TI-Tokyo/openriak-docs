# Description

Reverses the legacy replication client and server roles after connecting, allowing the connection initiator to act as the sending side. In this mode site clients run on the leader instead of being balanced across non-leader nodes.

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
module: riak_repl_leader, riak_repl_ring_handler, riak_repl_tcp_client, riak_repl_tcp_server
concept: connections, cross-cluster-replication

# Notes

This is the Erlang application environment key `inverse_connection` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_leader.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_leader.erl#L436)
- [riak_repl/src/riak_repl_ring_handler.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_ring_handler.erl#L176)
- [riak_repl/src/riak_repl_tcp_client.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_tcp_client.erl#L467)
- [riak_repl/src/riak_repl_tcp_server.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_tcp_server.erl#L270)

# Reviewed against

3.4.0: b567d802199691954782e2aa9e360e3bec1b09fa1b5cf7053571c731e8c416a9
3.4.1: b567d802199691954782e2aa9e360e3bec1b09fa1b5cf7053571c731e8c416a9
