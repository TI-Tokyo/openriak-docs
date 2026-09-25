# Description

Timeout, in milliseconds, for an individual legacy replication TCP connection attempt to a site's listener.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer TCP connection timeout, or `infinity`.

# Inferred default

`15000`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_tcp_client
concept: connections

# Notes

This is the Erlang application environment key `client_connect_timeout` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_tcp_client.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_tcp_client.erl#L347)

Additional type/default evidence:

- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: 9ae85289a4089c1fd6ae692c38ba00c82cb10ad5e26039387671706d3a459623
3.4.1: 9ae85289a4089c1fd6ae692c38ba00c82cb10ad5e26039387671706d3a459623
