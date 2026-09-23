# Description

Allocation strategy for the Erlang binary allocator's multi-block carriers. This changes how free blocks are reused; do not assume the runtime default is identical across OTP builds.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: memory, runtime

# Reviewed against

3.4.0: 61dd70c506f7e7e964ba2a74f4e50c90d553dbaa6e29657bf5728cc3ba4b623e
3.4.1: 61dd70c506f7e7e964ba2a74f4e50c90d553dbaa6e29657bf5728cc3ba4b623e
