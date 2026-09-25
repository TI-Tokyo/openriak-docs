# Description

Receive-buffer size, in bytes, applied to Erlang distribution sockets by `riak_core_dist_mon`. It affects inter-node distribution connections while that monitor is enabled.

# Datatype

Integer

# Units

- bytes

# Constraints

- Expected to be a positive integer socket buffer size.

# Inferred default

`786432` from `riak_core.app.src`.

# Tags

feature: erlang-runtime
repository: riak_core
module: riak_core_dist_mon
concept: connections, memory

# Notes

This is the Erlang application environment key `dist_recv_buf_size` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_dist_mon.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_dist_mon.erl#L62)

Additional type/default evidence:

- [riak_core/src/riak_core.app.src](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core.app.src)

# Reviewed against

3.4.0: 3a7d6fe757b2a95b2cdfce0c8355886cdcd15adfad7aa39de18c14fca8729a1e
3.4.1: 3a7d6fe757b2a95b2cdfce0c8355886cdcd15adfad7aa39de18c14fca8729a1e
