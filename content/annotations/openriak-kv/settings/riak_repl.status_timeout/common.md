# Description

Timeout, in milliseconds, for replication status collection from source, sink and legacy connection processes. Unresponsive components are reported as unavailable or too busy instead of blocking status collection indefinitely.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Use an integer of at least `1000` if `status_helper_timeout` is not explicitly set; its fallback subtracts `1000` from this value.

# Inferred default

`5000`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rt, riak_repl2_rtsource_conn, riak_repl_console
concept: diagnostics

# Notes

This is the Erlang application environment key `status_timeout` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rt.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rt.erl#L192)
- [riak_repl/src/riak_repl2_rtsource_conn.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtsource_conn.erl#L200)
- [riak_repl/src/riak_repl_console.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_console.erl#L883)

# Reviewed against

3.4.0: ba4401a989b94357c8b03dcf5f1fc4dd36927ac193cf81dcd11f3b005158a32d
3.4.1: ba4401a989b94357c8b03dcf5f1fc4dd36927ac193cf81dcd11f3b005158a32d
