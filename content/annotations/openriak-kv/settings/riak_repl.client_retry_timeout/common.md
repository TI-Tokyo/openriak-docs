# Description

Delay, in milliseconds, before retrying the legacy replication site's listener list after all connection attempts have failed.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer timer delay.

# Inferred default

`30000`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_tcp_client
concept: connections, scheduling

# Notes

This is the Erlang application environment key `client_retry_timeout` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_tcp_client.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_tcp_client.erl#L335)

Additional type/default evidence:

- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: 783221c22612eadc16d8db3101a23a1fd29ca450606e412ccf7009888c7fe1f2
3.4.1: 783221c22612eadc16d8db3101a23a1fd29ca450606e412ccf7009888c7fe1f2
