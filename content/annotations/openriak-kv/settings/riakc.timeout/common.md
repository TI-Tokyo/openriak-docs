# Description

Fallback request timeout, in milliseconds, for the Erlang Protocol Buffers client when an operation has no more specific timeout. AAE-fold operations use a separate, longer default.

# Datatype

Timeout

# Units

- milliseconds

# Constraints

- Non-negative integer timeout or `infinity`; request-specific timeout options can override it.

# Inferred default

`60000` from `riakc.app.src` and the generic PB timeout macro. Operations with specialized defaults can use their own timeout.

# Tags

feature: client-networking
repository: riakc
module: riakc_pb_socket
concept: connections

# Notes

This is the Erlang application environment key `timeout` in `riakc`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riakc/src/riakc_pb_socket.erl](https://github.com/OpenRiak/riak-erlang-client/blob/69c8d51857cc5705f594143912264d32fe2b9a8a/src/riakc_pb_socket.erl#L1264)

Additional type/default evidence:

- [riakc/include/riakc.hrl](https://github.com/OpenRiak/riak-erlang-client/blob/69c8d51857cc5705f594143912264d32fe2b9a8a/include/riakc.hrl)
- [riakc/src/riakc.app.src](https://github.com/OpenRiak/riak-erlang-client/blob/69c8d51857cc5705f594143912264d32fe2b9a8a/src/riakc.app.src)

# Reviewed against

3.4.0: 6ef15383e9e7901f8b6a4313df4931ace916837294f38f92a25f153b47c99a64
3.4.1: 6ef15383e9e7901f8b6a4313df4931ace916837294f38f92a25f153b47c99a64
