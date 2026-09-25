# Description

Send-buffer size, in bytes, applied to Erlang distribution sockets by `riak_core_dist_mon`. It affects inter-node distribution connections while that monitor is enabled.

# Datatype

Integer

# Units

- bytes

# Constraints

- Expected to be a positive integer socket buffer size.

# Inferred default

`393216` from `riak_core.app.src`.

# Tags

feature: erlang-runtime
repository: riak_core
module: riak_core_dist_mon
concept: connections, memory

# Notes

This is the Erlang application environment key `dist_send_buf_size` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_dist_mon.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_dist_mon.erl#L61)

Additional type/default evidence:

- [riak_core/src/riak_core.app.src](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core.app.src)

# Reviewed against

3.4.0: 3336627cba4a42f98d33b443bc485971e1ebdc1c48fab4d58ee2d2df985f23c5
3.4.1: 3336627cba4a42f98d33b443bc485971e1ebdc1c48fab4d58ee2d2df985f23c5
