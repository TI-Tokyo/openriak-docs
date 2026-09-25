# Description

List of supported full-sync strategies advertised by the legacy replication TCP protocol. Peers negotiate a common strategy from their lists and start the corresponding client and server workers.

# Datatype

List

# Constraints

- Ordered list of strategy atoms. `keylist` is implemented by the bundled legacy client/server; other names require matching `riak_repl_<strategy>_client` and `_server` modules.

# Inferred default

`[keylist]`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_tcp_client, riak_repl_tcp_server
concept: compatibility, cross-cluster-replication

# Notes

This is the Erlang application environment key `fullsync_strategies` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_tcp_client.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_tcp_client.erl#L166)
- [riak_repl/src/riak_repl_tcp_server.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_tcp_server.erl#L290)

Additional type/default evidence:

- [riak_repl/include/riak_repl.hrl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/include/riak_repl.hrl)
- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: b3de877fc08121a934e9409bd6c4cf1baeb102711981eab535de7e0a8245539d
3.4.1: b3de877fc08121a934e9409bd6c4cf1baeb102711981eab535de7e0a8245539d
