# Description

Maximum byte size of the legacy replication connection's bounded outgoing queue. When the queue exceeds its capacity, it drops queued entries and records the loss.

# Datatype

Integer

# Units

- bytes

# Constraints

- Non-negative integer byte capacity according to the bounded-queue specification. An oversized incoming item is retained alone, even when the capacity is zero.

# Inferred default

`104857600` (100 MiB).

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_bq
concept: memory, queueing

# Notes

This is the Erlang application environment key `queue_size` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_bq.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_bq.erl#L41)

Additional type/default evidence:

- [riak_repl/include/riak_repl.hrl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/include/riak_repl.hrl)
- [riak_repl/src/riak_repl.app.src](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl.app.src)

# Reviewed against

3.4.0: 26ad140e066dd68df8f569105fa90b15f5bdb7c121be834ba1c8f402a2f0bd45
3.4.1: 26ad140e066dd68df8f569105fa90b15f5bdb7c121be834ba1c8f402a2f0bd45
