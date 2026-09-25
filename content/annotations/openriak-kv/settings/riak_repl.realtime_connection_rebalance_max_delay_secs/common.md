# Description

Maximum randomized delay, in seconds, before a realtime source attempts connection rebalancing. Randomization spreads reconnections across nodes instead of moving every connection at once.

# Datatype

Number

# Units

- seconds

# Constraints

- Expected to be a non-negative number, multiplied by a random factor and rounded to integer milliseconds.

# Inferred default

`300` (five minutes); the actual delay is randomized up to this limit.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtsource_conn
concept: connections, scheduling

# Notes

This is the Erlang application environment key `realtime_connection_rebalance_max_delay_secs` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtsource_conn.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtsource_conn.erl#L381)

# Reviewed against

3.4.0: ff2c8a5ab047f4d0d62e11301ce8c01fde7e1121eec450030dc10a99628bd414
3.4.1: ff2c8a5ab047f4d0d62e11301ce8c01fde7e1121eec450030dc10a99628bd414
