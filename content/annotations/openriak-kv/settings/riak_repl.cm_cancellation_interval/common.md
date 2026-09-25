# Description

Delay, in milliseconds, before the connection manager removes a cancelled connection request from its pending state. The value `undefined` disables scheduled removal of cancelled requests.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer timer delay.

# Inferred default

`300000`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_core_connection_mgr
concept: connections, scheduling

# Notes

This is the Erlang application environment key `cm_cancellation_interval` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_core_connection_mgr.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_core_connection_mgr.erl#L710)

# Reviewed against

3.4.0: f4ea7eb6e0af482b9b3c5636ef02ca3498c592993013e183d89bd703fc2d8172
3.4.1: f4ea7eb6e0af482b9b3c5636ef02ca3498c592993013e183d89bd703fc2d8172
