# Description

Interval, in milliseconds, for aggregating and reporting realtime objects dropped because their bucket types are missing or incompatible at the sink. Each report resets the accumulated drop counts.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer timer delay.

# Inferred default

`10000`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtsink_conn
concept: diagnostics, cross-cluster-replication

# Notes

This is the Erlang application environment key `bucket_type_drop_report_interval` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtsink_conn.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtsink_conn.erl#L117)

# Reviewed against

3.4.0: 550cb8888d74d7805ee2ec3b973dbda6c469896b75b7e31935379602edd783b0
3.4.1: 550cb8888d74d7805ee2ec3b973dbda6c469896b75b7e31935379602edd783b0
