# Description

Control packet coalescing on Protocol Buffers connections. The schema translates this into the socket's `nodelay` option: disabling Nagle sends small writes promptly, while enabling it permits TCP to combine them.

# Tags

feature: client-networking
repository: riak_api
module: riak_api_pb_listener
concept: connections

# Reviewed against

3.4.0: 35bca66588595b022fdad34af5374fa9f6eca8639dd6323175f5a58dae6ecc1d
3.4.1: 8e86cd7f0ab47154a34f6fb7b87b6488c3150a9cfb8f129700993f5babd25895
