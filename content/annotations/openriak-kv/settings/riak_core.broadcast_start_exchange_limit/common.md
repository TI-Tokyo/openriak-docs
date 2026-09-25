# Description

Maximum number of broadcast anti-entropy exchanges this node may initiate concurrently. Incoming exchange limits are the responsibility of the individual exchange implementation.

# Datatype

Integer

# Units

- exchanges

# Constraints

- Expected to be a non-negative integer; `0` prevents starting new outgoing exchanges.

# Inferred default

`1`.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_broadcast
concept: concurrency, replica-repair

# Notes

This is the Erlang application environment key `broadcast_start_exchange_limit` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_broadcast.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_broadcast.erl#L411)

# Reviewed against

3.4.0: 0dd78f9eb054a078882224e4cb3d2c143130bb8ad6e4e3e0a17220aa504bf7d6
3.4.1: 0dd78f9eb054a078882224e4cb3d2c143130bb8ad6e4e3e0a17220aa504bf7d6
