# Description

Allocation strategy for the Erlang process-heap allocator's multi-block carriers. This changes how free blocks are reused; do not assume the runtime default is identical across OTP builds.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: memory, runtime

# Reviewed against

3.4.0: f17f87781d23c4135fe5196d27680cf2db3dc426ce3fcd52edf5a8614f81018f
3.4.1: f17f87781d23c4135fe5196d27680cf2db3dc426ce3fcd52edf5a8614f81018f
