# Description

Interval, in milliseconds, between the node watcher's broadcasts of node and service availability. This controls service-status gossip rather than the ring gossip token limit.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer timer delay.

# Inferred default

`60000` from `riak_core.app.src`.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_node_watcher
concept: scheduling

# Notes

This is the Erlang application environment key `gossip_interval` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_node_watcher.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_node_watcher.erl#L408)

Additional type/default evidence:

- [riak_core/src/riak_core.app.src](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core.app.src)

# Reviewed against

3.4.0: 9d9e03cb0362937f064ce9bc2cec5f5233ce583c5cc8f0b8d0400fb96592e3dd
3.4.1: 9d9e03cb0362937f064ce9bc2cec5f5233ce583c5cc8f0b8d0400fb96592e3dd
