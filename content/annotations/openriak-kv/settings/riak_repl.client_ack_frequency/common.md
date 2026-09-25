# Description

Number of received replication items between client acknowledgements in the legacy bounded-queue protocol. The keylist full-sync client also uses it to acknowledge received keylist data, providing sender backpressure.

# Datatype

Integer

# Units

- objects

# Constraints

- Expected to be a positive integer acknowledgement frequency.

# Inferred default

`5`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_keylist_client, riak_repl_tcp_client
concept: queueing, cross-cluster-replication

# Notes

This is the Erlang application environment key `client_ack_frequency` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_keylist_client.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_keylist_client.erl#L62)
- [riak_repl/src/riak_repl_tcp_client.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_tcp_client.erl#L497)

Additional type/default evidence:

- [riak_repl/include/riak_repl.hrl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/include/riak_repl.hrl)
- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: 637f8c199280f5a9b15309f08834d26bd98f571c38e457f91d6cecdd24443f2e
3.4.1: 637f8c199280f5a9b15309f08834d26bd98f571c38e457f91d6cecdd24443f2e
