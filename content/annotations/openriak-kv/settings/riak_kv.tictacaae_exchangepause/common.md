# Description

Pause, in milliseconds, between state transitions in Tictac AAE exchanges. Both local repair exchanges and Tictac full-sync exchanges pass it to the exchange engine as `transition_pause_ms`.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer exchange pause.

# Inferred default

`1000`.

# Tags

feature: tictac-aae, full-sync
repository: riak_kv
module: riak_kv_tictacaae_repairs, riak_kv_ttaaefs_manager
concept: scheduling, replica-repair

# Notes

This is the Erlang application environment key `tictacaae_exchangepause` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_tictacaae_repairs.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_tictacaae_repairs.erl#L78)
- [riak_kv/src/riak_kv_ttaaefs_manager.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_ttaaefs_manager.erl#L265)

# Reviewed against

3.4.0: d8f3e42cdc6d2e4d951eba7e5f5d6279597f0d65f4d4648f5d2d74518b53777a
3.4.1: 2a6308900c5079280bd77e2aaaada0fd457189b03b9ac6e4ac1c037e39cb0b4c
