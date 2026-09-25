# Description

Deprecated port for a single Protocol Buffers listener, paired with `riak_api.pb_ip`. Both values must be supplied to add this legacy listener; current listener configuration uses `riak_api.pb` address/port pairs.

# Datatype

Integer

# Constraints

- TCP port number in `0..65535`; `0` requests an automatically assigned port.

# Inferred default

Unset (`undefined`); requires `riak_api.pb_ip` as well.

# Tags

feature: client-networking
repository: riak_api, riak_kv
module: riak_api_pb_listener, riak_kv_pb_object
concept: connections, compatibility

# Notes

This is the Erlang application environment key `pb_port` in `riak_api`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_api/src/riak_api_pb_listener.erl](https://github.com/OpenRiak/riak_api/blob/ffdbd6be1afd3e2350eee99dc96930f7b339c3bf/src/riak_api_pb_listener.erl#L106)
- [riak_kv/src/riak_kv_pb_object.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_pb_object.erl#L688)

# Reviewed against

3.4.0: 077f695d89586e54b2c876b7c43ae3364995de511ceded4e61bd39a7b7c045c4
3.4.1: 70339667a356f839be446d0e6c453008719947ed1f86502fa7b1d878bc319918
