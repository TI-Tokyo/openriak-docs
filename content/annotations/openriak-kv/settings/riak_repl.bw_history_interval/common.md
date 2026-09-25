# Description

Interval, in milliseconds, between replication bandwidth samples. The statistics process uses the change in transferred bytes to record bandwidth history.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer timer delay.

# Inferred default

`60000`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_stats
concept: diagnostics, scheduling

# Notes

This is the Erlang application environment key `bw_history_interval` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl_stats.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl_stats.erl#L280)

# Reviewed against

3.4.0: 8da45d8d07f2ef6802f75d7fe9cadaceab1c2fdce911792f601b8f41998a03c6
3.4.1: 8da45d8d07f2ef6802f75d7fe9cadaceab1c2fdce911792f601b8f41998a03c6
