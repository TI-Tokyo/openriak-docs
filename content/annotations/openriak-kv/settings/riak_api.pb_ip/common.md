# Description

Deprecated IP address for a single Protocol Buffers listener, paired with `riak_api.pb_port`. Use the `riak_api.pb` list of address/port pairs, exposed through the listener configuration, for current deployments.

# Datatype

IP address

# Constraints

- An IP address string or address tuple accepted by the listener. Use together with `riak_api.pb_port`.

# Inferred default

Unset (`undefined`); no legacy listener is added unless both `pb_ip` and `pb_port` are set.

# Tags

feature: client-networking
repository: riak_api, riak_kv
module: riak_api_pb_listener, riak_kv_pb_object
concept: connections, compatibility

# Notes

This is the Erlang application environment key `pb_ip` in `riak_api`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_api/src/riak_api_pb_listener.erl](https://github.com/OpenRiak/riak_api/blob/ffdbd6be1afd3e2350eee99dc96930f7b339c3bf/src/riak_api_pb_listener.erl#L118)
- [riak_kv/src/riak_kv_pb_object.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_pb_object.erl#L687)

# Reviewed against

3.4.0: 696777a60de4e5702240b5f59617c575dfc8c7c9baefac6716a010d6017bbf6b
3.4.1: ee6c734466797f7252b5009935de8180dc03c4641076214a638cf5db49001cab
