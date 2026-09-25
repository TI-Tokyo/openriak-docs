# Description

Time, in milliseconds, to wait for a forwarded PUT coordinator to acknowledge execution before treating it as failed and considering a retry. It works with the coordinator-failure retry option and negotiated acknowledgement capability.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer receive timeout, or `infinity`.

# Inferred default

`3000`.

# Tags

feature: request-processing
repository: riak_kv
module: riak_kv_put_fsm
concept: quorums, runtime

# Notes

This is the Erlang application environment key `put_coordinator_failure_timeout` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_put_fsm.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_put_fsm.erl#L193)

# Reviewed against

3.4.0: e0f12f21c95891bc1fc9ef0e434d5c0b6aa78a739485c04a121fc328cb65ffda
3.4.1: 1cb0ddad8867f1788b30e5dc6250277cc58267e4ab748e597e671baedea94692
