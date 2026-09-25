# Description

Delay, in milliseconds, between checks to reactivate a realtime sink socket paused by backpressure. Reading resumes when pending sink work has fallen enough.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer timer delay.

# Inferred default

`10`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtsink_conn
concept: queueing, scheduling

# Notes

This is the Erlang application environment key `reactivate_socket_interval_millis` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtsink_conn.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtsink_conn.erl#L439)

# Reviewed against

3.4.0: ff378658f2e122221733736b577b93350f713b3e65022b0d0b9df5b31182e26f
3.4.1: ff378658f2e122221733736b577b93350f713b3e65022b0d0b9df5b31182e26f
