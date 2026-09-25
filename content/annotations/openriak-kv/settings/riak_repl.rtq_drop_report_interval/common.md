# Description

Interval, in milliseconds, used by the realtime queue overload counter to report objects dropped during overload. It controls reporting frequency rather than the overload threshold.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer timer delay.

# Inferred default

`5000`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtq_overload_counter
concept: diagnostics, overload-protection

# Notes

This is the Erlang application environment key `rtq_drop_report_interval` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtq_overload_counter.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtq_overload_counter.erl#L29)

# Reviewed against

3.4.0: 9b3927894f488d68a5dd005857bb3928a8215f22897d35f80e00178c88487c48
3.4.1: 9b3927894f488d68a5dd005857bb3928a8215f22897d35f80e00178c88487c48
