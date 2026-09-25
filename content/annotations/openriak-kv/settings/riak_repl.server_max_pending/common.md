# Description

Maximum number of sent but unacknowledged items on a legacy replication bounded-queue connection. Once reached, the sender retains further work in its outgoing queue until acknowledgements arrive.

# Datatype

Integer

# Units

- objects

# Constraints

- Expected to be a positive integer pending-object limit.

# Inferred default

`5`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_bq
concept: queueing, cross-cluster-replication

# Notes

This is the Erlang application environment key `server_max_pending` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_bq.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_bq.erl#L43)

Additional type/default evidence:

- [riak_repl/include/riak_repl.hrl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/include/riak_repl.hrl)
- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: 6aedddac59b2bbf6ec979bcd0420dec0e47acea5907accc8ac97393646a45ca3
3.4.1: 6aedddac59b2bbf6ec979bcd0420dec0e47acea5907accc8ac97393646a45ca3
